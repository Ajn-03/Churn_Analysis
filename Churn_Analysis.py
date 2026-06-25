#!/usr/bin/env python
# coding: utf-8

# Task 1: Data Ingestion and Validation 11.06.26

#Load Dataset
import pandas as pd
import seaborn as sns
import streamlit as st
df = pd.read_csv("European_Bank.csv")

#To check data types and not null count
df.info()

#To check null values
print("Null value columns:")
for i in df.columns:
    if (df[i].isna()).any():
        print(f"{i} ")

#To check how many contain 0
print("Zero values columns:")
for i in df.columns:
    if (df[i]==0).any():
        print(f"{i} ",end="")

#To check if binary values are valid
print((df['HasCrCard']>1).sum())
print((df['IsActiveMember']>1).sum())

#To check -ve values
print("Negative values columns:")
for i in df.select_dtypes(include='number').columns:
    if (df[i]<0).any():
        print(f"{i} ",end="")

#To check Churn Label Consistency
if (df['Exited'].unique()).any() in range(0,2):
    print("Churn Accuracy Validated")
print(df['Exited'].unique())

#Task 2 Data Cleaning And Preparation 12.06.26

#Duplicates and Irrelevant Data
print(df.duplicated().sum())
df1=df.drop(columns=['Year','Surname','CustomerId'])
df1

#categorical columns and unique values
cate_col={}
for i in df1.columns:
    if df1[i].dtype=='object':
        cate_col[i]=df1[i].nunique()
print(cate_col)

#Check Typos
for i in df1.select_dtypes(include='object').columns:
    print(df[i].unique())

#Task 3 : Customer Segmentation design 13.06.26

#Checking Outliers and If Valid
df2=df.drop(columns=['Year','Surname','CustomerId','Geography','Gender'])
df2.describe()
import matplotlib.pyplot as plt 
fig, axs = plt.subplots(len(df2.columns), 1, figsize=(7, 12), dpi=95)
for i, col in enumerate(df2.columns):
    axs[i].boxplot(df2[col], vert=False)
    axs[i].set_ylabel(col)
plt.tight_layout()
plt.show()
plt.close()

#Segmentation
def segmentation(df,seg):
    max_seg=df[seg].max()
    min_seg=df[seg].min()
    q1=df[seg].quantile(0.25)
    q3=df[seg].quantile(0.75)
    return max_seg,min_seg,q1,q3

#Age Segmentation
max_age,a,b,c=segmentation(df,'Age')
df1['Age']=pd.cut(df1['Age'], bins=[0,29,45,60,max_age], labels=['<30','30-45','46-60','60+'])

#Credit Score Segmentation
max_cs,min_cs,q1,q3=segmentation(df,'CreditScore')
df1['CreditScore']=pd.cut(df1['CreditScore'],bins=[min_cs-1,q1,q3,max_cs],
                          labels=['Low','Medium', 'High'])

#Tenure Segmentation
max_t,min_t,q1,q3=segmentation(df,'Tenure')
df1['Tenure']=pd.cut(df1['Tenure'],bins=[min_t-1,q1,q3-1,max_t],
                          labels=['New','Mid-Term', 'Long-Term'])

#Balance segmentation
max_b=df1['Balance'].max()
med_b = df1[df1['Balance'] > 0]['Balance'].median()
df1['Balance'] = pd.cut(df1['Balance'],bins=[-1,0,med_b,max_b ],
                        labels=['Zero_Bal', 'Low_Bal', 'High_Bal'])

#Task 4 Churn Distribution Analysis 15.06.26

#Overall Churn Rate
def churn_summary(df1):    
    total_cust=df1.shape[0]
    total_churn=df1['Exited'].sum()
    total_retain=total_cust-total_churn
    churn_rate = (df1['Exited'].mean()*100).round(2)
    retain_rate=100-churn_rate
    return {
        "Total Customers": total_cust,
        "Churned Customers": total_churn,
        "Retained Customers": total_retain,
        "Overall Churn Rate": churn_rate,
        "Overall Retention Rate": retain_rate
    }

