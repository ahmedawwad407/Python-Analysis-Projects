# E-Commerce Sales Analysis — Python & Pandas

A portfolio-ready end-to-end **E-Commerce Sales Analysis** project using Python, Pandas, NumPy, and Matplotlib.

## Project Overview

This project covers a complete data-analysis workflow:

- Data loading and inspection
- Missing-value analysis
- Duplicate detection
- Data cleaning and validation
- Invalid-value and outlier handling
- Feature engineering
- Exploratory Data Analysis (EDA)
- Sales and customer analysis
- RFM customer segmentation
- Business insights
- Data visualization

## Dataset

Place the project CSV at:

```text
data/sales_data.csv
```

Expected columns:

```text
Order_ID
Order_Date
Customer_ID
Customer_Name
Gender
Age
City
Product
Category
Unit_Price
Quantity
Discount
Payment_Method
Sales_Rep
Region
```

## Project Structure

```text
E-Commerce_Sales_Analysis_Python/
│
├── data/
│   ├── sales_data.csv
│   └── README.md
│
├── outputs/
│   ├── charts/
│   ├── cleaned_sales_data.csv
│   ├── rfm_customer_segments.csv
│   └── segment_sales_summary.csv
│
├── analysis.py
└── README.md
```

## Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- PyCharm
- GitHub

## Data Cleaning

The analysis includes:

1. Removing exact duplicate rows.
2. Inspecting duplicate `Order_ID` values without automatically deleting valid distinct records.
3. Converting `Order_Date` to datetime.
4. Removing rows with unavailable order dates.
5. Filling missing customer names and cities with `Unknown`.
6. Replacing invalid ages outside the accepted range with the median.
7. Filling missing products with the product mode.
8. Validating discounts and replacing invalid values with the median.
9. Filling missing payment methods and sales representatives with their modes.
10. Replacing negative quantities with the median valid quantity.
11. Replacing non-positive unit prices with the median valid price.
12. Replacing extreme placeholder prices such as `99999` with a valid median price.
13. Removing zero-quantity orders because they generate zero sales.

## Feature Engineering

```python
Sales = Unit_Price * Quantity
Net_Sales = Sales * (1 - Discount)
```

Additional fields include:

- `Year_Month`
- `Age_Group`
- `Recency`
- `Frequency`
- `Monetary`
- RFM scores
- Customer segments

## RFM Analysis

Customers are segmented using:

- **Recency:** days since the customer's last purchase
- **Frequency:** number of unique orders
- **Monetary:** total net sales

The project uses quintile-based RFM scoring and the following project-defined segmentation rules:

| Segment | RFM Score |
|---|---:|
| Champions | 13–15 |
| Loyal Customers | 10–12 |
| Potential Loyalists | 7–9 |
| At Risk | 5–6 |
| Lost Customers | 3–4 |

These thresholds are analytical conventions for this project, not a universal RFM standard.

## Key Results From the Completed Analysis

After cleaning, the analyzed dataset contained **2,988 orders**.

### Overall Performance

- Total Sales: **5,362,454.65**
- Total Net Sales: **4,996,892.91**
- Average Net Sales per Order: **1,668.41**

### Category

Electronics generated approximately **2.98M** in net sales, about **59.7%** of total net sales.

### Region

- Central: approximately **1.72M**
- South: approximately **1.66M**
- North: approximately **1.62M**

### Top Products by Net Sales

1. Tablet — approximately **676K**
2. Smart Watch — approximately **618K**
3. Smartphone — approximately **609K**
4. Laptop — approximately **561K**
5. Headphones — approximately **523K**

### Year-over-Year

- 2024 Net Sales: approximately **2.47M**
- 2025 Net Sales: approximately **2.52M**
- YoY growth: approximately **2.1%**

### Customer Segments

| Segment | Customers | Sales Share |
|---|---:|---:|
| Loyal Customers | 164 | 36.67% |
| Potential Loyalists | 189 | 27.41% |
| Champions | 83 | 25.41% |
| At Risk | 77 | 6.31% |
| Lost Customers | 81 | 4.21% |

## Visualizations

The Python script creates 10 charts:

1. Net Sales by Category
2. Net Sales by Region
3. Monthly Net Sales Trend
4. Top 10 Products by Net Sales
5. Net Sales by Age Group
6. Customer Segments Distribution
7. Net Sales by Customer Segment
8. Average Recency by Segment
9. Average Frequency by Segment
10. Average Monetary Value by Segment

Charts are saved automatically to:

```text
outputs/charts/
```

## Business Recommendations

Based on the observed data patterns:

- Monitor electronics inventory and performance because the category contributes a large share of sales.
- Use RFM segments to design differentiated customer-engagement strategies.
- Consider retention initiatives for high-value and recently active customers.
- Investigate re-engagement opportunities among At Risk and Lost customers.
- Review lower-performing products for pricing, bundling, and merchandising opportunities.
- Monitor monthly sales fluctuations rather than assuming continuous growth.


## Portfolio Skills Demonstrated

- Data Cleaning
- Exploratory Data Analysis (EDA)
- Pandas
- NumPy
- Data Validation
- Feature Engineering
- GroupBy Aggregations
- RFM Analysis
- Customer Segmentation
- Data Visualization
- Business Insight Generation

## Author

**Ahmed Awwad**  
Data Analyst | IT & Software Applications

Portfolio: https://ahmedawwad407.github.io/AhmedAwwad.githup.io/
