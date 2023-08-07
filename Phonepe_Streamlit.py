# Importing Neccessary libraries
import streamlit as st
import toml
import time
import mysql.connector
import pandas as pd
import plotly.express as px


# Setting Webpage Configurations
st.set_page_config(page_title="PhonePe", page_icon="🧭", layout="wide")

image = 'https://raw.githubusercontent.com/Sukumar9944/Phonpe-Pulse-Data-Visualization/main/Title_image/Phonepe%20Title.png'
st.image(image,width = 1050)

# MySQL Connection

secrets = toml.load('secrets.toml')
Password = secrets['secrets']["password"]

connection = mysql.connector.connect(
    host = "localhost",
    port=3306,
    user = "root",
    password = Password,
    database = "phonepe_data")

cursor = connection.cursor()

year = [2018,2019,2020,2021,2022]
quarter = [1,2,3,4]
type = ["Transaction","User"]

select_bar1,select_bar2,select_bar3 = st.columns(3)
with select_bar1:
    Type = st.selectbox("Select the type",options = type)
with select_bar2:
    Year = st.selectbox("Select a year",options = year)
with select_bar3:
    Quarter = st.selectbox("Select a Quarter",options = quarter)

tab1, tab2, tab3 = st.tabs(["Home Page","Live Geo-Data Visualization","Top Charts Data Analysis"])

with tab1:
    st.subheader(':violet[Welcome to our PhonePe Data Analytics Dashboard!]')
    st.markdown(':green[Explore, analyze, and visualize data like never before. Uncover insights and trends that empower smarter decision-making.]')
    st.subheader(':violet[Geo_Data Visualization!]')
    st.markdown(':green[Explore dynamic geodata visualization that brings your data to life on maps. Discover geographic trends and patterns with interactive maps that provide valuable insights into your data]')
    st.subheader(':violet[Interactive Charts!]')
    st.markdown(':green[Dive into information with interactive charts that transform numbers into visual stories. From bar graphs to pie charts, explore data from different angles.]')
    st.subheader(':violet[Top Questions Answered!]')
    st.caption(':green[Get instant answers to your top questions. Our dashboard provides key insights, addressing queries on demand, so you can make informed decisions swiftly.]')



with tab2:
    if Type == "Transaction":
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP - For Choropleth Map
            query1 = f'select state as State,sum(count) as No_of_Transactions ,round(sum(total_amount)) as All_Transactions , round(sum(total_amount/100000000)) as Total_Payment_Value_in_Crores from map_transaction_data where year = {Year} and quarter = {Quarter} group by state;'
            query2 = 'select * from indian_state_data;'
            cursor.execute(query1)
            #fetch all the rows returned by the first query
            rows = cursor.fetchall()
            df1 = pd.DataFrame(rows,columns = cursor.column_names)

            cursor.execute(query2)
            rows = cursor.fetchall()
            df2 = pd.DataFrame(rows,columns=cursor.column_names)
            df1["State"] = df2

            col1,col2,col3 = st.columns(3)
            with col1:
                st.header(":blue[All Transactions]")
                total_amount = df1["All_Transactions"].sum()
                st.subheader(f':orange[{total_amount}]')
            with col2:
                st.header(":blue[No of Transactions]")
                total_transactions = df1["No_of_Transactions"].sum()
                st.subheader(f':orange[{total_transactions}]')
            with col3:
                st.header(":blue[Total payment value(Cr)]")
                InCrores = df1["Total_Payment_Value_in_Crores"].sum()
                st.subheader(f':orange[{InCrores} Cr]')
            
            # Choropleth Maps
            fig = px.choropleth(df1,
                                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                featureidkey='properties.ST_NM',
                                locations="State",
                                color = 'State',
                                color_continuous_scale='speed',
                                hover_data=['State','All_Transactions','No_of_Transactions'])

            fig.update_geos(fitbounds="locations", visible=False)
            fig.update_layout(height=600,geo = dict(bgcolor='rgba(0,0,0,0)'))
            with st.spinner("Please wait !"):
                time.sleep(1)
            st.plotly_chart(fig,use_container_width=True)
                        


    if Type ==  "User":
        query3 = f'select state as State,sum(registered_users) as Total_Users ,sum(AppOpens) as Total_AppOpens from map_user_data where year = {Year} and quarter = {Quarter} group by state;'
        query4 = 'select * from indian_state_data;'
        cursor.execute(query3)
        #fetch all the rows returned by the first query
        rows = cursor.fetchall()
        df3 = pd.DataFrame(rows,columns = cursor.column_names)

        cursor.execute(query4)
        rows = cursor.fetchall()
        df4 = pd.DataFrame(rows,columns=cursor.column_names)
        df3["State"] = df4


        st.header(":blue[Total Users]")
        total_users = df3["Total_Users"].sum()
        st.subheader(f':orange[{total_users}]')
    

    #   Choropleth Maps
        fig = px.choropleth(df3,
                            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            locations="State",
                            color = 'State',
                            color_continuous_scale='speed',
                            hover_data=['State','Total_Users'])

        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(height=600,geo = dict(bgcolor='rgba(0,0,0,0)'))
        with st.spinner("Please wait !"):
            time.sleep(1)
        st.plotly_chart(fig,use_container_width=True)   

