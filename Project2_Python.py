# import libraries

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
#import datetime
import mysql.connector 
import seaborn as sns

st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

connection=mysql.connector.connect(user = 'toyscie', password = 'WILD4Rdata!', host = '51.68.18.102', port = '23456', database = 'toys_and_models')

col1, col2, col3 = st.columns(3)
#[2,1,3]

col1_1, col1_2 = st.columns(2)

query_sales= '''WITH productline_quantity AS (
SELECT productline, YEAR(orderDate) order_year, SUM(quantityordered) order_quantity, MONTH(orderDate) order_month
FROM orders
INNER JOIN orderdetails USING (orderNumber)
INNER JOIN products USING (productCode)
GROUP BY productline, order_year, order_month
)
SELECT productline, order_year, order_month, order_quantity,
LAG(order_quantity, 1) OVER (
PARTITION BY productLine, order_month
ORDER BY order_month, order_year) as prev_year_order_quantity, (order_quantity * 100)/lag(order_quantity, 1) OVER (
        PARTITION BY productLine, order_month
        ORDER BY order_month, order_year) as ratechange
FROM
    productline_quantity'''

df_sales= pd.read_sql(query_sales, con=connection)

#Second Graphic

with col1:
    st.subheader('''The number of products sold by category:''')
    fig3, ax3 = plt.subplots(figsize=(10,4))
    colors=['grey', 'black', 'blue']
    sns.barplot(data=df_sales, x="productline", y="order_quantity", hue="order_year", ci=None, palette=colors)
    ax3.set_xlabel("Categories")
    ax3.set_ylabel("# orders")
    ax3.legend(title="Year: ")
    ax3.set_title('# products by category')
    st.pyplot(fig3)
    
    st.subheader('''The number of products sold by category:''')
    fig3, ax3 = plt.subplots(figsize=(10,4))
    colors=['grey', 'black', 'blue']
    sns.barplot(data=df_sales, x="productline", y="order_quantity", hue="order_year", ci=None, palette=colors)
    ax3.set_xlabel("Categories")
    ax3.set_ylabel("# orders")
    ax3.legend(title="Year: ")
    ax3.set_title('# products by category')
    st.pyplot(fig3)
      
    with col1_1:
            st.subheader('''The number of products sold by category:''')
            fig3, ax3 = plt.subplots(figsize=(10,4))
            colors=['grey', 'black', 'blue']
            sns.barplot(data=df_sales, x="productline", y="order_quantity", hue="order_year", ci=None, palette=colors)
            ax3.set_xlabel("Categories")
            ax3.set_ylabel("# orders")
            ax3.legend(title="Year: ")
            ax3.set_title('# products by category')
            st.pyplot(fig3)
    with col1_2:
            st.subheader('''The number of products sold by category:''')
            fig3, ax3 = plt.subplots(figsize=(10,4))
            colors=['grey', 'black', 'blue']
            sns.barplot(data=df_sales, x="productline", y="order_quantity", hue="order_year", ci=None, palette=colors)
            ax3.set_xlabel("Categories")
            ax3.set_ylabel("# orders")
            ax3.legend(title="Year: ")
            ax3.set_title('# products by category')
            st.pyplot(fig3)
    
with col2:
    st.subheader('''The number of products sold by category:''')
    fig3, ax3 = plt.subplots(figsize=(10,4))
    colors=['grey', 'black', 'blue']
    sns.barplot(data=df_sales, x="productline", y="order_quantity", hue="order_year", ci=None, palette=colors)
    ax3.set_xlabel("Categories")
    ax3.set_ylabel("# orders")
    ax3.legend(title="Year: ")
    ax3.set_title('# products by category')
    st.pyplot(fig3)

with col3:
    st.subheader('''The number of products sold by category:''')
    fig3, ax3 = plt.subplots(figsize=(10,4))
    colors=['grey', 'black', 'blue']
    sns.barplot(data=df_sales, x="productline", y="order_quantity", hue="order_year", ci=None, palette=colors)
    ax3.set_xlabel("Categories")
    ax3.set_ylabel("# orders")
    ax3.legend(title="Year: ")
    ax3.set_title('# products by category')
    st.pyplot(fig3)

