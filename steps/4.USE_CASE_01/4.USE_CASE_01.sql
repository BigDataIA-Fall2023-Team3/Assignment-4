
USE ROLE ANALYST_ROLE;
USE WAREHOUSE A4_WH;

USE DATABASE A4_DB;


USE SCHEMA A4_DB.BIGDATA;



-- Create or replace a view to calculate the annual robbery count for cities in the US


CREATE OR REPLACE VIEW robbery_count_view AS
SELECT
    ic.CITY AS city,
    convert_date_to_year(ts.DATE) AS year,
    ts.VALUE AS robbery_count
FROM
    urban_crime_timeseries ts
JOIN
    urban_crime_incident_log ic 
ON ts.GEO_ID = ic.GEO_ID
WHERE
    ts.VARIABLE_NAME = 'Daily count of incidents, robbery'
GROUP BY
    ic.CITY, year, robbery_count;

CREATE OR REPLACE VIEW view_annual_robbery_summary AS
SELECT CITY, YEAR, SUM(ROBBERY_COUNT) AS TOTAL_ROBBERY_COUNT
FROM ROBBERY_COUNT_VIEW
GROUP BY CITY, YEAR
ORDER BY TOTAL_ROBBERY_COUNT DESC;









