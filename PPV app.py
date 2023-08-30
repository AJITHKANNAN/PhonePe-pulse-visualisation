

# Importing Libraries
import pandas as pd
import mysql.connector as sql
import streamlit as st
import plotly.express as px
import os
import json
from streamlit_option_menu import option_menu
from PIL import Image
from git.repo.base import Repo
import plotly.graph_objects as go



# Setting up page configuration

st.set_page_config(page_title= "Phonepe Pulse Data Visualization ",                   
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   #menu_items={'About': """ Data has been cloned from Phonepe Pulse Github Repo"""}
                   )

st.sidebar.header(""" :wave: Hai Guys, 
     Hope you all are Good! 
     Welcome to Phonepe Pulse 
     Visualisation dashboard """)

# #To clone the Github Pulse repository use the following code
# Reference Syntax - Repo.clone_from("Clone Url", "Your working directory")
# Repo.clone_from("https://github.com/PhonePe/pulse.git", "E:\Phonepe pulse")

# Creating connection with mysql workbench
mydb = sql.connect(host="localhost",
                                user="root",
                                password="AjithatML6",
                                database= "phonepe_pulse" )
mycursor = mydb.cursor(buffered=True)



# Creating option menu in the side bar
with st.sidebar:
    selected = option_menu("Menu", ["Home","Top Charts","Explore Data","About"], 
                icons=["house","graph-up-arrow","bar-chart-line", "exclamation-circle"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})
# MENU 1 - HOME
if selected == "Home":
    
    st.header("---------------------Phonepe Pulse Data Visualization---------------------")
    
    col1, col2, col3 = st.columns(3)
    col2.image("pp_logo.jpg", width=250)
    #st.image("pp_logo.jpg", width= 250)
    
    st.header(" Overview : ")
    st.write(""" You can visualise the phonepe pulse data in this streamlit web app and gain a lot of insights on transactions, 
             number of users, top 10 state, district, pincode, and which brand has the most users, and more.""")
    st.write("Bar charts, Pie charts and Geo map visualization are used to get some insights")
      
    st.header(" Data Visualization and Exploration  ")
    st.markdown(""" We have used Phonepe pulse API data from github to explore and visualize the Phonepe company's performance.
                For that we have created an user-friendly web app by using Streamlit and Plotly """)
    
    #st.write(" ")
   
    st.header(" Domain : ")
    st.markdown(" FINTECH")
    st.header(" Technologies used :  ")
    st.write("1. Github Cloning")
    st.write("2. Python")
    st.write("3. Pandas")
    st.write("4. MySQL")
    st.write("5. mysql-connector-python")
    st.write("6. Streamlit")
    st.write("7. Plotly")
      
# MENU 2 - TOP CHARTS
if selected == "Top Charts":
    st.header(" Top Charts ")
    Type = st.sidebar.selectbox("TYPE ", ("Transactions", "Users"))
    column1,column2= st.columns([1,1.5],gap="medium")
    with column1:
        Year = st.slider("Year", min_value=2018, max_value=2023)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)
    
    with column2:
        st.info(
                """
                #### From this menu we can get insights like :
                - Overall ranking on a particular Year and Quarter.
                - Top 10 State, District, Pincode based on Total number of transaction and Total amount spent on phonepe.
                - Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.
                
                """,icon="🔍"
                )
        
