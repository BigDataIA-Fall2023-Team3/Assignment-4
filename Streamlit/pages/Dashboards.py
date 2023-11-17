
import streamlit as st
import pandas as pd
import snowflake.connector


snowflake_config = {
    'user': st.secrets['SNOWFLAKE_USER'],
    'password': st.secrets['SNOWFLAKE_PASSWORD'],
    'account': st.secrets['SNOWFLAKE_ACCOUNT'],
    'warehouse': st.secrets['SNOWFLAKE_WAREHOUSE'],
    'database': st.secrets['SNOWFLAKE_DATABASE'],
    'schema': 'BIGDATA',  # Adjust the schema if necessary
}

##############################################################################################################
# USE CASE 1: Annual Robbery Count Analysis
# Function to retrieve the annual robbery count data
def view_annual_robbery_data():

    conn = snowflake.connector.connect(**snowflake_config)
    
    # SQL query to retrieve the annual robbery count data
    sql_query = """
    SELECT CITY, YEAR, SUM(ROBBERY_COUNT) AS TOTAL_ROBBERY_COUNT
    FROM ROBBERY_COUNT_VIEW
    GROUP BY CITY, YEAR
    ORDER BY YEAR, CITY;
    """

    # Execute the SQL query
    df = pd.read_sql(sql_query, conn)

    # Close the Snowflake connection
    conn.close()

    # Display the annual robbery count data as a table
    st.write("Annual Robbery Count Data")
    st.dataframe(df)

# Function to find the city with the highest robbery count for a specific year
def city_by_year(year):
   
    conn = snowflake.connector.connect(**snowflake_config)

    # SQL query to retrieve the city with the highest robbery count for the specified year
    sql_query = f"""
    WITH RobberyByYear AS (
        SELECT YEAR, CITY, SUM(ROBBERY_COUNT) AS TOTAL_ROBBERY_COUNT
        FROM ROBBERY_COUNT_VIEW
        WHERE YEAR = {year}
        GROUP BY YEAR, CITY
    )
    SELECT YEAR, CITY, MAX(TOTAL_ROBBERY_COUNT) AS HIGHEST_ROBBERY_COUNT
    FROM RobberyByYear
    GROUP BY YEAR, CITY
    HAVING MAX(TOTAL_ROBBERY_COUNT) = (SELECT MAX(TOTAL_ROBBERY_COUNT) FROM RobberyByYear)
    """

    # Execute the SQL query
    cursor = conn.cursor()
    cursor.execute(sql_query)

    # Fetch the result
    result = cursor.fetchone()
    conn.close()

    if result:
        city = result[0]
        highest_count = result[2]
        st.write(f"For the year {year}, the city with the highest robbery count is '{city}' with a count of {highest_count}.")
    else:
        st.write(f"No data found for the year {year}.")

##############################################################################################################
# USE CASE 2: Description and Dashboard
def detailed_crime_analysis():
    
    conn = snowflake.connector.connect(**snowflake_config)
    
    # SQL query to retrieve detailed crime analysis data
    sql_query = """
    SELECT INCIDENT_ID, OFFENSE_CATEGORY, Severity_Classification, Geography_Name, Incident_Location, DATE
    FROM view_detailed_crime_analysis
    LIMIT 100;  -- Limiting results to the first 100 rows for demonstration purposes
    """

    # Execute the SQL query
    df = pd.read_sql(sql_query, conn)

    # Close the Snowflake connection
    conn.close()

    # Display the detailed crime analysis data as a table
    st.write("Detailed Crime Analysis Data")
    st.dataframe(df)

# Function to retrieve crime summary statistics
def crime_summary():
    

    conn = snowflake.connector.connect(**snowflake_config)

    # SQL query to retrieve crime summary statistics
    sql_query = """
    SELECT Incident_Location, Total_Number_of_Crimes, High, Medium, Low
    FROM view_crime_summary
    """

    # Execute the SQL query
    df = pd.read_sql(sql_query, conn)

    # Close the Snowflake connection
    conn.close()

    # Display the crime summary statistics as a table
    st.write("Crime Summary Statistics")
    st.dataframe(df)

    st.write("Crime Summary Statistics (Total Crimes)")
    st.bar_chart(df.set_index('INCIDENT_LOCATION')['TOTAL_NUMBER_OF_CRIMES'])

    st.write("Crime Summary Statistics (High Level Crimes)")
    st.bar_chart(df.set_index('INCIDENT_LOCATION')['HIGH'])

    st.write("Crime Summary Statistics (Medium Level Crimes)")
    st.bar_chart(df.set_index('INCIDENT_LOCATION')['MEDIUM'])

    st.write("Crime Summary Statistics (Low Level Crimes)")
    st.bar_chart(df.set_index('INCIDENT_LOCATION')['LOW'])

##############################################################################################################
# USE CASE 3: Description and Dashboard

def crime_trends():
    
    conn = snowflake.connector.connect(**snowflake_config)
    
    # SQL query to retrieve crime trends data
    sql_query = """
            SELECT RELATED_GEO_NAME, SUM(Total_Incidents) AS Total_Incidents
            FROM crime_trends_in_relation_to_geography
            GROUP BY RELATED_GEO_NAME
            ORDER BY Total_Incidents DESC
            """
    df = pd.read_sql(sql_query, conn)
    st.write("Crime Trends Data")
    st.dataframe(df)
    conn.close()

def weekday_probability():

    conn = snowflake.connector.connect(**snowflake_config)

    weekday_probability_query = """
        SELECT Weekday, Weekday_Total_Incidents, Probability
        FROM weekday_incident_probability
        """
    df = pd.read_sql(weekday_probability_query, conn)
    st.write("Weekday Probability Data")
    st.dataframe(df)
    st.bar_chart(df.set_index('WEEKDAY')['PROBABILITY'])
    conn.close()

