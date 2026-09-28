# Customer Churn Analysis — Python & Pandas

A portfolio-ready end-to-end customer churn analysis project using Python, Pandas, NumPy and Matplotlib.

## Project Goals
- Clean and validate customer data
- Explore churn patterns
- Compare retained vs churned customers
- Analyze contract, payment, tenure and satisfaction factors
- Build business-oriented visualizations and insights

## Dataset
`data/customer_churn_raw.csv` contains 3,535 rows including intentionally duplicated and problematic records.

Columns:
- Customer_ID
- Gender
- Age
- City
- Tenure_Months
- Contract_Type
- Monthly_Charges
- Total_Charges
- Payment_Method
- Internet_Service
- Support_Calls
- Satisfaction_Score
- Late_Payments
- Churn

## Project Workflow
1. Data loading and inspection
2. Duplicate detection and removal
3. Missing-value treatment
4. Invalid-value validation
5. Feature engineering
6. Exploratory Data Analysis
7. Churn analysis
8. Visualization
9. Business insights and recommendations

## Cleaning Rules
- Remove exact duplicate rows.
- Replace invalid Age values outside 18–100 with the median valid age.
- Replace missing categorical values with `Unknown` or the mode where appropriate.
- Replace invalid/non-positive Monthly Charges with the median valid charge.
- Replace invalid Satisfaction Scores outside 1–5 with the median.
- Replace invalid Tenure values below 1 month with the median valid tenure.
- Recalculate/validate Total Charges when necessary.

## Visualizations
1. Churn Distribution
2. Churn by Gender
3. Churn by Age Group
4. Churn by Contract Type
5. Churn by Payment Method
6. Churn by Internet Service
7. Average Monthly Charges — Churn vs Retained
8. Churn by Tenure Group
9. Churn by Satisfaction Score
10. Churn by Support Calls

## Skills Demonstrated
Python · Pandas · NumPy · Matplotlib · Data Cleaning · EDA · GroupBy · Feature Engineering · Customer Churn Analysis · Data Visualization · Business Insights

## Author
**Ahmed Awwad**

Data Analyst | IT & Software Applications
