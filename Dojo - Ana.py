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


#[theme]
#primaryColor="#F63366"
#backgroundColor="#FFFFFF"
#secondaryBackgroundColor="#F0F2F6"
#textColor="#262730"
#font="sans serif"



#Query 1 - Define turnover of countries of last 2 months

#query_fin1 = '''select customers.country, month(orders.orderDate) as 'Month', sum(orderdetails.quantityOrdered*orderdetails.priceEach) as Turnover
#from orders
#join orderdetails
#on orderdetails.orderNumber = orders.orderNumber
#join customers
#on orders.customerNumber = customers.customerNumber
#where status <>'Cancelled' and orders.orderDate>=date_sub(curdate(), interval 2 month)
#group by Turnover;'''


query_fin = '''select customers.country, month(orders.orderDate) as 'Month', sum(orderdetails.quantityOrdered*orderdetails.priceEach) as Turnover
from orders
join orderdetails
on orderdetails.orderNumber = orders.orderNumber
join customers
on orders.customerNumber = customers.customerNumber
where status <>'Cancelled' and orders.orderDate>=date_sub(curdate(), interval 2 month)
group by country, monthname(orders.orderDate) desc;'''

#dffin

#query_fin2 = '''with amount_ordered as (select orders.customerNumber, sum(orderdetails.priceEach*orderdetails.quantityOrdered) as final_ordered from orderdetails
#join orders
#on orders.orderNumber = orderdetails.orderNumber
#group by orders.customerNumber -- did not include status <> 'Cancelled' because the difference is negative for some, might mean that order was partially cancelled and part of it was paid
#order by orders.customerNumber),
#amount_paid as (select payments.customerNumber, sum(payments.amount) as final_paid from payments
#group by payments.customerNumber
#order by customerNumber)
#select amount_ordered.customerNumber, final_ordered, final_paid, final_ordered-final_paid as to_be_paid from amount_paid
#join amount_ordered
#on amount_ordered.customerNumber = amount_paid.customerNumber
#having to_be_paid <> 0
#order by to_be_paid desc;'''


#Contact information of the clients overdue
query_fin3='''with amount_ordered as (select orders.customerNumber, sum(orderdetails.priceEach*orderdetails.quantityOrdered) as final_ordered, count(orders.orderNumber) as Nb_orders from orderdetails
join orders
on orders.orderNumber = orderdetails.orderNumber
group by orders.customerNumber -- did not include status <> 'Cancelled' because the difference is negative for some, might mean that order was partially cancelled and part of it was paid
order by orders.customerNumber),
amount_paid as (select payments.customerNumber, sum(payments.amount) as final_paid from payments
group by payments.customerNumber
order by customerNumber)
select amount_ordered.customerNumber as Customer_Number, customers.customerName as Customer_Name, customers.country as Country, final_ordered-final_paid as Outstanding_payment from amount_paid
join amount_ordered
on amount_ordered.customerNumber = amount_paid.customerNumber
join customers
on customers.customerNumber=amount_paid.customerNumber
having Outstanding_payment <> 0
order by Outstanding_payment desc
;'''

connection2 = mysql.connector.connect(user = 'toyscie', password = 'WILD4Rdata!', host = '51.68.18.102', port = '23456', database = 'toys_and_models')    

dffin = pd.read_sql_query(query_fin, con=connection2)    
#dffin1 = pd.read_sql_query(query_fin1, con=connection2)
#dffin2['customerNumber'] = dffin2['customerNumber'].astype(str)        
dffin3 = pd.read_sql_query(query_fin3, con=connection2)
#dffin3.set_index('Customer_Number', drop = True)       

primaryColor = '#77FFE3'
color = ['lightgreen','mediumseagreen','seagreen']


st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

image1 = Image.open('Desktop/Screenshot 2022-11-08 at 16.04.56.png')
image1 = image1.resize((200, 100))
st.image(image1)

st.header('Financial Performance (8/Sep - 8/Nov)')
#st.markdown("<h1 style='text-align: center; color: Black;'>Financial Performance (8/Sep - 8/Nov)</h1>", unsafe_allow_html=True)

st.metric(label="Total Turnover", value="123,000", delta="-2%")

col1, col2, col3 = st.columns(3)


#with col1:
 #   st.text(' ')
    
#with col2:
 #   st.metric(label="Total Turnover", value="123,000", delta="-2%")

#with col3:
 #   st.text(' ')
    
col1, col2 = st.columns(2)

with col1:
    #st.subheader('Total turnover')
    
    st.subheader('*Turnover per country*')
    fig1, ax = plt.subplots(figsize = (10, 5))
    sns.barplot(data=dffin, x='country', y="Turnover", hue="Month", palette =color, ci=None)
    ax.set_ylabel('Turnover')
    ax.set_xlabel('Country')
    ax.set_title('Turnover per country over the past 2 months')
    ax.get_yaxis().set_major_formatter(mtick.FuncFormatter(lambda x, p: format(int(x), ',')))
    plt.legend(loc='upper left', title='Month')
    st.pyplot(fig1)

with col2:
    
    
    st.subheader('*Clients with payments outstanding*')
    #st.text('List of clients with outstanding payments')  
    hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    st.table(dffin3.head(5).style.format({'Outstanding_payment': '{:.2f}'})) 
    