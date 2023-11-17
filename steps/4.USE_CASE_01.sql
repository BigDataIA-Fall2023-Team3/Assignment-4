
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


-- Create or replace a view to calculate the annual robbery count for cities in 2022
CREATE OR REPLACE VIEW view_annual_robbery_summary AS
SELECT
    ic.city,
    convert_date_to_year(ts.date),
    SUM(ts.value) AS annual_robbery,
    DENSE_RANK() OVER (ORDER BY SUM(ts.value) DESC) AS robbery_city_rank
FROM
    A4_DB.BIGDATA.urban_crime_timeseries AS ts
JOIN
    A4_DB.BIGDATA.urban_crime_incident_log AS ic ON ts.geo_id = ic.geo_id
WHERE
    AND ts.variable_name = 'Daily count of incidents, robbery'
GROUP BY
    ts.geo_id, ic.city, year
ORDER BY
    annual_robbery DESC;













