
--create view1

CREATE OR REPLACE A4_DB.RESULTS.urban_crime_annual_robbery_view AS
SELECT
    urban_crime_timeseries.geo_id,
    urban_crime_incident_log.city,
    YEAR(urban_crime_timeseries.date)::STRING AS year,
    urban_crime_timeseries.value 
FROM
    BIGDATA.urban_crime_timeseries
JOIN
    BIGDATA.urban_crime_incident_log ON urban_crime_timeseries.geo_id = urban_crime_incident_log.geo_id;

SELECT*FROM A4_DB.RESULTS.urban_crime_annual_robbery_view LIMIT 10;


--CREATE view2

CREATE OR REPLACE VIEW A4_DB.RESULTS.urban_crime_top_theft_view AS
SELECT
    geo.geo_name,
    ts.city,
    ts.date,
    ts.variable_name,
    ts.value
FROM
    bigdata.urban_crime_timeseries AS ts
JOIN
    bigdata.geography_index AS geo ON (ts.geo_id = geo.geo_id);

SELECT*FROM A4_DB.RESULTS.urban_crime_top_theft_view LIMIT 10;

--CREATE view3

CREATE OR REPLACE VIEW A4_DB.RESULTS.urban_crime_dui_view AS
SELECT
    YEAR(ts.DATE)::STRING AS Year,
    ts.GEO_ID,
    ts.CITY,
    ca.OFFENSE_CATEGORY,
    ts.VARIABLE_NAME ,
    ts.VALUE
FROM
    bigdata.URBAN_CRIME_TIMESERIES AS ts
JOIN
    bigdata.URBAN_CRIME_ATTRIBUTES AS ca ON ts.VARIABLE = ca.VARIABLE;


SELECT * FROM A4_DB.RESULTS.urban_crime_dui_view LIMIT 10;





