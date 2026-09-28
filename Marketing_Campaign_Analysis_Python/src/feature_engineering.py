import pandas as pd
import numpy as np

INPUT = "../data/cleaned/marketing_campaign_cleaned.csv"
OUTPUT = "../data/cleaned/marketing_campaign_features.csv"

df = pd.read_csv(INPUT, parse_dates=["Campaign_Start_Date","Campaign_End_Date"])

df["Age_Group"] = pd.cut(
    df["Age"], bins=[17,24,34,44,54,64,100],
    labels=["18-24","25-34","35-44","45-54","55-64","65+"]
)

df["Campaign_Duration"] = (
    df["Campaign_End_Date"] - df["Campaign_Start_Date"]
).dt.days.clip(lower=0)

df["CTR"] = np.where(df["Impressions"] > 0, df["Clicks"]/df["Impressions"]*100, 0)
df["Conversion_Rate"] = np.where(df["Clicks"] > 0, df["Conversions"]/df["Clicks"]*100, 0)
df["Profit"] = df["Revenue"] - df["Cost"]
df["Profit_Margin"] = np.where(df["Revenue"] > 0, df["Profit"]/df["Revenue"]*100, 0)
df["ROI"] = np.where(df["Ad_Spend"] > 0, (df["Revenue"]-df["Ad_Spend"])/df["Ad_Spend"]*100, 0)
df["Email_Open_Rate"] = np.where(
    df["Channel"].eq("Email"), (df["Email_Opened"].eq("Yes").astype(int))*100, np.nan
)
df["Email_Click_Rate"] = np.where(
    df["Channel"].eq("Email"), (df["Email_Clicked"].eq("Yes").astype(int))*100, np.nan
)
df["Customer_Value"] = df["Previous_Purchases"] * df["Purchase_Amount"] + df["Purchase_Amount"]
df["Purchase_Frequency"] = df["Previous_Purchases"] + (df["Conversions"] > 0).astype(int)
df["Campaign_Month"] = df["Campaign_Start_Date"].dt.to_period("M").astype(str)

df.to_csv(OUTPUT,index=False)
print(f"Feature dataset saved to: {OUTPUT}")
