from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent
DATA = BASE / 'data/customer_churn_raw.csv'
OUT = BASE / 'outputs'
CHARTS = OUT / 'charts'
CHARTS.mkdir(parents=True, exist_ok=True)
df = pd.read_csv(DATA)
print('Initial shape:', df.shape)
print(df.info())
print('\nMissing values:\n', df.isna().sum())
print('\nDuplicate rows:', df.duplicated().sum())

# Cleaning
df = df.drop_duplicates().reset_index(drop=True)
for c in ['City', 'Contract_Type', 'Payment_Method', 'Internet_Service']:
    df[c] = df[c].fillna('Unknown')
valid_age = df.loc[df['Age'].between(18, 100), 'Age']
df.loc[~df['Age'].between(18, 100), 'Age'] = np.nan
df['Age'] = df['Age'].fillna(valid_age.median())
valid_tenure = df.loc[df['Tenure_Months'] >= 1, 'Tenure_Months']
df.loc[df['Tenure_Months'] < 1, 'Tenure_Months'] = np.nan
df['Tenure_Months'] = df['Tenure_Months'].fillna(valid_tenure.median())
valid_monthly = df.loc[df['Monthly_Charges'] > 0, 'Monthly_Charges']
df.loc[df['Monthly_Charges'] <= 0, 'Monthly_Charges'] = np.nan
df['Monthly_Charges'] = df['Monthly_Charges'].fillna(valid_monthly.median())
valid_sat = df.loc[df['Satisfaction_Score'].between(1, 5), 'Satisfaction_Score']
df.loc[~df['Satisfaction_Score'].between(1, 5), 'Satisfaction_Score'] = np.nan
df['Satisfaction_Score'] = df['Satisfaction_Score'].fillna(valid_sat.median())
df['Total_Charges'] = df['Monthly_Charges'] * df['Tenure_Months']

# Features
bins = [0, 24, 34, 44, 54, 100]
labels = ['Under 25', '25-34', '35-44', '45-54', '55+']
df['Age_Group'] = pd.cut(df['Age'], bins=bins, labels=labels)
tenure_bins = [0, 12, 24, 48, 72, 100]
tenure_labels = ['0-12 Months', '13-24 Months', '25-48 Months', '49-72 Months', '72+ Months']
df['Tenure_Group'] = pd.cut(df['Tenure_Months'], bins=tenure_bins, labels=tenure_labels, include_lowest=True)

print('\n=== Churn Distribution ===')
print(df['Churn'].value_counts())
print(df['Churn'].value_counts(normalize=True).mul(100).round(2))
for col in ['Gender', 'Contract_Type', 'Payment_Method', 'Internet_Service', 'Age_Group', 'Tenure_Group',
            'Satisfaction_Score', 'Support_Calls']:
    print(f'\n=== Churn by {col} ===')
    print(pd.crosstab(df[col], df['Churn'], normalize='index').mul(100).round(2))

summary = df.groupby('Churn').agg(Customers=('Customer_ID', 'count'), Avg_Monthly_Charges=('Monthly_Charges', 'mean'),
                                  Avg_Tenure=('Tenure_Months', 'mean'), Avg_Support_Calls=('Support_Calls', 'mean'),
                                  Avg_Satisfaction=('Satisfaction_Score', 'mean'),
                                  Avg_Late_Payments=('Late_Payments', 'mean')).round(2)
print('\n=== Churn Summary ===\n', summary)
df.to_csv(OUT / 'cleaned_customer_churn.csv', index=False)
summary.to_csv(OUT / 'churn_summary.csv')


# charts

def bar(s, title, xlabel, ylabel, name, rot=0):
    plt.figure(figsize=(10, 6))
    s.plot(kind='bar')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=rot)
    plt.tight_layout()
    plt.savefig(CHARTS / name, dpi=150)
    plt.close()


bar(df['Churn'].value_counts(), 'Churn Distribution', 'Churn', 'Customers', '01_churn_distribution.png')
bar(pd.crosstab(df['Gender'], df['Churn'], normalize='index').mul(100)['Yes'], 'Churn Rate by Gender', 'Gender',
    'Churn Rate (%)', '02_churn_by_gender.png')
bar(pd.crosstab(df['Age_Group'], df['Churn'], normalize='index').mul(100)['Yes'], 'Churn Rate by Age Group',
    'Age Group', 'Churn Rate (%)', '03_churn_by_age.png')
bar(pd.crosstab(df['Contract_Type'], df['Churn'], normalize='index').mul(100)['Yes'], 'Churn Rate by Contract Type',
    'Contract Type', 'Churn Rate (%)', '04_churn_by_contract.png', 20)
bar(pd.crosstab(df['Payment_Method'], df['Churn'], normalize='index').mul(100)['Yes'], 'Churn Rate by Payment Method',
    'Payment Method', 'Churn Rate (%)', '05_churn_by_payment.png', 20)
bar(pd.crosstab(df['Internet_Service'], df['Churn'], normalize='index').mul(100)['Yes'],
    'Churn Rate by Internet Service', 'Internet Service', 'Churn Rate (%)', '06_churn_by_internet.png', 20)
bar(df.groupby('Churn')['Monthly_Charges'].mean(), 'Average Monthly Charges by Churn', 'Churn',
    'Average Monthly Charges', '07_avg_monthly_charges.png')
bar(pd.crosstab(df['Tenure_Group'], df['Churn'], normalize='index').mul(100)['Yes'], 'Churn Rate by Tenure Group',
    'Tenure Group', 'Churn Rate (%)', '08_churn_by_tenure.png', 20)
bar(pd.crosstab(df['Satisfaction_Score'], df['Churn'], normalize='index').mul(100)['Yes'],
    'Churn Rate by Satisfaction Score', 'Satisfaction Score', 'Churn Rate (%)', '09_churn_by_satisfaction.png')
bar(df.groupby('Churn')['Support_Calls'].mean(), 'Average Support Calls by Churn', 'Churn', 'Average Support Calls',
    '10_support_calls_by_churn.png')
print('\nAnalysis completed. Outputs saved to outputs/.')
