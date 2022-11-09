# import libraries

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
#import datetime
import mysql.connector 
import seaborn as sns

st.set_page_config(
    page_title="Streamlit",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

connection=mysql.connector.connect(user = 'toyscie', password = 'WILD4Rdata!', host = '51.68.18.102', port = '23456', database = 'toys_and_models')


query_hr= '''WITH top_sellers AS (select e.employeeNumber, e.firstname, jobTitle, e.lastname, DATE_FORMAT(o.orderdate, "%c %Y") as DateOrd, year(o.orderdate) as YearOrd, month(o.orderdate) as month_,sum(od.quantityordered*od.priceeach) as highest_turnover,
RANK() OVER (PARTITION BY DateOrd ORDER BY highest_turnover DESC) sell_rank from employees e
join customers c on e.employeeNumber=c.salesRepEmployeeNumber
join orders o on c.customerNumber=o.customerNumber
join orderdetails od on o.orderNumber=od.orderNumber
WHERE jobTitle like 'Sales Rep%' and o.status <> 'Cancelled'
Group by DateOrd, employeeNumber
Order by DateOrd, highest_turnover DESC)
select * from top_sellers
where sell_rank=1 or sell_rank=2;'''

df_hr = pd.read_sql(query_hr, con=connection)
df_hr.head(53)
df_hr = df_hr[df_hr['YearOrd'] == 2021]
print(df_hr)

st.title('''Sellers Ranking 2021 🏆 ''')

col1, col2, col3 = st.columns([2, 1, 3])

with col1:
    st.subheader('''Best sellers per month in 2021:''')
    df_hr = pd.read_sql(query_hr, con=connection)
    df_hr = df_hr[df_hr['YearOrd'] == 2021]
    df_hrv2 = df_hr.loc[:, ["month_", "firstname", "lastname", "sell_rank", "highest_turnover","DateOrd"]]
    df_hrv3 = df_hrv2.sort_values(by=["month_", "sell_rank"], ascending=True)
    st.dataframe (df_hrv3, 450, 600)
    
with col2:
    st.title('' '')
    
with col3:
    st.subheader('''Sales difference beetween the TOP 2 sellers:''')
    st.info('Information related to the year 2021')
    df_hr = pd.read_sql(query_hr, con=connection)
    df_hr = df_hr[df_hr['YearOrd'] == 2021]
    df_hrv2 = df_hr.loc[:, ["month_", "firstname", "lastname", "sell_rank", "highest_turnover","DateOrd"]]
    df_hrv3 = df_hrv2.sort_values(by=["month_", "sell_rank"], ascending=True)
    
    fig, axes = plt.subplots(figsize=(10,4))
    colors=['grey', 'black']
    sns.barplot(data=df_hrv3, x="DateOrd", y="highest_turnover", hue="sell_rank", ci=None, palette=colors).set(title='Top 2 sellers with the highest turnover')
    axes.set_xlabel("Month")
    axes.set_ylabel("Turnover")
    axes.legend(title="Sell Rank: ")
    st.pyplot(fig)
