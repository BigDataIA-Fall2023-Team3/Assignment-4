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

def year_with_highest_crime_count():

    conn = snowflake.connector.connect(**snowflake_config)

    # SQL query to get the year with the highest crime count
    sql_query = """
    SELECT YEAR(DATE) AS CrimeYear, SUM(VALUE) AS TotalCrimeCount
    FROM CRIME_DATA_WITH_RELATIONSHIP_TYPE_VIEW
    GROUP BY CrimeYear
    ORDER BY TotalCrimeCount DESC
    """

    cursor = conn.cursor()
    cursor.execute(sql_query)

    # Fetch the result
    result = cursor.fetchone()
    conn.close()

    if result:
        year = result[0]
        total_crime_count = result[1]
        return f"The year with the highest crime count is {year} with a total crime count of {total_crime_count}."
    else:
        return f"No data found."

# Example usage:
result = year_with_highest_crime_count()
print(result)


def most_committed_crime_name():
    conn = snowflake.connector.connect(**snowflake_config)

    # SQL query to find the most committed crime name
    sql_query = """
    SELECT VARIABLE_NAME AS CrimeName, SUM(VALUE) AS TotalCrimeCount
    FROM CRIME_DATA_WITH_RELATIONSHIP_TYPE_VIEW
    GROUP BY CrimeName
    ORDER BY TotalCrimeCount DESC
    LIMIT 1
    """

    cursor = conn.cursor()
    cursor.execute(sql_query)

    # Fetch the result
    result = cursor.fetchone()
    conn.close()

    if result:
        crime_name = result[0]
        total_crime_count = result[1]
        return f"The most committed crime name is '{crime_name}' with a total crime count of {total_crime_count}."
    else:
        return f"No data found."

# Example usage:
result = most_committed_crime_name()
print(result)


def total_crime_count():
    conn = snowflake.connector.connect(**snowflake_config)

    # SQL query to calculate the total crime count
    sql_query = """
    SELECT SUM(VALUE) AS TotalCrimeCount
    FROM CRIME_DATA_WITH_RELATIONSHIP_TYPE_VIEW
    """

    cursor = conn.cursor()
    cursor.execute(sql_query)

    result = cursor.fetchone()
    conn.close()

    if result:
        total_count = result[0]
        return f"The total crime count is {total_count}."
    else:
        return "No data available."

# Example usage:
result = total_crime_count()
print(result)
