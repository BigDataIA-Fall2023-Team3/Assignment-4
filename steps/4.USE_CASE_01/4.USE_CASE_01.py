import snowflake.connector
import os
import subprocess
def city_by_year(year):
    snowflake_config = {
    'user': os.environ['SNOWSQL_USER'],
    'password': os.environ['SNOWSQL_PWD'],
    'account': os.environ['SNOWSQL_ACCOUNT'],
    'warehouse': 'A4_WH',  
    'database': 'A4_DB',   
    'schema': 'BIGDATA'       
    }


    conn = snowflake.connector.connect(**snowflake_config)
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
        return f"For the year {year}, the city with the highest robbery count is '{city}' with a count of {highest_count}."
    else:
        return f"No data found for the year {year}."

# Example usage:
year = 2022  # Replace with the desired year
result = city_by_year(year)
print(result)