##############################################################################################################
# USE CASE 4: Description and Dashboard
def city_crime_count():
    
    conn = snowflake.connector.connect(**snowflake_config)
    
    # SQL query to retrieve crime trends data
    sql_query = """ SELECT CITY, CLASSIFIED_RELATIONSHIP_TYPE, SUM(VALUE)
    FROM CRIME_DATA_WITH_RELATIONSHIP_TYPE_VIEW
    GROUP BY CITY, CLASSIFIED_RELATIONSHIP_TYPE
    ORDER BY SUM(VALUE) DESC
    """
    df = pd.read_sql(sql_query, conn)
    st.write("Crime Around or Near Cities")
    st.dataframe(df)
    st.bar_chart(df.set_index('CLASSIFIED_RELATIONSHIP_TYPE')['SUM(VALUE)'])
    conn.close()
def geoname_crime_count():
    
    conn = snowflake.connector.connect(**snowflake_config)
    
    # SQL query to retrieve crime trends data
    sql_query = """ SELECT DATE, SUM(VALUE)
    FROM CRIME_DATA_WITH_RELATIONSHIP_TYPE_VIEW
    GROUP BY DATE
    ORDER BY SUM(VALUE) DESC
    """
    df = pd.read_sql(sql_query, conn)
    st.write("New York City Crime Count by Year")
    st.dataframe(df)
    st.bar_chart(df.set_index('DATE')['SUM(VALUE)'])
    conn.close()

def types_of_crime():
        
        conn = snowflake.connector.connect(**snowflake_config)
        
        # SQL query to retrieve crime trends data
        sql_query = """ SELECT VARIABLE_NAME AS OFFENSE_CATEGORY, SUM(VALUE) AS TOTAL_COUNT
        FROM CRIME_DATA_WITH_RELATIONSHIP_TYPE_VIEW
        GROUP BY OFFENSE_CATEGORY
        ORDER BY TOTAL_COUNT DESC;
        """
        df = pd.read_sql(sql_query, conn)
        st.write("New York City Crime Count By Offense Category")
        st.dataframe(df)
        st.bar_chart(df.set_index('OFFENSE_CATEGORY')['TOTAL_COUNT'][1:])
        conn.close()

##############################################################################################################
# Streamlit App
st.title("Use Case Dashboard")

# Explanation of Use Cases
st.markdown("""
This dashboard presents multiple use cases for analyzing data. Select a use case to explore and interact with the data.
""")

# Buttons for use case selection
use_case_choice = st.selectbox("Select a Use Case:", ["Use Case 1", "Use Case 2", "Use Case 3", "Use Case 4"])

# Use Case 1: Annual Robbery Count Analysis
if use_case_choice == "Use Case 1":
    st.header("Use Case 1: Annual Robbery Count Analysis")
    st.write("This use case analyzes the annual robbery count data for cities in the US.")
    st.subheader("Dashboard Options:")
    dashboard_choice = st.selectbox("Select a Dashboard:", ["View Annual Robbery Data", "City with Highest Robbery Count"])
    
    # Dashboard 1: View Annual Robbery Data
    if dashboard_choice == "View Annual Robbery Data":
        view_annual_robbery_data()

    # Dashboard 2: City with Highest Robbery Count
    if dashboard_choice == "City with Highest Robbery Count":
        year = st.number_input("Enter a Year between 2014 - 2023:", min_value=2014, max_value=2023)
        if year:
            city_by_year(year)

# Use Case 2: Description and Dashboard (Add more cases as needed)
elif use_case_choice == "Use Case 2":
    st.header("Use Case 2: Crime Analysis")
    st.markdown("""
This Use Case involves detailed crime analysis and crime summary statistics.
You can view the detailed crime analysis data and summary statistics for different incident locations.
""")
    st.subheader("Dashboard Options:")
    dashboard_choice = st.selectbox("Select a Dashboard:", ["Detailed Crime Analysis", "Crime Summary Statistics"])
    
    # Dashboard 1: Detailed Crime Analysis
    if dashboard_choice == "Detailed Crime Analysis":
        detailed_crime_analysis()

    # Dashboard 2: Crime Summary Statistics
    if dashboard_choice == "Crime Summary Statistics":
        crime_summary()

# Use Case 3: Description and Dashboard (Add more cases as needed)
elif use_case_choice == "Use Case 3":
    st.header("Use Case 3: Crime Trends")
    st.subheader("Dashboard Options:")
    dashboard_choice = st.selectbox("Select a Dashboard:", ["Crime Trends", "Weekday Probability"])
    if dashboard_choice == "Crime Trends":
        st.write("Use Case 3: Crime Trends: The number of crimes in relation to geography")
        crime_trends()
    if dashboard_choice == "Weekday Probability":
        st.write("Use Case 3: Weekday Probability: The probability of a crime occurring on a weekday")
        weekday_probability()

# Use Case 4: Description and Dashboard (Add more cases as needed)
elif use_case_choice == "Use Case 4":
    st.header("Use Case 4: Crime Analysis in NEW YORK CITY")
    st.subheader("Dashboard Options:")
    dashboard_choice = st.selectbox("Select a Dashboard:", ["City Crime Count", "Geoname Crime Count", "Types of Crime"])
    if dashboard_choice == "City Crime Count":
        st.write("Use Case 4: New York City Crime Count: The number of crimes around or near cities")
        city_crime_count()
    if dashboard_choice == "Geoname Crime Count":
        st.write("Use Case 4: New York City Crime Count: The number of crimes in each year")
        geoname_crime_count()
    if dashboard_choice == "Types of Crime":
        st.write("Use Case 4: New York City Crime Count: The number of crimes by offense category")
        types_of_crime()
    
