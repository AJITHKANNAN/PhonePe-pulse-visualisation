

# # Data Extraction

# # Cloning Data from Github


import pandas as pd
import mysql.connector as sql
import streamlit as st
import plotly.express as px
import os
import json
from streamlit_option_menu import option_menu
from PIL import Image


# """
# import git
# 
# from git import *
# 
# 
# cloning =Repo.clone_from('https://github.com/PhonePe/pulse.git',"E:\PPV")
# """



# # Data Transformation
# # Dataframe of aggregated Transactions

data_path1 = "E:/PPV/data/aggregated/transaction/country/india/state/"

aggregated_trans_list = os.listdir(data_path1)

col1 = {'State': [], 'Year': [], 'Quarter': [], 'Transaction_type': [], 'Transaction_count': [],
            'Transaction_amount': []}

aggregated_trans_list = os.listdir(data_path1)

for state in aggregated_trans_list:
    current_state = data_path1 + state + "/"
    aggregated_year_list = os.listdir(current_state)
    
    for year in aggregated_year_list:
        current_year = current_state + year + "/"
        aggregated_file_list = os.listdir(current_year)

        for file in aggregated_file_list:
            current_file = current_year + file
            data = open(current_file, 'r')
            AT = json.load(data)
            
            for i in AT['data']['transactionData']:
                name = i['name']
                count = i['paymentInstruments'][0]['count']
                amount = i['paymentInstruments'][0]['amount']
                col1['Transaction_type'].append(name)
                col1['Transaction_count'].append(count)
                col1['Transaction_amount'].append(amount)
                col1['State'].append(state)
                col1['Year'].append(year)
                col1['Quarter'].append(int(file.strip('.json')))
                
df_aggre_trans = pd.DataFrame(col1)
df_aggre_trans          
      


# # Dataframe of aggregated user


data_path2 = "E:/PPV/data/aggregated/user/country/india/state/"


aggregated_user_list = os.listdir(data_path2)

col2 = {'State': [], 'Year': [], 'Quarter': [], 'Brands': [], 'Count': [],
            'Percentage': []}

for state in aggregated_user_list:
    current_state = data_path2 + state + "/"
    aggregated_year_list = os.listdir(current_state)
    
    for year in aggregated_year_list:
        current_year = current_state + year + "/"
        aggregated_file_list = os.listdir(current_year)

        for file in aggregated_file_list:
            current_file = current_year + file
            data = open(current_file, 'r')
            AU = json.load(data)
            try:
                for i in AU["data"]["usersByDevice"]:
                    brand_name = i["brand"]
                    counts = i["count"]
                    percents = i["percentage"]
                    col2["Brands"].append(brand_name)
                    col2["Count"].append(counts)
                    col2["Percentage"].append(percents)
                    col2["State"].append(state)
                    col2["Year"].append(year)
                    col2["Quarter"].append(int(file.strip('.json')))
            except:
                pass
            
df_aggre_users = pd.DataFrame(col2)
df_aggre_users
             


# # Dataframe of map transactions



data_path3 = "E:/PPV/data/map/transaction/hover/country/india/state/"

map_trans_list = os.listdir(data_path3)

col3 = {'State': [], 'Year': [], 'Quarter': [], 'District': [], 'Count': [], 'Amount': []}

for state in map_trans_list:
    current_state = data_path3 + state + "/"
    map_year_list = os.listdir(current_state)
    
    for year in map_year_list:
        current_year = current_state + year + "/"
        map_file_list = os.listdir(current_year)
        
        for file in map_file_list:
            current_file = current_year + file
            data = open(current_file, 'r')
            MT = json.load(data)
            
            for i in MT["data"]["hoverDataList"]:
                district = i["name"]
                count = i["metric"][0]["count"]
                amount = i["metric"][0]["amount"]
                col3["District"].append(district)
                col3["Count"].append(count)
                col3["Amount"].append(amount)
                col3['State'].append(state)
                col3['Year'].append(year)
                col3['Quarter'].append(int(file.strip('.json')))
                

df_map_trans = pd.DataFrame(col3)
df_map_trans


# # Dataframe of map user


data_path4 = "E:/PPV/data/map/user/hover/country/india/state/"

map_user_list = os.listdir(data_path4)

col4 = {"State": [], "Year": [], "Quarter": [], "District": [],
            "RegisteredUser": [], "AppOpens": []}

for state in map_user_list:
    current_state = data_path4 + state + "/"
    map_year_list = os.listdir(current_state)
    
    for year in map_year_list:
        current_year = current_state + year + "/"
        map_file_list = os.listdir(current_year)
        
        for file in map_file_list:
            current_file = current_year + file
            data = open(current_file, 'r')
            MU = json.load(data)
            
            for i in MU["data"]["hoverData"].items():
                district = i[0]
                registereduser = i[1]["registeredUsers"]
                appOpens = i[1]['appOpens']
                col4["District"].append(district)
                col4["RegisteredUser"].append(registereduser)
                col4["AppOpens"].append(appOpens)
                col4['State'].append(state)
                col4['Year'].append(year)
                col4['Quarter'].append(int(file.strip('.json')))
                
df_map_user = pd.DataFrame(col4)
df_map_user


# # Dataframe of top transactions




data_path5 = "E:/PPV/data/top/transaction/country/india/state/"

top_trans_list = os.listdir(data_path5)
col5 = {'State': [], 'Year': [], 'Quarter': [], 'Pincode': [], 'Transaction_count': [],
            'Transaction_amount': []}