# Top Charts - TRANSACTIONS    
    if Type == "Transactions":
        col1,col2 = st.columns([1,1],gap="medium")
        
        with col1:
            st.header(" State ")
            mycursor.execute(f"select state, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from agg_trans where year = {Year} and quarter = {Quarter} group by state order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transactions_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                             names='State',
                             title='Top 10 States',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with col2:
            st.header(" District ")
            mycursor.execute(f"select district , sum(Count) as Total_Count, sum(Amount) as Total from map_trans where year = {Year} and quarter = {Quarter} group by district order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Transactions_Count','Total_Amount'])

            fig = px.pie(df, values='Total_Amount',
                             names='District',
                             title='Top 10 District',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'}, width = 1000)

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
    
    if Type == "Transactions":
                
        st.header(" Pincode ")
        mycursor.execute(f"select pincode, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from top_trans where year = {Year} and quarter = {Quarter} group by pincode order by Total desc limit 10")
        df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Transactions_Count','Total_Amount'])
        fig = px.pie(df, values='Total_Amount',
                            names='Pincode',
                            title='Top 10 Pincode',
                            color_discrete_sequence=px.colors.sequential.Agsunset,
                            hover_data=['Transactions_Count'],
                            labels={'Transactions_Count':'Transactions_Count'})
        

        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig,use_container_width=True)
            
# Top Charts - USERS          
    if Type == "Users":
        col1,col2 = st.columns([1,1],gap="medium")
        
        with col1:
            st.header(" Brands ")
            if Year == 2023 and Quarter in [1,2,3,4]:
                st.header(" Sorry there is NO brand Data available for 2023  ")
            else:
                mycursor.execute(f"select brands, sum(count) as Total_Count, avg(percentage)*100 as Avg_Percentage from agg_user where year = {Year} and quarter = {Quarter} group by brands order by Total_Count desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
                fig = px.bar(df,
                             title='Top 10 Brands',
                             x="Total_Users",
                             y="Brand",
                             orientation='h',
                             color='Avg_Percentage',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig,use_container_width=True)   
    
        with col2:
            st.header(" District ")
            mycursor.execute(f"select district, sum(Registered_User) as Total_Users, sum(app_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by district order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users','Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                         title='Top 10 District',
                         x="Total_Users",
                         y="District",
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            

            st.plotly_chart(fig,use_container_width=True)
            
    if Type == "Users":
        col3,col4 = st.columns([1,1],gap="medium")
                 
        with col3:
            st.header(" Pincode ")
            mycursor.execute(f"select Pincode, sum(Registered_Users) as Total_Users from top_user where year = {Year} and quarter = {Quarter} group by Pincode order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Total_Users'])
            fig = px.pie(df,
                         values='Total_Users',
                         names='Pincode',
                         title='Top 10 Pincode',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Total_Users'])
            fig.update_layout(shapes=[go.layout.Shape(
                                type='rect',
                                xref='paper',
                                yref='paper',
                                x0=0,
                                y0=-0.1,
                                x1=1.01,
                                y1=1.02,
                                line={'width': 1, 'color': 'black'}
                            )])

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with col4:
            st.header(" State ")
            mycursor.execute(f"select state, sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
            fig = px.pie(df, values='Total_Users',
                             names='State',
                             title='Top 10 States',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Total_Appopens'],
                             labels={'Total_Appopens':'Total_Appopens'})
            fig.update_layout(shapes=[go.layout.Shape(
                                type='rect',
                                xref='paper',
                                yref='paper',
                                x0=0,
                                y0=-0.1,
                                x1=1.01,
                                y1=1.02,
                                line={'width': 1, 'color': 'black'}
                            )])


            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
# MENU 3 - EXPLORE DATA
if selected == "Explore Data":
    Year = st.sidebar.slider(" Year ", min_value=2018, max_value=2023)
    Quarter = st.sidebar.slider("Quarter", min_value=1, max_value=4)
    Type = st.sidebar.selectbox(" Type ", ("Transactions", "Users"))
    col1,col2 = st.columns(2)
    
# EXPLORE DATA - TRANSACTIONS
    if Type == "Transactions":
        
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
        with col1:
            st.header(" Overall State Data - Transactions Total AMOUNT")
            mycursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv('dataframes\Statenames.csv') #dataframes\Statenames.csv
            df1.State = df2

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_amount',
                      color_continuous_scale='sunset', width=1500, height=400)
            fig.update_layout(shapes=[go.layout.Shape(
                                type='rect',
                                xref='paper',
                                yref='paper',
                                x0=0,
                                y0=-0.1,
                                x1=1.01,
                                y1=1.02,
                                line={'width': 1, 'color': 'black'}
                            )])


            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
            
        # Overall State Data - TRANSACTIONS COUNT - INDIA MAP
        with col2:
            
            st.header(" Overall State Data - Transactions Total COUNT")
            mycursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv('dataframes\Statenames.csv')
            df1.Total_Transactions = df1.Total_Transactions.astype(int) 
            df1.State = df2 

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_Transactions',
                      color_continuous_scale='sunset', width=1500, height=400)

            fig.update_layout(shapes=[go.layout.Shape(
                                type='rect',
                                xref='paper',
                                yref='paper',
                                x0=0,
                                y0=-0.1,
                                x1=1.01,
                                y1=1.02,
                                line={'width': 1, 'color': 'black'}
                            )])

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
            
            
            
# BAR CHART - TOP PAYMENT TYPE
        st.header(" Top Payment Type ")
        mycursor.execute(f"select Transaction_type, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from agg_trans where year= {Year} and quarter = {Quarter} group by transaction_type order by Transaction_type")
        df = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_type', 'Total_Transactions','Total_amount'])

        fig = px.bar(df,
                     title='Transaction Types vs Total_Transactions',
                     x="Transaction_type",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        fig.update_layout(shapes=[go.layout.Shape(
                                type='rect',
                                xref='paper',
                                yref='paper',
                                x0=0,
                                y0=-0.1,
                                x1=1.01,
                                y1=1.02,
                                line={'width': 1, 'color': 'black'}
                            )])


        st.plotly_chart(fig,use_container_width=True)
        
# BAR CHART TRANSACTIONS - DISTRICT WISE DATA            
        st.header("# ")
        st.header("# ")
        st.header("# ")
        st.header(" Select any State to explore more ")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
         
        mycursor.execute(f"select State, District,year,quarter, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} and State = '{selected_state}' group by State, District,year,quarter order by state,district")
        
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State','District','Year','Quarter',
                                                         'Total_Transactions','Total_amount'])
        fig = px.bar(df1,
                     title=selected_state,
                     x="District",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=  'sunset')
        #color_continuous_scale='sunset',
     

        st.plotly_chart(fig,use_container_width=True)
        
# EXPLORE DATA - USERS      
    if Type == "Users":
        
        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.header(" Overall State Data - User App opening frequency ")
        mycursor.execute(f"select state, sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by state")
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
        df2 = pd.read_csv('Statenames.csv')
        df1.Total_Appopens = df1.Total_Appopens.astype(float)
        df1.State = df2
        
        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                  featureidkey='properties.ST_NM',
                  locations='State',
                  color='Total_Appopens',
                  color_continuous_scale='sunset', width=1500, height=400)
        fig.update_layout(shapes=[go.layout.Shape(
                                type='rect',
                                xref='paper',
                                yref='paper',
                                x0=0,
                                y0=-0.1,
                                x1=1.01,
                                y1=1.02,
                                line={'width': 1, 'color': 'black'}
                            )])


        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)
        
        # BAR CHART TOTAL UERS - DISTRICT WISE DATA 
        st.header(" Select any State to explore more" )
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
        
        mycursor.execute(f"select State,year,quarter,District,sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} and state = '{selected_state}' group by State, District,year,quarter order by state,district")
        
        df = pd.DataFrame(mycursor.fetchall(), columns=['State','year', 'quarter', 'District', 'Total_Users','Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(int)
        
        fig = px.bar(df,
                     title=selected_state,
                     x="District",
                     y="Total_Users",
                     orientation='v',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        

        st.plotly_chart(fig,use_container_width=True)

    

# MENU 4 - ABOUT
if selected == "About":
    
    
    st.write(" ")
    st.write(" ")
    
    st.header(" About PhonePe Pulse: ")
    st.write(" PhonePe Pulse is India's go-to destination for accurate and comprehensive data on digital payment trends.   The Pulse website reveals digital transaction habits of over 300 Mn Indians at a district level. The Pulse report is a 'state of the union' in-depth view on the Indian digital payments industry ")

    st.write(" To Know more about  Phonepe Pulse please visit to the URL:  https://www.prnewswire.com/in/news-releases/phonepe-launches-the-pulse-of-digital-payments-india-s-first-interactive-geospatial-website-888262738.html")
    st.write(" ")
    st.write(" ")
    st.header("About PhonePe: ")
    st.write(" PhonePe is an Indian digital payments and financial services company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016.	The PhonePe app is available in 11 Indian languages. Using PhonePe, users can send and receive money, recharge mobile, DTH, data cards, make utility payments, pay at shops, invest in tax saving funds, liquid funds, buy insurance, mutual funds, and digital gold. ")
	
    st.write(" To Know more about Phonepe, please visit to the URL: https://en.wikipedia.org/wiki/PhonePe ")
    st.write(" ")
    st.write(" ")
    st.header(" Phonepe pulse Project GitHub link ")
    st.write(" https://github.com/AJITHKANNAN/PhonePe-pulse-visualisation ")
    