#Segment-wise Churn Rate
# if 100 mem in Germany then 30 of them churned
segments=['Geography','Gender','Age','CreditScore','Tenure','Balance']
import streamlit as st
import matplotlib.pyplot as plt

def seg_churn_rate(df1, segments):
    for i in segments:
        churn_seg = df1.groupby(i)['Exited'].mean().mul(100)
        churn_seg.plot(
            kind='bar',
            color=['pink', 'skyblue', 'yellow', 'lightgreen'],
            figsize=(3,3)
        )
        plt.title(f'Churn Rate (%) per {i} Segment',fontsize=8)
        plt.xticks(fontsize=8)
        plt.ylabel('Churn Rate (%)',fontsize=8)
        st.pyplot(plt.gcf())   # instead of plt.show()
        plt.clf()
        plt.close()# clears figure before next loop

#Churn contribution by segment size
#If 100 mem in total churned and Germany had 40 churned mem
print("Churn contribution by segment size\n")
def churn_contri_pie(df1,segments):
    for i in segments:
        churned_in_i=df1.groupby(i)['Exited'].sum()
        total_churned=df1['Exited'].sum()
        churn_contri=((churned_in_i*100)/(total_churned))
        churn_contri.plot(kind='pie', figsize=(5,3), autopct='%1.1f%%')
        plt.title(f'Churn Contribution By {i}')
        plt.ylabel('')
        yield plt.gcf()
        plt.clf()
        plt.close()

#Comparison of churned vs retained profiles

#Need More Segmentation For Comprehensive Comparison
#Estimated Salary Segmentation
max_s,min_s,q1,q3=segmentation(df,'EstimatedSalary')
df1['EstimatedSalary']=pd.cut(df1['EstimatedSalary'],bins=[min_s-1,q1,q3-1,max_s],
                          labels=['Low','Mid', 'High'])
#Num of Prod Segmentation
df1['NumOfProducts']=pd.cut(df1['NumOfProducts'],
                            bins=[0,1,4],
                           labels=['One','Multiple'])
#Has Cr Card and IsActiveMember
col=['HasCrCard','IsActiveMember']
for i in col:
    df1[i]=pd.cut(df1[i],
                  bins=[-1,0,1],
                  labels=['No','Yes'])
df1

#Total no. of churned and retained customers
churned = (df1['Exited'] == 1).sum()
retained=(df1['Exited'] == 0).sum()
print(churned)
print(retained)

def seg_csv(df1,segments,name):
    max_churned={}
    max_retained={}
    max_churn_contri=[]
    max_retain_contri=[]
    for i in segments:
        churn_seg=(df1.groupby(i)['Exited'].mean().mul(100).round(2))
        churned_in_i=df1.groupby(i)['Exited'].sum()
        total_churned=df1['Exited'].sum()
        churn_contri=((churned_in_i*100)/(total_churned))
        max_churn_contri.append(churn_contri.idxmax())
        max_retain_contri.append(churn_contri.idxmin())
        max_churned[i]=churn_seg.idxmax()
        max_retained[i]=churn_seg.idxmin()
    hb_df = pd.DataFrame({
        'Segment': max_churned.keys(),
        'Highest Churn Rate': max_churned.values(),
        'Highest Churn Contributor': max_churn_contri,
        'Highest Retain Rate Per Segment': max_retained.values(),
        'Highest Retained Contributor': max_retain_contri
    })

    hb_df.to_csv(f"{name}.csv",index=False)
    return hb_df

segments=['CreditScore','Geography','Gender','Age','Tenure','Balance','NumOfProducts','HasCrCard',
          'IsActiveMember','EstimatedSalary']
seg_csv(df1,segments,"Summary")

# Task 5 Comparative Demographic Analysis 16.06.26

#Gender-based churn difference
gender=df1.groupby('Gender')['Exited'].mean()
print(gender)

#Geography-Age Interaction Analysis
df1.groupby(['Geography','Age'])['Exited'].mean()
churn_seg=(df1.groupby(['Geography','Age'])['Exited'].mean().mul(100))
churn_seg.plot(kind='bar',
               color = ['pink', 'skyblue', 'yellow','lightgreen'],
                figsize=(5,5))
