USE ROLE ANALYST_ROLE;
USE WAREHOUSE A4_WH;

USE DATABASE A4_DB;
USE SCHEMA BIGDATA;

CREATE OR REPLACE VIEW crime_trends_in_relation_to_geography AS
SELECT 
    gr.RELATED_GEO_NAME,
    gr.RELATIONSHIP_TYPE,
    extract_weekday(uct.DATE) AS Weekday,
    uct.VARIABLE,
    SUM(uct.VALUE) AS Total_Incidents
FROM 
    URBAN_CRIME_TIMESERIES uct
JOIN 
    GEOGRAPHY_RELATIONSHIPS gr
ON 
    uct.GEO_ID = gr.GEO_ID
GROUP BY 
    gr.RELATED_GEO_NAME, gr.RELATIONSHIP_TYPE, Weekday, uct.VARIABLE
ORDER BY 
    gr.RELATED_GEO_NAME, Weekday, Total_Incidents DESC;



CREATE OR REPLACE VIEW weekday_incident_probability AS
WITH total_incidents AS (
    SELECT 
        Weekday, 
        SUM(Total_Incidents) AS Weekday_Total_Incidents
    FROM 
        crime_trends_in_relation_to_geography
    GROUP BY 
        Weekday
),
total_count AS (
    SELECT 
        SUM(Weekday_Total_Incidents) AS Total_Incidents_All_Weekdays
    FROM 
        total_incidents
)
SELECT 
    ti.Weekday, 
    ti.Weekday_Total_Incidents,
    (ti.Weekday_Total_Incidents / tc.Total_Incidents_All_Weekdays) AS Probability
FROM 
    total_incidents ti
CROSS JOIN 
    total_count tc
ORDER BY 
    ti.Weekday;