for state in top_trans_list:
    current_state = data_path5 + state + "/"
    top_year_list = os.listdir(current_state)
    
    for year in top_year_list:
        current_year = current_state + year + "/"
        top_file_list = os.listdir(current_year)
        
        for file in top_file_list:
            current_file = current_year + file
            data = open(current_file, 'r')
            TT = json.load(data)
            
            for i in TT['data']['pincodes']:
                name = i['entityName']
                count = i['metric']['count']
                amount = i['metric']['amount']
                col5['Pincode'].append(name)
                col5['Transaction_count'].append(count)
                col5['Transaction_amount'].append(amount)
                col5['State'].append(state)
                col5['Year'].append(year)
                col5['Quarter'].append(int(file.strip('.json')))


df_top_trans = pd.DataFrame(col5)
            
df_top_trans


# # Dataframe of top users


data_path6 = "E:/PPV/data/top/user/country/india/state/"

top_user_list = os.listdir(data_path6)
col6 = {'State': [], 'Year': [], 'Quarter': [], 'Pincode': [], 'RegisteredUsers': []}

for state in top_user_list:
    current_state = data_path6 + state + "/"
    top_year_list = os.listdir(current_state)
    
    for year in top_year_list:
        current_year = current_state + year + "/"
        top_file_list = os.listdir(current_year)
        
        for file in top_file_list:
            current_file = current_year + file
            data = open(current_file, 'r')
            TU = json.load(data)
            
            for i in TU['data']['pincodes']:
                name = i['name']
                registeredUsers = i['registeredUsers']
                
                col6['Pincode'].append(name)
                col6['RegisteredUsers'].append(registeredUsers)
                col6['State'].append(state)
                col6['Year'].append(year)
                col6['Quarter'].append(int(file.strip('.json')))
df_top_user = pd.DataFrame(col6)         
df_top_user



# # Converting Dataframes to CSV files

df_aggre_trans.to_csv('agg_trans.csv',index=False)
df_aggre_users.to_csv('agg_user.csv',index=False)
df_map_trans.to_csv('map_trans.csv',index=False)
df_map_user.to_csv('map_user.csv',index=False)
df_top_trans.to_csv('top_trans.csv',index=False)
df_top_user.to_csv('top_user.csv',index=False)


# # Creating connection with MySQL

# # Connecting with SQL





mydb = sql.connect(host="localhost",
                                user="root",
                                password="AjithatML6",
                                database= "phonepe_pulse" )
mycursor = mydb.cursor(buffered=True)

"""
# #Creating a new Database and tables
# 
# #mycursor.execute("CREATE DATABASE phonepe_pulse")

# # Creating agg_trans table

mycursor.execute("create table agg_trans (State varchar(100), Year int, Quarter int, Transaction_type varchar(100), Transaction_count int, Transaction_amount double)")

for i,row in df_aggre_trans.iterrows():
    #here %S means string values 
    sql = "INSERT INTO agg_trans VALUES (%s,%s,%s,%s,%s,%s)"
    mycursor.execute(sql, tuple(row))
    # the connection is not auto committed by default, so we must commit to save our changes
    mydb.commit()


# # Creating agg_user table

mycursor.execute("create table agg_user (State varchar(100), Year int, Quarter int, Brands varchar(100), Count int, Percentage double)")

for i,row in df_aggre_users.iterrows():
    sql = "INSERT INTO agg_user VALUES (%s,%s,%s,%s,%s,%s)"
    mycursor.execute(sql, tuple(row))
    mydb.commit()


# # Creating map_trans table

mycursor.execute("create table map_trans (State varchar(100), Year int, Quarter int, District varchar(100), Count int, Amount double)")

for i,row in df_map_trans.iterrows():
    sql = "INSERT INTO map_trans VALUES (%s,%s,%s,%s,%s,%s)"
    mycursor.execute(sql, tuple(row))
    mydb.commit()


# # Creating map_user table


mycursor.execute("create table map_user (State varchar(100), Year int, Quarter int, District varchar(100), Registered_user int, App_opens int)")

for i,row in df_map_user.iterrows():
    sql = "INSERT INTO map_user VALUES (%s,%s,%s,%s,%s,%s)"
    mycursor.execute(sql, tuple(row))
    mydb.commit()


# # Creating top_trans table



mycursor.execute("create table top_trans (State varchar(100), Year int, Quarter int, Pincode int, Transaction_count int, Transaction_amount double)")

for i,row in df_top_trans.iterrows():
    sql = "INSERT INTO top_trans VALUES (%s,%s,%s,%s,%s,%s)"
    mycursor.execute(sql, tuple(row))
    mydb.commit()


# # Creating top_user table
# 


mycursor.execute("create table top_user (State varchar(100), Year int, Quarter int, Pincode int, Registered_users int)")

for i,row in df_top_user.iterrows():
    sql = "INSERT INTO top_user VALUES (%s,%s,%s,%s,%s)"
    mycursor.execute(sql, tuple(row))
    mydb.commit()


# # List of tables


mycursor.execute("show tables")
mycursor.fetchall()




# Migrating data from dataframe to SQL
        
# mysql+mysqlconnector://user1:pscale_pw_abc123@us-east.connect.psdb.cloud:3306/sqlalchemy

# 'mysql://dt_admin:dt2016@localhost:3308/dreamteam_db'
# ("mysql+mysqlconnector://user:password@host/database")


    engine = sqlalchemy.create_engine('mysql://root:AjithatML6@127.0.0.1:3306/youtube_db3')
    
    try:
        # Migrating channel details into channel table
        ch_df.to_sql('ychannel2', engine, if_exists='append', index=False)

        # Migrating playlist details into playlist table
        pl_df.to_sql('yplaylist2', engine, if_exists='append', index=False)

        # Migrating video details into video table
        vdo_df.to_sql('yvideo2', engine, if_exists='append', index=False)

        # Migrating comment details into comment table
        cmt_df.to_sql('ycomment2', engine, if_exists='append', index=False)
        return 1
    except IntegrityError:
        return 0
"""

