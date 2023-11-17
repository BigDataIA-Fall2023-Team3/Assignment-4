import snowflake.connector

# Function to get the crime count by level for a specific city
def get_crime_count_by_level(city, crime_level):
    snowflake_config = {
    'user': os.environ['SNOWSQL_USER'],
    'password': os.environ['SNOWSQL_PWD'],
    'account': os.environ['SNOWSQL_ACCOUNT'],
    'warehouse': 'A4_WH',  
    'database': 'A4_DB',   
    'schema': 'BIGDATA'       
    }

    conn = snowflake.connector.connect(**snowflake_config)

    # Define the SQL query to retrieve the count of the specified crime level in the given city
    sql_query = f"""
    SELECT SUM(CASE WHEN Severity_Classification = '{crime_level}' THEN 1 ELSE 0 END) AS CrimeCount
    FROM view_detailed_crime_analysis
    WHERE Incident_Location = '{city}'
    """

    cursor = conn.cursor()
    cursor.execute(sql_query)

    # Fetch the result
    result = cursor.fetchone()
    conn.close()

    if result:
        crime_count = result[0]
        return f"The count of '{crime_level}' level crimes in '{city}' is {crime_count}."
    else:
        return f"No data found for '{crime_level}' level crimes in '{city}'."

# Example usage:
city_name = 'New York'  # Replace with the desired city name
crime_level = 'High'   # Replace with the desired crime level ('High', 'Medium', or 'Low')
result = get_crime_count_by_level(city_name, crime_level)
print(result)

def get_total_crime_count_by_city(city):
    snowflake_config = {
    'user': os.environ['SNOWSQL_USER'],
    'password': os.environ['SNOWSQL_PWD'],
    'account': os.environ['SNOWSQL_ACCOUNT'],
    'warehouse': 'A4_WH',  
    'database': 'A4_DB',   
    'schema': 'BIGDATA'       
    }
    

    conn = snowflake.connector.connect(**snowflake_config)

    # Define the SQL query to retrieve the total number of crimes in the given city
    sql_query = f"""
    SELECT COUNT(*) AS TotalCrimeCount
    FROM view_detailed_crime_analysis
    WHERE Incident_Location = '{city}'
    """

    cursor = conn.cursor()
    cursor.execute(sql_query)

    # Fetch the result
    result = cursor.fetchone()
    conn.close()

    if result:
        total_crime_count = result[0]
        return f"The total number of crimes in '{city}' is {total_crime_count}."
    else:
        return f"No data found for '{city}'."

# Example usage:
city_name = 'New York'  # Replace with the desired city name
result = get_total_crime_count_by_city(city_name)
print(result)

