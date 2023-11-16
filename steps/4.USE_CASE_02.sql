-- /*---
-- Use Case 2:Community Awareness:

-- Residents and community leaders can be informed about areas with high theft incidents, encouraging community engagement and awareness.
-- Retail and Business Decision-Making:

-- Businesses and retailers can use the information to make informed decisions about security measures and location planning, especially if certain zip codes have higher theft rates.                                                                                                  


-- Top five ZIP CODES in US with  specific crime incidents 

USE ROLE ANALYST_ROLE;
USE WAREHOUSE A4_WH;

USE DATABASE A4_DB;

SELECT
    geo.geo_name,
    ts.city,
    ts.date,
    ts.variable_name,
    ts.value
FROM
    bigdata.urban_crime_timeseries AS ts
JOIN
    bigdata.geography_index AS geo ON (ts.geo_id = geo.geo_id)
WHERE
    ts.variable_name = 'Daily count of incidents, theft'
ORDER BY
    ts.value DESC 
LIMIT 5;