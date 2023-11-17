USE ROLE ANALYST_ROLE;
USE WAREHOUSE A4_WH;
USE DATABASE A4_DB;
USE SCHEMA A4_DB.BIGDATA;

-- Create a UDF to convert a date to a year
CREATE OR REPLACE FUNCTION convert_date_to_year(input_date DATE)
RETURNS STRING
AS
$$
    CASE
        WHEN EXTRACT(YEAR FROM input_date) IS NOT NULL THEN CAST(EXTRACT(YEAR FROM input_date) AS STRING)
        ELSE NULL
    END
$$;


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

CREATE OR REPLACE FUNCTION classify_relationship_type(relationship_type STRING)
RETURNS STRING 
AS
$$
    CASE 
        WHEN relationship_type = 'Overlaps' THEN 'OVERLAPS'
        ELSE 'CONTAINS'
    END
$$;