import snowflake.connector
import os

# Define Snowflake configuration
snowflake_config = {
    'user': os.environ['SNOWSQL_USER'],
    'password': os.environ['SNOWSQL_PWD'],
    'account': os.environ['SNOWSQL_ACCOUNT'],
    'warehouse': 'A4_WH',  
    'database': 'A4_DB',   
    'schema': 'BIGDATA'       
    }

def get_total_incidents_by_geoname(geoname):
    conn = snowflake.connector.connect(**snowflake_config)

    # Define SQL query to get the sum of total incidents for the specified geoname
    sql_query = f"""
    SELECT SUM(Total_Incidents) AS TotalIncidents
    FROM crime_trends_in_relation_to_geography
    WHERE RELATED_GEO_NAME LIKE %s
    """

    parameter_value = f"%{geoname}%"

    cursor = conn.cursor()
    cursor.execute(sql_query, (parameter_value,))

    # Fetch the result
    result = cursor.fetchone()
    conn.close()

    if result:
        total_incidents = result[0]
        return f"The sum of total incidents in '{geoname}' is {total_incidents}."
    else:
        return f"No data found for '{geoname}'."

def get_probability_by_weekday(weekday):
    conn = snowflake.connector.connect(**snowflake_config)

    # Define SQL query to get the probability of crime for the specified weekday
    sql_query = f"""
    SELECT Probability
    FROM weekday_incident_probability
    WHERE Weekday = '{weekday}'
    """

    cursor = conn.cursor()
    cursor.execute(sql_query)

    # Fetch the result
    result = cursor.fetchone()
    conn.close()

    if result:
        probability = result[0]
        return f"The probability of crime on '{weekday}' is {probability}."
    else:
        return f"No data found for '{weekday}'."

# Example usages:
geoname = ''  # Replace with the desired geoname
weekday = 'Monday'   # Replace with the desired weekday
result1 = get_total_incidents_by_geoname(geoname)
result2 = get_probability_by_weekday(weekday)
print(result1)
print(result2)