# import libraries

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
#import datetime
import mysql.connector 
import seaborn as sns


st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a Dashboard about the Sales on the different categores of our Company"
    }
)



connection=mysql.connector.connect(user = 'toyscie', password = 'WILD4Rdata!', host = '51.68.18.102', port = '23456', database = 'toys_and_models')

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

query_logistics= '''select p.productname,p.productline, sum(od.quantityordered) as sumOrdered, p.quantityinstock from products p join orderdetails od on p.productcode=od.productCode
group by p.productname
order by sumOrdered desc
limit 5'''

df_logistics=pd.read_sql(query_logistics, con=connection)

#colors = sns.color_palette("ch:start=.2,rot=-.3", as_cmap=True)
colors = ['lightgrey', 'darkgrey', 'dimgrey']

st.title('''Avaliation of the categories in the company''')

col1, col2, col3= st.columns(3, gap="Large")

# SALES 

# with col1:
#     st.title('''Sales''')
#     st.subheader('''The rate of change compared to the same month of the previous year:''')
#     fig2, ax2 = plt.subplots(figsize=(10,4))
#     colors=['grey', 'black']
#     sns.barplot(data=df_sales, x="order_month", y="ratechange", hue="order_year", ci=None, palette=colors)
#     ax2.set_xlabel("Month")
#     ax2.set_ylabel("Rate of change (%)")
#     ax2.legend(title="Year: ")
#     ax2.set_title('Rate of change')
#     st.pyplot(fig2)
#     st.write("  ")

with col1:
    #Second Graphic
    st.header('''The number of products sold by category:''')
    #st.subheader('''The number of products sold by category:''')
    fig3, ax3 = plt.subplots(figsize=(10,12))
    #colors=['grey', 'black', 'blue']
    sns.barplot(data=df_sales, x="productline", y="order_quantity", hue="order_year", ci=None, palette=colors)
    ax3.set_xlabel("Categories")
    ax3.set_ylabel("# orders")
    ax3.legend(title="Year: ")
    ax3.set_title('# products by category')
    st.pyplot(fig3)

# LOGISTICS

with col2:
    #st.title('''Logistics''')
    st.header('''The stock of the 5 most ordered products:''')
    #st.subheader('''The stock of the 5 most ordered products:''')
    fig, ax1 = plt.subplots(figsize=(10, 12))
    ax1.bar(df_logistics["productname"], df_logistics["quantityinstock"], color='darkgrey')
    ax1.set_title('# stock x product')
    ax1.set_ylabel('Qty in stock (nº)')
    ax1.set_xlabel('Product')
    fig.autofmt_xdate()
    # ax2 = ax1.twinx()
    # ax2.set_ylabel('# orders')
    # ax2.plot(df_logistics["productname"], df_logistics["sumOrdered"], color = 'blue')
    # ax2.set_yticks(range(0, 1600, 500))
    st.pyplot(fig)
    st.set_option('deprecation.showPyplotGlobalUse', False)

with col3:
    st.header('''Table with more insights on the products:''')
    st.dataframe(df_logistics)
    # fig, ax1 = plt.subplots(figsize=(5, 5))
    # ax1.hist(df_logistics["productline"], color='grey')
    # ax1.set_title('# Products')
    # ax1.set_ylabel('')
    # ax1.set_xlabel('')
    # st.pyplot(fig)