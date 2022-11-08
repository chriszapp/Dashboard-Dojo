import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
#import sqlalchemy as sql
import datetime
import mysql.connector
from PIL import Image 

query_sales = '''with productline_sales as (
select productLine,
month(orderDate) order_month,
year(orderDate) order_year,
DATE_FORMAT(orderDate, "%M %Y") as month_year,
round(sum(quantityOrdered),0) total_orders
from orders
inner join orderdetails using (orderNumber)
inner join products using (productCode)
group by productLine, order_year, order_month
)
select productline,  total_orders, order_month, order_year, month_year, LAG(total_orders, 1) over (
partition by productLine, order_month
order by productLine, month_year
) prev_year_order_total , (((total_orders - (LAG(total_orders, 1) over (
partition by productLine, order_month
order by  productLine, month_year
)))/(LAG(total_orders, 1) over (
partition by productLine
order by  productLine, month_year ASC
))) *100) as growth
from productline_sales
order by  productLine, month_year'''
    
connection2 = mysql.connector.connect(user = 'toyscie', password = 'WILD4Rdata!', host = '51.68.18.102', port = '23456', database = 'toys_and_models')    
   
dfSales = pd.read_sql(query_sales, con=connection2)

st.set_page_config(page_title='Sales Monitoring Dashboard', page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

primaryColor = '#77FFE3'
color = ['lightgreen','mediumseagreen','seagreen']

st.title("Sales")
col1, col2, col3 = st.columns([2,1,3])

with col1:
   st.subheader("*Overall Business Overview*")
   data2020 = dfSales[dfSales['order_year']==2020].groupby('productline').total_orders.sum()
   dataAll = dfSales.groupby('productline').total_orders.sum()
   labels = ['Classic Cars', 'Motorcycles', 'Planes', 'Ships', 'Trains',
   'Trucks and Buses', 'Vintage Cars']
   colors = sns.color_palette('Greens')[0:5]
   colors1 = sns.color_palette('Paired')[0:7]
   fig05, ax = plt.subplots(figsize = (5,1))
   plt.pie(dataAll, labels = labels, colors = colors, autopct='%.0f%%', textprops={'fontsize': 4})
   st.pyplot(fig05)
   

   st.markdown("")

   st.subheader("*Growth by category*")
   fig01, ax = plt.subplots(figsize = (12,3))
   dfS = dfSales.groupby('productline').mean()
   ax.bar(dfS.index, dfS['growth'], color = 'mediumseagreen')
   ax.set_ylabel('Overall Growth in Orders')
   ax.set_xlabel('Product Lines')
   ax.set_title('Growth by category (all_dates)')
   fmt = '%.0f%%' 
   xticks = mtick.FormatStrFormatter(fmt) 
   ax.yaxis.set_major_formatter(xticks)
   st.pyplot(fig01)

with col2:
    st.title("")

with col3: 
    st.subheader('*How are categories growing on a YoY basis?*')
    options = st.selectbox('Choose the type of product:', dfSales['productline'].unique())
        
    fig07, ax = plt.subplots(figsize = (15, 10))
    sns.barplot(data=dfSales[dfSales['productline']==options], x='order_month', y="total_orders", hue="order_year", palette =color, ci=None)
    ax.set_ylabel('Orders')
    ax.set_xlabel('Month')
    ax.set_title('Monthly order growth by category')
    ax.get_yaxis().set_major_formatter(mtick.FuncFormatter(lambda x, p: format(int(x), ',')))
    plt.legend(loc='upper right', title='Year')
    st.pyplot(fig07)
