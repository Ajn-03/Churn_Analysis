# Churn Analysis
This project analyzes customer churn in a European bank using Exploratory Data Analysis (EDA). It identifies demographic, geographic, financial, and behavioral factors associated with customer attrition and presents the findings through an interactive Streamlit dashboard to support data-driven retention strategies.

## Problem Statement
Despite having rich customer-level data, banks face challenges in:
- Identifying high-risk customer segments
- Understanding churn differences by geography and demographics
- Quantifying the financial profile of churned customers

## Project Objectives
- Measure overall churn rate
- Identify churn distribution across customer segments
- Compare churn behavior across European regions

## Dataset
- Source : [European Banking Dataset](https://drive.google.com/file/d/11QvtjI65oXCtcNmoNa3qYdPs3xBcc84b/view?usp=sharing)
- Total Records : 10,000
- Features : 13
- Target Variable : 'Exited' (0 = retained, 1 = churned)

## Project Structure
1. Datasets:
   - European_Banking.csv (Original dataset)
   - New_European_Banking.csv (Segmented fields)
   - High_Bal.csv (High value customer churn summary)
   - churn_summary.csv
2. Python File:
   - Churn_Analysis.py
3. Streamlit App:
   - app.py
4. Reports:
   - Churn_EDA_Report.pdf
   - Executive_Summary.pdf
5. requirements.txt

## Technologies Used
1. Python
2. Streamlit
3. Pandas
4. Matplotlib
5. Seaborn
6. Jupyter Notebook

## Exploratory Data Analysis
- Data preparation and cleaning 
- Missing value analysis
- Duplicate detection
- Outlier detection
- Customer Segmentation 
- Customer demographic analysis
- Financial behavior analysis
- Feature-wise churn comparison
- Correlation analysis

## Key Insights
- Overall churn rate is 20.37%.
- Demographically, Female customers exhibit the highest churn rate among all regions.
- Region-wise, Germany has the highest churn rate that is 35%.
- Customers aged 46–60 years churn more frequently which is approx 50%.
- Behaviorally, single product owners and inactive members are significantly more likely to leave.
- Customers with high balances have 24% churn rate.
- Overall, banks face revenue loss of 18 Million Euros.

# Business Recommendations
- Implement customer engagement strategies
- Exclusive loyalty benefit programs for high value customer retention.
- Speedy customer grievance addressal
- Machine learning based prediction model to prevent churn by identifying the pattern.

## Key Performance Indicators (KPIs)
<table>
  <tr>
  <th>KPI Name</th>	<th>Description</th>
  </tr>
<tr>
  <td>Overall Churn Rate</td>
<td>% customers who exited</td>
</tr>	<tr>
  <td>Segment Churn Rate</td>
	<td>Churn % by segment</td></tr>
<tr>
  <td>High-Value Churn Ratio</td>	
  <td>Churn among premium customers</td></tr>
  <tr>
    <td>Geographic Risk Index</td>	
    <td>Regional churn exposure</td></tr>
  <tr>
    <td>Engagement Drop Indicator</td>	
    <td>Inactivity vs churn</td></tr>
</table>

## Streamlit Dashboard Features
- Overall Churn Summary
- Dynamic Key Performance Indicators (KPIs)
- Segment-wise churn visualization & comparison with other segments
- Geography-wise churn visualization
- Age-Tenure churn comparison
- High-value customer churn explorer

## Installation
1. git clone https://github.com/Ajn-03/Churn_Analysis.git
2. pip install -r requirements.txt
3. streamlit run app.py

## Preview 
<img width="895" height="689" alt="image" src="https://github.com/user-attachments/assets/fb6b8fce-5b28-4b9b-9e75-e30e1d86309e" />
<img width="900" height="631" alt="image" src="https://github.com/user-attachments/assets/eceaab5f-07c9-4a44-a8ea-d02207a04a83" />
<img width="891" height="573" alt="image" src="https://github.com/user-attachments/assets/db81243f-9cd8-42ed-b390-78981ee338dc" />
<img width="890" height="573" alt="image" src="https://github.com/user-attachments/assets/278466ff-315b-4c63-a1ad-02038a740084" />
<img width="651" height="697" alt="image" src="https://github.com/user-attachments/assets/80266b86-95eb-450b-b21f-77da498b3710" />

## Dashboard Link
[Churn Analysis Dashboard](https://churnanalysis-kzenkrauxmf4y43vexy3js.streamlit.app/?)

## Conclusion
Thus, this project provides a clear, segmentation-driven understanding of customer churn in European banking. By uncovering churn patterns across geography, demographics, and financial profiles, it equips decision-makers with actionable insights to design targeted, data-driven retention strategies.

### Author
Aditi Jain | [LinkedIn](https://www.linkedin.com/in/aditijainn26/) | Email: aditij2603@gmail.com