with tab3:
    st.subheader(":blue[These Analysis is Based on the Overall Data]")
    questions = st.selectbox(":orange[Select any questions given below to get detailed insights:]",
    ['Click the question that you would like to query',
    '1. Top 10 states which has the highest total amount and which payment type does they belong to?',
    '2. Top 10 Brands with the most number of Registered Users?',
    '3. Top 10 districts which has the highest Total Payments',
    '4. Least 10 districts which has the least Total Payments',
    '5. Which Payment Type has the highest Number of Transactions',
    '6. Top 10 Districts which has the highest number of Registered Users',
    '7. Average Transaction Values of each State',
    '8. Number of Registered Users present in Each Brand'])

    if questions == '1. Top 10 states which has the highest total amount and which payment type does they belong to?':
        query5 = '''select distinct(state) as State,payment_type as Payment_Type,round(sum(total_amount)) as Total_Transaction_amount from aggregated_transaction_data
                   group by State,Payment_Type
                   order by Total_Transaction_amount desc
                   limit 10;'''
        
        cursor.execute(query5)
        rows = cursor.fetchall()
        df5 = pd.DataFrame(rows,columns=cursor.column_names)
        
        col1,col2 = st.columns(2)

        with st.spinner("Please wait !"):
            time.sleep(1)
        with col1:
            st.write(df5)
        with col2:
            # Bar Charts:
            fig = px.bar(df5,x = 'State',y = 'Total_Transaction_amount',color = 'State', title = 'Highest Total Amount by State and Payment Type')
            st.plotly_chart(fig,use_container_width=True)


    elif questions == '2. Top 10 Brands with the most number of Registered Users?':
        query6 = '''select sum(registered_users) as Registered_Users,brand as Brand from aggregated_userdata 
                    group by brand
                    order by registered_users desc
                    limit 10;''' 
        cursor.execute(query6)
        rows = cursor.fetchall()
        df6 = pd.DataFrame(rows,columns=cursor.column_names)

        col1,col2 = st.columns(2)
        
        with st.spinner("Please wait !"):
            time.sleep(1)
        with col1:
            st.write(df6)
        with col2:
            # Bar charts:
            fig = px.bar(df6,x = "Brand",y = "Registered_Users",color = "Brand",title = 'Most Registered Users by Brand')
            st.plotly_chart(fig,use_container_width=True)

    elif questions == '3. Top 10 districts which has the highest Total Payments':
        query7 = 'SELECT distinct(state) as State FROM aggregated_transaction_data;'
        cursor.execute(query7)
        rows = cursor.fetchall()
        df7 = pd.DataFrame(rows,columns=cursor.column_names)
      
        list_of_states = df7["State"].to_dict().values()    
        State = st.selectbox("Select a State",list_of_states)

        query8 = f'''select state as State,district,round(sum(total_amount)) as All_Transactions,count(count) as No_of_Transactions
                    from top_transaction_data
                    where State = '{State}'
                    group by state,district
                    order by All_Transactions desc
                    limit 10;'''
        cursor.execute(query8)
        rows = cursor.fetchall()
        df8 = pd.DataFrame(rows,columns=cursor.column_names)

        col1,col2 = st.columns(2)

        with st.spinner("Please wait !"):
            time.sleep(1)
        with col1:
            st.dataframe(df8[["district","All_Transactions"]])
        with col2:       
            fig = px.bar(df8,x = "district",y = "All_Transactions",color = "district",color_continuous_scale="magma",hover_data=["State","All_Transactions","No_of_Transactions"],title = 'Highest Total Payments by District',orientation="v")
            st.plotly_chart(fig,use_container_width=True)
    
    elif questions == '4. Least 10 districts which has the least Total Payments':
        query9 = 'SELECT distinct(state) as State FROM aggregated_transaction_data;'
        cursor.execute(query9)
        rows = cursor.fetchall()
        df9 = pd.DataFrame(rows,columns=cursor.column_names)
      
        list_of_states = df9["State"].to_dict().values()    
        State = st.selectbox("Select a State",list_of_states)

        query10 = f'''select state as State,district,round(sum(total_amount)) as All_Transactions,count(count) as No_of_Transactions
                    from top_transaction_data
                    where State = '{State}'
                    group by state,district
                    order by All_Transactions
                    limit 10;'''
        cursor.execute(query10)
        rows = cursor.fetchall()
        df10 = pd.DataFrame(rows,columns=cursor.column_names)

        col1,col2 = st.columns(2)

        with st.spinner("Please wait !"):
            time.sleep(1)
        with col1:
            st.dataframe(df10[["district","All_Transactions"]])
        with col2:       
            fig = px.bar(df10,x = "district",y = "All_Transactions",color = "district",color_continuous_scale="magma",hover_data=["State","All_Transactions","No_of_Transactions"],title = 'Lowest Total Payments by District',orientation="v")
            st.plotly_chart(fig,use_container_width=True)
    
    elif questions == '5. Which Payment Type has the highest Number of Transactions':
        query9 = '''select payment_type as Payment_Type, sum(count) as Number_of_Transactions from aggregated_transaction_data
                    group by Payment_Type
                    order by Number_of_Transactions desc;'''
        cursor.execute(query9)
        rows = cursor.fetchall()
        df9 = pd.DataFrame(rows,columns = cursor.column_names)

        col1,col2 = st.columns(2)

        with st.spinner("Please wait !"):
            time.sleep(1)
        with col1:
            st.dataframe(df9)
        with col2:
            pie_chart = px.pie(df9,values = 'Number_of_Transactions',names='Payment_Type',title = 'Payment Type Distribution by Transaction Count')              
            st.plotly_chart(pie_chart,use_container_width=True)

    elif questions == '6. Top 10 Districts which has the highest number of Registered Users':
        query10 = 'SELECT distinct(state) as State FROM aggregated_transaction_data;'
        cursor.execute(query10)
        rows = cursor.fetchall()
        df10 = pd.DataFrame(rows,columns=cursor.column_names)
      
        list_of_states = df10["State"].to_dict().values()    
        State = st.selectbox("Select a State",list_of_states)
      

        query11 = f'''select state as State,district as District,sum(registered_users_d) as Registered_Users from top_user_data 
                      where State = '{State}'
                      group by State,district
                      order by Registered_Users desc
                      limit 10;'''
        
        cursor.execute(query11)
        rows = cursor.fetchall()
        df11 = pd.DataFrame(rows,columns=cursor.column_names)

        col1,col2 = st.columns(2)

        with st.spinner("Please wait !"):
            time.sleep(1)
        with col1:
            st.dataframe(df11[["District","Registered_Users"]])
        with col2:       
            hist = px.histogram(df11,x = "District",y = "Registered_Users",color = "District",hover_data=['State','District','Registered_Users'],title = 'Most Registered Users by District')
            st.plotly_chart(hist,use_container_width=True)

    
    elif questions == '7. Average Transaction Values of each State':
        query12 = '''select state,round(avg(total_amount))
                     as Average_Transaction_amount from map_transaction_data
                     group by state;'''
        cursor.execute(query12)
        rows = cursor.fetchall()
        df12 = pd.DataFrame(rows,columns = cursor.column_names)
        
        with st.spinner("Please wait !"):
            time.sleep(1)
            scatter_plot = px.sunburst(df12,names = 'Average_Transaction_amount',values = 'Average_Transaction_amount',path= ['state','Average_Transaction_amount'])
            st.plotly_chart(scatter_plot,use_container_width=True)

            st.dataframe(df12)
    
    elif questions == '8. Number of Registered Users present in Each Brand':
        query13 = 'SELECT distinct(state) as State FROM aggregated_transaction_data;'
        cursor.execute(query13)
        rows = cursor.fetchall()
        df13 = pd.DataFrame(rows,columns=cursor.column_names)
      
        list_of_states = df13["State"].to_dict().values()    
        State = st.selectbox("Select a State",list_of_states)

        query14 = f'''select state,sum(registered_users) as Registered_Users,brand from aggregated_userdata
                     where state = '{State}'
                     group by state,brand;'''
        
        cursor.execute(query14)
        rows = cursor.fetchall()
        df14 = pd.DataFrame(rows,columns = cursor.column_names)

        with st.spinner("Please wait !"):
            time.sleep(1)
            tree_map = px.treemap(df14,names = 'brand',parents='state',values = 'Registered_Users',color = 'brand',title = 'Registered Users by Brand')
            st.plotly_chart(tree_map,use_container_width=True)
            
            st.dataframe(df14)
     






