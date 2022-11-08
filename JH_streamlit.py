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

#Table with contact info

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
    

query_logistics = '''select sum(products.quantityInStock), products.productName
from products
join orderdetails
on products.productCode = orderdetails.productCode
join orders
on orderdetails.orderNumber = orders.orderNumber
where not orders.status ='Cancelled'
group by products.productName
order by sum(orderdetails.quantityOrdered) desc limit 0,5'''

#Query 1 - Show the best sellers since the last 3 months

query1_hr = '''with top_sellers as (select employeeNumber, lastName, firstName, jobTitle, sum(priceEach*quantityOrdered) as final_amount,
 DATE_FORMAT(orders.orderdate, "%m %Y") as date_true, rank() over (partition by date_true order by final_amount desc) price_rank from employees
join customers
on employees.employeeNumber=customers.salesRepEmployeeNumber
join orders
on orders.customerNumber=customers.customerNumber
join orderdetails
on orders.orderNumber=orderdetails.orderNumber
where jobTitle like 'Sales Rep%' and orders.status <> 'Cancelled'
group by date_true, employees.employeeNumber
order by date_true, final_amount desc)
select concat(firstName, ' ', lastName) as Sellers, employeeNumber, final_amount, date_true, price_rank
from top_sellers
having price_rank=1 or price_rank=2;'''

# Query 2 HR 

query2_hr = '''with top_sellers as (select employeeNumber, lastName, firstName, jobTitle, sum(priceEach*quantityOrdered) as final_amount,
 DATE_FORMAT(orders.orderdate, "%m %Y") as date_true, rank() over (partition by date_true order by final_amount desc) as Ranking from employees
join customers
on employees.employeeNumber=customers.salesRepEmployeeNumber
join orders
on orders.customerNumber=customers.customerNumber
join orderdetails
on orders.orderNumber=orderdetails.orderNumber
where jobTitle like 'Sales Rep%' and orders.status <> 'Cancelled'
group by date_true, employees.employeeNumber
order by date_true, final_amount desc)
select concat(firstName, ' ', lastName) as Sellers, count(Ranking) as Recurring_best_sellers from top_sellers
where ranking=1
group by lastname
order by count(ranking) desc;'''

connection2 = mysql.connector.connect(user = 'toyscie', password = 'WILD4Rdata!', host = '51.68.18.102', port = '23456', database = 'toys_and_models')    
#connection3 = mysql.connector.connect(user = 'toyscie', password = 'WILD4Rdata!', host = '51.68.18.102', port = '23456', database = 'toys_and_models')
#connection = 'mysql://toyscie:WILD4Rdata!@51.68.18.102:23456/toys_and_models'
#sql_engine = sql.create_engine(connection) 

 
dffin = pd.read_sql_query(query_fin, con=connection2)    
#dffin2 = pd.read_sql_query(query_fin2, con=connection2)
#dffin2['customerNumber'] = dffin2['customerNumber'].astype(str)        
dffin3 = pd.read_sql_query(query_fin3, con=connection2)
#dffin3.set_index('Customer_Number', drop = True)    
dfSales = pd.read_sql(query_sales, con=connection2)
dfLog = pd.read_sql_query(query_logistics, con=connection2)    
dffin_1 = pd.read_sql_query(query1_hr, con=connection2)
dffin_2 = pd.read_sql_query(query2_hr, con=connection2)



primaryColor = '#77FFE3'
color = ['lightgreen','mediumseagreen','seagreen']

#color1 = sns.color_palette("light:#5A9", as_cmap=True)
#colors1 = sns.color_palette('Paired')[0:7]

st.set_page_config(
    page_title="Sales",
    page_icon=":sac_d'argent:",
    layout="wide",
    )

# Query 1 plot
#if add_selectbox == 'Intro':
st.title('Vintage Cars Sales Challenge!🚗💰')

#image = Image.open('/Users/anacarolinaquintino/Downloads/Model.jpg')
#st.image(image)

#st.subheader('What does data tell us?')

#image1 = Image.open('Images/vintage_car.png')
#st.image(image1)

#elif add_selectbox == 'Finance':

#fig2, ax = plt.subplots(figsize = (5, 5)) 
#sns.barplot(data=dffin2, x='customerNumber', y="to_be_paid", color='b')
#ax.set_ylabel('Amount to be paid')
#ax.set_xlabel('Customer Number')
#ax.set_title('Which clients do we have to chase?')
#plt.legend(loc='upper left')
#st.pyplot(fig2)

data2020 = dfSales[dfSales['order_year']==2020].groupby('productline').total_orders.sum()
dataAll = dfSales.groupby('productline').total_orders.sum()
labels = ['Classic Cars', 'Motorcycles', 'Planes', 'Ships', 'Trains',
        'Trucks and Buses', 'Vintage Cars']

#define Seaborn color palette
colors = sns.color_palette('Greens')[0:5]
colors1 = sns.color_palette('Paired')[0:7]


#sns.boxplot(x=dffin3["age"])

col1, col2, col3 = st.columns(3)

with col1:
    st.header('Which is the most important category? 📦')
   # st.image("https://static.streamlit.io/examples/cat.jpg")
    #st.subheader('*Which is the most important category?*')

    fig05, ax = plt.subplots(figsize = (10,2))
    plt.pie(dataAll, labels = labels, colors = colors, autopct='%.0f%%', textprops={'fontsize': 4})
    #plt.yticks(fontsize=10)
    st.pyplot(fig05)
    st.subheader('')

with col2:
    st.header("How are categories growing on a YoY basis?💲")
    options = st.selectbox('Choose the type of product:', dfSales['productline'].unique())
    fig07, ax = plt.subplots(figsize = (10, 5))
    colors = sns.color_palette('Greens')[5]
    sns.barplot(data=dfSales[dfSales['productline']==options], x='order_month', y="total_orders", hue="order_year", palette =color, ci=None)
    ax.set_ylabel('Orders')
    ax.set_xlabel('Month')
    ax.set_title('Monthly order growth by category')
    ax.get_yaxis().set_major_formatter(mtick.FuncFormatter(lambda x, p: format(int(x), ',')))
    plt.legend(loc='upper right', title='Year')
    st.pyplot(fig07)

with col3:
    st.header("Best sellers for Vintage Cars👩‍💻")
    options = st.selectbox('Choose the month:', dffin_1['date_true'].unique())
    #['Classic Cars', 'Vintage Cars', 'Planes', 'Motorcycles','Ships','Trains','Trucks and Buses'])
    df_HR=dffin_1[dffin_1['date_true']==options][['Sellers','final_amount']]
    hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    st.table(df_HR)


col4, col5, col6 = st.columns(3)

with col4:
    st.header("💻[REMEMBER] Update your new deal on the CRM: https://dynamics.microsoft.com/en-us/digital-commerce-solution/")

with col6:
    image3 = Image.open("C:/Users/hanau/Downloads/vintage_car.png")
    st.image(image3)


   #st.image("https://static.streamlit.io/examples/dog.jpg")

   #st.image("https://static.streamlit.io/examples/owl.jpg")



#dfSales[dfSales['productline']=='Classic Cars']
#st.subheader('*How are categories growing on a YoY basis?*')







