# Python Project #3 — Marketing Campaign Analysis

## Overview
A complete Python portfolio project for analyzing marketing campaign performance, customer behavior, revenue, conversion, and ROI.

**Workflow:** Raw Data → Data Cleaning → EDA → Feature Engineering → Visualization → Business Insights

## Dataset
Approximately 5,000 campaign/customer interaction records.

Main fields include:
- Customer_ID, Customer_Name, Gender, Age
- City, Country, Income, Customer_Segment
- Campaign_ID, Campaign_Name, Campaign_Type, Channel
- Campaign_Start_Date, Campaign_End_Date
- Ad_Spend, Impressions, Clicks, Conversions
- Revenue, Cost, Purchase_Amount
- Response, Previous_Purchases
- Email_Opened, Email_Clicked, Website_Visits
- Customer_Status

## Data Quality Problems
The raw dataset intentionally contains:
- Duplicate records
- Missing values
- Invalid ages
- Negative monetary values
- Inconsistent categorical formatting
- Missing campaign IDs
- Potential outliers
- Mixed Yes/No formatting

## Feature Engineering
Created metrics:
- Age_Group
- Campaign_Duration
- CTR
- Conversion_Rate
- Profit
- Profit_Margin
- ROI
- Customer_Value
- Purchase_Frequency
- Campaign_Month

## Business Questions
1. Which campaigns generate the most revenue?
2. Which channels have the highest conversion rates?
3. How efficiently is advertising spend converted into revenue?
4. Which customer segments generate the most revenue?
5. How do clicks and impressions relate to conversions?
6. How do new and returning customers differ?
7. Which campaigns have strong ROI?
8. Which customers have the highest value?

## Project Structure
```text
Marketing_Campaign_Analysis_Python/
├── data/
│   ├── raw/marketing_campaign_raw.csv
│   └── cleaned/
├── src/
│   ├── data_cleaning.py
│   ├── feature_engineering.py
│   ├── analysis.py
│   └── eda.py
├── visualizations/
├── README.md
```

## Technologies
- Python
- Pandas
- NumPy
- Matplotlib
- Jupyter Notebook

## Author
**Ahmed Awwad**

Python / Data Analytics Portfolio Project
