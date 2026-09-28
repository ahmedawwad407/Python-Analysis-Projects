from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "sales_raw.csv"
CHART_DIR = BASE_DIR / "outputs" / "charts"
CHART_DIR.mkdir(parents=True, exist_ok=True)

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATA_PATH}\n"
        "Place your CSV at data/sales_data.csv"
    )

df = pd.read_csv(DATA_PATH)
print("Initial shape:", df.shape)

# ---------- Cleaning ----------
df = df.drop_duplicates().reset_index(drop=True)
df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
df = df.dropna(subset=["Order_Date"]).reset_index(drop=True)

df["Customer_Name"] = df["Customer_Name"].fillna("Unknown")
df["City"] = df["City"].fillna("Unknown")

invalid_age = (df["Age"] < 18) | (df["Age"] > 100)
df.loc[invalid_age, "Age"] = np.nan
df["Age"] = df["Age"].fillna(df["Age"].median())

df["Product"] = df["Product"].fillna(df["Product"].mode()[0])

invalid_discount = (df["Discount"] < 0) | (df["Discount"] > 1)
df.loc[invalid_discount, "Discount"] = np.nan
df["Discount"] = df["Discount"].fillna(df["Discount"].median())

df["Payment_Method"] = df["Payment_Method"].fillna(df["Payment_Method"].mode()[0])
df["Sales_Rep"] = df["Sales_Rep"].fillna(df["Sales_Rep"].mode()[0])

median_quantity = df.loc[df["Quantity"] >= 0, "Quantity"].median()
df.loc[df["Quantity"] < 0, "Quantity"] = median_quantity

median_price = df.loc[df["Unit_Price"] > 0, "Unit_Price"].median()
df.loc[df["Unit_Price"] <= 0, "Unit_Price"] = median_price

reasonable_price = df.loc[df["Unit_Price"] < 99999, "Unit_Price"].median()
df.loc[df["Unit_Price"] >= 99999, "Unit_Price"] = reasonable_price

df = df[df["Quantity"] > 0].reset_index(drop=True)
df["Category"] = df["Category"].astype(str).str.strip().str.title()

# ---------- Feature Engineering ----------
df["Sales"] = df["Unit_Price"] * df["Quantity"]
df["Net_Sales"] = df["Sales"] * (1 - df["Discount"])
df["Year_Month"] = df["Order_Date"].dt.to_period("M").astype(str)

bins = [0, 24, 34, 44, 54, 100]
labels = ["Under 25", "25-34", "35-44", "45-54", "55+"]
df["Age_Group"] = pd.cut(df["Age"], bins=bins, labels=labels)

# ---------- Core Analysis ----------
print("\n=== Overall Performance ===")
print("Rows:", len(df))
print("Total Sales:", round(df["Sales"].sum(), 2))
print("Total Net Sales:", round(df["Net_Sales"].sum(), 2))
print("Average Net Sales / Order:", round(df["Net_Sales"].mean(), 2))

category_sales = df.groupby("Category")["Net_Sales"].sum().sort_values(ascending=False)
region_sales = df.groupby("Region")["Net_Sales"].sum().sort_values(ascending=False)

product_analysis = (
    df.groupby("Product")
    .agg(Orders=("Order_ID", "count"), Units_Sold=("Quantity", "sum"),
         Net_Sales=("Net_Sales", "sum"), Avg_Order_Value=("Net_Sales", "mean"))
    .sort_values("Net_Sales", ascending=False)
)

monthly_sales = df.groupby("Year_Month").agg(Orders=("Order_ID", "count"), Net_Sales=("Net_Sales", "sum"))
yearly_sales = df.groupby(df["Order_Date"].dt.year).agg(
    Orders=("Order_ID", "count"), Net_Sales=("Net_Sales", "sum"), Avg_Order_Value=("Net_Sales", "mean")
)
age_analysis = df.groupby("Age_Group", observed=True).agg(
    Orders=("Order_ID", "count"), Net_Sales=("Net_Sales", "sum"), Avg_Order_Value=("Net_Sales", "mean")
)

print("\n=== Category ===\n", category_sales)
print("\n=== Region ===\n", region_sales)
print("\n=== Top Products ===\n", product_analysis.head(10))
print("\n=== Yearly Sales ===\n", yearly_sales)
print("\n=== Age Groups ===\n", age_analysis)

# ---------- RFM ----------
reference_date = df["Order_Date"].max()
rfm = df.groupby("Customer_ID").agg(Last_Purchase=("Order_Date", "max"))
rfm["Recency"] = (reference_date - rfm["Last_Purchase"]).dt.days
rfm["Frequency"] = df.groupby("Customer_ID")["Order_ID"].nunique()
rfm["Monetary"] = df.groupby("Customer_ID")["Net_Sales"].sum()