plt.title(f'Churn Rate (%) per Geography - Age Segment')
plt.ylabel('Churn Rate (%)')
plt.show()
plt.close()

churned_in_i=df1.groupby(['Geography','Age'])['Exited'].sum()
total_churned=df1['Exited'].sum()
churn_contri=((churned_in_i*100)/(total_churned))
churn_contri.plot(kind='pie', figsize=(5,3), autopct='%1.1f%%')
plt.title(f'Churn Contribution By Age In Geography')
plt.ylabel('')
plt.show()
plt.close()

#Financial Stability Vs Churn
df1.groupby(['EstimatedSalary','CreditScore'])['Exited'].mean().mul(100).round(2)

#Task 6 High-Value Customer Churn Analysis 17.06.26

#Identify High balance churners
high_bal_df=df1[df1['Balance']=='High_Bal']
print(f"Total number of High Balance Customers: {high_bal_df.shape[0]}")
print(f"Total number of High Balance churners: {high_bal_df['Exited'].sum()}")
print(f"Churn rate among High Balance customers: {(high_bal_df['Exited'].mean()*100).round(2)}")
print(f"Retention rate among High Balance customers: {100-(high_bal_df['Exited'].mean()*100).round(2)}")

segments=['CreditScore','Geography','Gender','Age','Tenure','NumOfProducts','HasCrCard',
          'IsActiveMember','EstimatedSalary']
seg_csv(high_bal_df,segments,"High_Bal")

#Compare salary vs balance churn patterns
df1.groupby(['Balance','EstimatedSalary'])['Exited'].mean().mul(100).round(2)

#Quantify revenue risk from churn
total_bal_lost=df[df['Exited']==1]['Balance'].sum()
print(f"Total Revenue lost : {total_bal_lost} Euros")
bal=df[df['Exited']==1].groupby('Geography')['Balance'].sum()
bal_per=((bal/total_bal_lost)*100).round(2)
print(f"Percentage of total churned balance contributed by each {bal_per}")

#Task 7 : Engagement Drop Indicator 18.06.26

#Inactivity Vs Churn
churn_rate=df1.groupby("IsActiveMember")['Exited'].mean().mul(100).round(2)
churn_contri=(df1.groupby("IsActiveMember")['Exited'].sum()*100)/(df1['Exited'].sum())
print(churn_rate)
churn_contri

#saving segmented value fields dataset
df1.to_csv("New_European_Bank.csv",index=False)

#age tenure heatmap
import seaborn as sns

def age_tenure_heatmap(df1,seg_1,seg_2):

    age_tenure = (
        df1.groupby([seg_1,seg_2])['Exited']
           .mean()
           .mul(100)
           .round(2)
           .reset_index()
           .pivot(index=seg_1, columns=seg_2, values='Exited')
    )

    fig, ax = plt.subplots(figsize=(6,3))

    sns.heatmap(
        age_tenure,
        annot=True,
        fmt='.1f',
        cmap='YlOrRd',
        ax=ax
    )

    ax.set_xlabel(seg_2,fontsize=8)
    ax.set_ylabel(seg_1,fontsize=8)
    plt.close()
    return fig

def dynamic_kpi(df1,a,sub_cate):#a means segment
    churn_seg = round(df1.loc[df1[a] == sub_cate, 'Exited'].mean() * 100,2)#Segment-wise churn rate
    churned_in_i = df1.loc[df1[a] == sub_cate, 'Exited'].sum()
    total_churned = df1['Exited'].sum()
    churn_contri = round((churned_in_i * 100) / total_churned,2) #Overall churn contribution
    high_val = round(df1.loc[(df1[a] == sub_cate) & (df1['Balance'] == 'High_Bal'),'Exited'].mean()*100,2)#Churn rate among high value customers belonging to this segment
    kpi={'ocr':churn_contri,'scr':churn_seg,'hvcr':high_val}
    return kpi

def high_val_groupby(df1,a,sub_cate,hv_gb):
    return pd.DataFrame(df1[(df1[a]==sub_cate) & (df1['Balance']=='High_Bal')].groupby(hv_gb)['Exited'].mean().mul(100).round(2))