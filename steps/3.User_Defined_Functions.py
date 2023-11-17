import snowflake.connector
import os
import subprocess

# Snowflake connection parameters
snowflake_config = {
    'user': 'SANJU1209',
    'password': 'Sanju1209',
    'account': 'HYUGZMI-NFB65118',
    'warehouse': 'A4_WH',
    'database': 'A4_DB',
    'schema': 'BIGDATA'
}


conn = snowflake.connector.connect(**snowflake_config)

# Define UDFs
udf_convert_date_to_year = """
CREATE OR REPLACE FUNCTION convert_date_to_year(input_date DATE)
RETURNS STRING
AS
$$
    CASE
        WHEN EXTRACT(YEAR FROM input_date) IS NOT NULL THEN CAST(EXTRACT(YEAR FROM input_date) AS STRING)
        ELSE NULL
    END
$$;
"""

udf_classify_crime_severity = """
CREATE OR REPLACE FUNCTION classify_crime_severity(offense_category STRING)
RETURNS STRING
AS
$$
    CASE
        WHEN offense_category IN ('Homicide', 'Human Trafficking', 'Sex Offense', 'Offense Involving Children') THEN 'High'
        WHEN offense_category IN ('Robbery', 'Battery Or Assault', 'Narcotics', 'Burglary', 'Interference With Public Officer', 'Kidnapping') THEN 'Medium'
        ELSE 'Low'
    END
$$;
"""

udf_extract_weekday = """
CREATE OR REPLACE FUNCTION extract_weekday(date_input DATE)
RETURNS STRING
AS
$$
    CASE DAYOFWEEK(date_input)
        WHEN 1 THEN 'Sunday'
        WHEN 2 THEN 'Monday'
        WHEN 3 THEN 'Tuesday'
        WHEN 4 THEN 'Wednesday'
        WHEN 5 THEN 'Thursday'
        WHEN 6 THEN 'Friday'
        WHEN 7 THEN 'Saturday'
    END
$$;
"""

udf_classify_relationship_type = """
CREATE OR REPLACE FUNCTION classify_relationship_type(relationship_type STRING)
RETURNS STRING 
AS
$$
    CASE 
        WHEN relationship_type = 'Overlaps' THEN 'OVERLAPS'
        ELSE 'CONTAINS'
    END
$$;
"""

# Execute UDF creation SQL statements
cursor = conn.cursor()
cursor.execute(udf_convert_date_to_year)
cursor.execute(udf_classify_crime_severity)
cursor.execute(udf_extract_weekday)
cursor.execute(udf_classify_relationship_type)

# Close the Snowflake connection
conn.close()