rfm["R_Score"] = pd.qcut(rfm["Recency"], 5, labels=[5,4,3,2,1], duplicates="drop").astype(int)
rfm["F_Score"] = pd.qcut(rfm["Frequency"], 5, labels=[1,2,3,4,5], duplicates="drop").astype(int)
rfm["M_Score"] = pd.qcut(rfm["Monetary"], 5, labels=[1,2,3,4,5], duplicates="drop").astype(int)
rfm["RFM_Score"] = rfm[["R_Score", "F_Score", "M_Score"]].sum(axis=1)

def segment_customer(score):
    if score >= 13:
        return "Champions"
    if score >= 10:
        return "Loyal Customers"
    if score >= 7:
        return "Potential Loyalists"
    if score >= 5:
        return "At Risk"
    return "Lost Customers"

rfm["Segment"] = rfm["RFM_Score"].apply(segment_customer)

df_segment = df.merge(rfm[["Segment"]], on="Customer_ID", how="left")
segment_sales = df_segment.groupby("Segment").agg(
    Customers=("Customer_ID", "nunique"), Orders=("Order_ID", "nunique"),
    Net_Sales=("Net_Sales", "sum"), Avg_Order_Value=("Net_Sales", "mean")
).sort_values("Net_Sales", ascending=False)
segment_sales["Sales_Share_%"] = (segment_sales["Net_Sales"] / df["Net_Sales"].sum() * 100).round(2)

print("\n=== RFM Segments ===\n", rfm["Segment"].value_counts())
print("\n=== Segment Sales ===\n", segment_sales)

# ---------- Visualizations ----------
def save_bar(series, title, xlabel, ylabel, filename, rotation=0):
    plt.figure(figsize=(10, 6))
    series.plot(kind="bar")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=rotation)
    plt.tight_layout()
    plt.savefig(CHART_DIR / filename, dpi=150)
    plt.close()

def save_barh(series, title, xlabel, ylabel, filename):
    plt.figure(figsize=(10, 6))
    series.sort_values().plot(kind="barh")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(CHART_DIR / filename, dpi=150)
    plt.close()

save_bar(category_sales, "Net Sales by Category", "Category", "Net Sales", "01_net_sales_by_category.png")
save_bar(region_sales, "Net Sales by Region", "Region", "Net Sales", "02_net_sales_by_region.png")

plt.figure(figsize=(14, 6))
plt.plot(monthly_sales.index, monthly_sales["Net_Sales"], marker="o")
plt.title("Monthly Net Sales Trend")
plt.xlabel("Month")
plt.ylabel("Net Sales")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(CHART_DIR / "03_monthly_net_sales_trend.png", dpi=150)
plt.close()

save_barh(product_analysis["Net_Sales"].head(10), "Top 10 Products by Net Sales", "Net Sales", "Product", "04_top_10_products.png")
save_bar(age_analysis["Net_Sales"], "Net Sales by Age Group", "Age Group", "Net Sales", "05_net_sales_by_age_group.png")

order = ["Champions", "Loyal Customers", "Potential Loyalists", "At Risk", "Lost Customers"]
segment_counts = rfm["Segment"].value_counts().reindex(order)
save_bar(segment_counts, "Customer Segments Distribution", "Customer Segment", "Number of Customers", "06_customer_segments_distribution.png", 20)
save_bar(segment_sales["Net_Sales"].reindex(order), "Net Sales by Customer Segment", "Customer Segment", "Net Sales", "07_net_sales_by_segment.png", 20)

segment_rfm = rfm.groupby("Segment").agg(
    Customers=("RFM_Score", "count"), Avg_Recency=("Recency", "mean"),
    Avg_Frequency=("Frequency", "mean"), Avg_Monetary=("Monetary", "mean"),
    Avg_RFM_Score=("RFM_Score", "mean")
).reindex(order)

save_bar(segment_rfm["Avg_Recency"], "Average Recency by Customer Segment", "Customer Segment", "Average Days Since Last Purchase", "08_average_recency.png", 20)
save_bar(segment_rfm["Avg_Frequency"], "Average Purchase Frequency by Customer Segment", "Customer Segment", "Average Number of Orders", "09_average_frequency.png", 20)
save_bar(segment_rfm["Avg_Monetary"], "Average Monetary Value by Customer Segment", "Customer Segment", "Average Net Sales per Customer", "10_average_monetary.png", 20)

# ---------- Outputs ----------
df.to_csv(BASE_DIR / "outputs" / "cleaned_sales_data.csv", index=False)
rfm.reset_index().to_csv(BASE_DIR / "outputs" / "rfm_customer_segments.csv", index=False)
segment_sales.reset_index().to_csv(BASE_DIR / "outputs" / "segment_sales_summary.csv", index=False)

print("\nAnalysis completed. Charts and CSV outputs are in outputs/.")
