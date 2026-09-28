import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../data/cleaned/marketing_campaign_features.csv")

# 1. Revenue by campaign
campaign_rev = df.groupby("Campaign_Name")["Revenue"].sum().sort_values()
plt.figure(figsize=(10,6))
campaign_rev.plot(kind="barh")
plt.title("Revenue by Campaign")
plt.xlabel("Revenue")
plt.tight_layout()
plt.savefig("../visualizations/revenue_by_campaign.png", dpi=150)
plt.close()

# 2. Revenue by channel
channel_rev = df.groupby("Channel")["Revenue"].sum().sort_values()
plt.figure(figsize=(10,6))
channel_rev.plot(kind="bar")
plt.title("Revenue by Channel")
plt.ylabel("Revenue")
plt.xticks(rotation=35, ha="right")
plt.tight_layout()
plt.savefig("../visualizations/channel_performance.png", dpi=150)
plt.close()

# 3. Conversion rate by channel
g = df.groupby("Channel")[["Clicks","Conversions"]].sum()
g["Conversion_Rate"] = g["Conversions"] / g["Clicks"].replace(0, pd.NA) * 100
plt.figure(figsize=(9,5))
g["Conversion_Rate"].sort_values().plot(kind="bar")
plt.title("Conversion Rate by Channel")
plt.ylabel("Conversion Rate (%)")
plt.xticks(rotation=35, ha="right")
plt.tight_layout()
plt.savefig("../visualizations/conversion_rate.png", dpi=150)
plt.close()

# 4. Customer segment revenue
seg = df.groupby("Customer_Segment")["Revenue"].sum().sort_values()
plt.figure(figsize=(9,5))
seg.plot(kind="bar")
plt.title("Revenue by Customer Segment")
plt.ylabel("Revenue")
plt.xticks(rotation=25)
plt.tight_layout()
plt.savefig("../visualizations/customer_segments.png", dpi=150)
plt.close()

# 5. Ad spend vs revenue
plt.figure(figsize=(8,6))
plt.scatter(df["Ad_Spend"], df["Revenue"], alpha=.35)
plt.title("Ad Spend vs Revenue")
plt.xlabel("Ad Spend")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig("../visualizations/ad_spend_vs_revenue.png", dpi=150)
plt.close()

print("EDA visualizations created.")
