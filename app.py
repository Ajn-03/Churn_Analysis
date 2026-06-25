import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from Churn_Analysis import churn_summary,seg_churn_rate,age_tenure_heatmap,high_val_groupby,dynamic_kpi

st.set_page_config(
    page_title="Churn Analysis",
    layout="wide"
)

st.title("Churn Analysis")
name=st.text_input("Enter Your Name")

if name:
    st.write(f"Hi {name} !")    
    st.header("Customer Churn Dashboard")
    tab1, tab2, tab3, tab4,tab5,tab6 = st.tabs(
    [
        "Overview",
        "KPIs",
        "Geography-wise churn visualization",
        "Age & tenure churn comparison",
        "High Value",
        "Segment Analysis & Comparison"
    ])

    #Read Database
    df = pd.read_csv("New_European_Bank.csv")

    with tab1:
        #Overall Churn Summary
        st.subheader("Churn Summary")
        summary = churn_summary(df)
        col1, col2, col3,col4,col5 = st.columns(5)
        col1.metric("Total Customers", summary["Total Customers"])
        col2.metric("Churned Customers", summary["Churned Customers"])
        col3.metric("Churn Rate", f"{summary["Overall Churn Rate"]}%")
        col4.metric("Retained Customers", summary["Retained Customers"])
        col5.metric("Retention Rate", f"{summary['Overall Retention Rate']}%")
        churn_df = pd.read_csv("churn_summary.csv")
        st.dataframe(churn_df,use_container_width=True,hide_index=True)
    
    with tab3:
        #Geography churn visualization
        st.subheader("Geography-wise churn visualization")
        seg=['Geography']
        seg_churn_rate(df,seg)
        segments=['CreditScore','Gender','Age','Tenure', 'Balance', 'NumOfProducts','HasCrCard',
                 'IsActiveMember','EstimatedSalary']
        seg_1='Geography'
        seg_2=st.selectbox("Geographic Risk Group By", segments)
        fig=age_tenure_heatmap(df,seg_1,seg_2)
        st.pyplot(fig)
        plt.close(fig)

    with tab4:    
        #Age & tenure churn comparison
        st.subheader("Age & tenure churn comparison")
        seg_1='Age'
        seg_2='Tenure'
        fig=age_tenure_heatmap(df,seg_1,seg_2)
        st.pyplot(fig)
        plt.close(fig)
        
    with tab5:
        # High-value customer churn explorer
        st.subheader("High-value customer churn explorer")
        high_bal = pd.read_csv("High_Bal.csv")
        st.dataframe(high_bal)

    with tab2:
        #Dynamic KPI updates
        st.subheader('Key Performance Indicators')
        segments=['CreditScore','Geography','Gender','Age','Tenure', 'Balance', 'NumOfProducts','HasCrCard',
                 'IsActiveMember','EstimatedSalary']
        a=st.selectbox("Select Segment",segments,key='select_seg')
        b=list(df[a].unique())#choose sub category list
        sub_cate=st.selectbox("Select sub category",b,key='sub_categories')
        button=st.button("Show",key='kpi')
        li=[]
        for i in segments:
            if i !=a and i!='Balance':
                li.append(i)

        if "show_kpi" not in st.session_state:
            st.session_state.show_kpi = False

        if button:
            st.session_state.show_kpi = True

        if st.session_state.show_kpi:
            kpi=dynamic_kpi(df,a,sub_cate)
            col1, col2, col3,col4= st.columns(4)
            col1.metric("Overall Churn Rate",f"{kpi["ocr"]}%")
            col2.metric("Segment Churn Rate",f"{kpi["scr"]}%")
            col3.metric("High-Value Churn Rate",f"{kpi["hvcr"]}%")
            with col4:
                hv_gb = st.selectbox("High-Value Group By", li)
                high_val_df=high_val_groupby(df,a,sub_cate,hv_gb)
                st.dataframe(high_val_df,width=130)                                            
            #Geographic Risk Index
            if a!='Geography':
                st.write("Geographic Risk Index")
                fig=age_tenure_heatmap(df,a,'Geography')
                st.pyplot(fig)
                plt.close(fig)
            #Engagement Drop Indicator
            st.write("Engagement Drop Indicator Churn Rate(%)")
            fig=age_tenure_heatmap(df,a,'IsActiveMember')
            st.pyplot(fig)
            plt.close(fig)

    with tab6:
        #Segment Filters
        st.subheader('Segment filters for churn rate (%) visualization')
        seg_filter = st.selectbox("Select Segment",segments)
        button = st.button("Submit")
        if button:
            seg_churn_rate(df,[seg_filter])

        #Churn comparison
        st.subheader("Churn comparison")
        seg_1=st.selectbox("Select Segment",segments,key='seg1')
        seg_2=st.selectbox("Select Segment",segments,key='seg2')
        button = st.button("Submit",key="churn_comp")
        if button:
            fig=age_tenure_heatmap(df,seg_1,seg_2)
            st.pyplot(fig)
            plt.close(fig)
