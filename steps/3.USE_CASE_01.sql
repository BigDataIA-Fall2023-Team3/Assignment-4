
USE ROLE ANALYST_ROLE;
USE WAREHOUSE A4_WH;

USE DATABASE A4_DB;

CREATE OR REPLACE FUNCTION get_annual_robbery(city_name VARCHAR, year_to_filter INT)
RETURNS TABLE (
    geo_id INT,
    city VARCHAR,
    year STRING,
    annual_robbery INT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        ts.geo_id,
        ic.city,
        YEAR(ts.date)::STRING AS year,
        SUM(ts.value) AS annual_robbery
    FROM
        BIGDATA.urban_crime_timeseries AS ts
    JOIN
        BIGDATA.urban_crime_incident_log AS ic ON ts.geo_id = ic.geo_id
    WHERE
        YEAR(ts.date) = year_to_filter
        AND ts.variable_name = 'Daily count of incidents, robbery'
        AND ic.city = city_name
    GROUP BY
        ts.geo_id, ic.city, year
    ORDER BY
        annual_robbery DESC;
END;
$$ LANGUAGE plpgsql;

