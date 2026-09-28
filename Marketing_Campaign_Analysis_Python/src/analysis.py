import pandas as pd
import numpy as np

df = pd.read_csv("../data/cleaned/marketing_campaign_features.csv")

campaign_summary = df.groupby(["Campaign_ID","Campaign_Name"], dropna=False).agg(
    Revenue=("Revenue","sum"),
    Ad_Spend=("Ad_Spend","sum"),
    Conversions=("Conversions","sum"),
    Clicks=("Clicks","sum"),
    Impressions=("Impressions","sum")
).reset_index()

campaign_summary["Conversion_Rate"] = np.where(
    campaign_summary["Clicks"]>0,
    campaign_summary["Conversions"]/campaign_summary["Clicks"]*100,0
)
campaign_summary["ROI"] = np.where(
    campaign_summary["Ad_Spend"]>0,
    (campaign_summary["Revenue"]-campaign_summary["Ad_Spend"])/campaign_summary["Ad_Spend"]*100,0
)

channel_summary = df.groupby("Channel").agg(
    Revenue=("Revenue","sum"),
    Ad_Spend=("Ad_Spend","sum"),
    Conversions=("Conversions","sum"),
    Clicks=("Clicks","sum"),
    Impressions=("Impressions","sum")
).reset_index()
channel_summary["Conversion_Rate"] = channel_summary["Conversions"]/channel_summary["Clicks"].replace(0,np.nan)*100
channel_summary["ROI"] = (channel_summary["Revenue"]-channel_summary["Ad_Spend"])/channel_summary["Ad_Spend"].replace(0,np.nan)*100

campaign_summary.to_csv("../data/cleaned/campaign_summary.csv",index=False)
channel_summary.to_csv("../data/cleaned/channel_summary.csv",index=False)

print("Top campaigns by revenue:")
print(campaign_summary.sort_values("Revenue", ascending=False).head(10))
print("\nChannel performance:")
print(channel_summary.sort_values("Revenue", ascending=False))
