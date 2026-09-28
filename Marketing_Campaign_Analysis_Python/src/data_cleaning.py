import pandas as pd
import numpy as np

RAW_PATH = "../data/raw/marketing_campaign_raw.csv"
CLEAN_PATH = "../data/cleaned/marketing_campaign_cleaned.csv"

df = pd.read_csv(RAW_PATH)

# Remove exact duplicate records
df = df.drop_duplicates()

# Standardize text fields
text_cols = ["Customer_Name","Gender","City","Country","Customer_Segment",
             "Campaign_Name","Campaign_Type","Channel","Response",
             "Email_Opened","Email_Clicked","Customer_Status"]
for col in text_cols:
    df[col] = df[col].astype("string").str.strip()

for col in ["Gender","Channel","Response","Email_Opened","Email_Clicked"]:
    df[col] = df[col].str.title()

# Normalize missing IDs
df["Campaign_ID"] = df["Campaign_ID"].astype("string").str.strip()
df["Campaign_ID"] = df["Campaign_ID"].replace({"<NA>": pd.NA, "nan": pd.NA})

# Numeric conversion
numeric_cols = ["Age","Income","Ad_Spend","Impressions","Clicks","Conversions",
                "Revenue","Cost","Purchase_Amount","Previous_Purchases","Website_Visits"]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Validate age
df.loc[(df["Age"] < 18) | (df["Age"] > 80), "Age"] = np.nan
df["Age"] = df["Age"].fillna(df["Age"].median()).round().astype(int)

# Handle monetary errors
for col in ["Income","Ad_Spend","Revenue","Cost","Purchase_Amount"]:
    df.loc[df[col] < 0, col] = np.nan
    df[col] = df[col].fillna(df[col].median())

# Fill categorical missing values
for col in ["City","Country","Customer_Segment","Campaign_ID","Campaign_Name","Campaign_Type","Channel"]:
    df[col] = df[col].fillna("Unknown")

# Dates
df["Campaign_Start_Date"] = pd.to_datetime(df["Campaign_Start_Date"], errors="coerce")
df["Campaign_End_Date"] = pd.to_datetime(df["Campaign_End_Date"], errors="coerce")
df["Campaign_Start_Date"] = df["Campaign_Start_Date"].fillna(df["Campaign_Start_Date"].median())
df["Campaign_End_Date"] = df["Campaign_End_Date"].fillna(df["Campaign_End_Date"].median())

# Logical fixes
df["Clicks"] = df["Clicks"].clip(lower=0)
df["Conversions"] = df["Conversions"].clip(lower=0)
df["Conversions"] = np.minimum(df["Conversions"], df["Clicks"])

df.to_csv(CLEAN_PATH, index=False)
print(f"Cleaned dataset saved to: {CLEAN_PATH}")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")
