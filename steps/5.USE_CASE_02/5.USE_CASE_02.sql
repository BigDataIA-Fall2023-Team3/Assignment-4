USE ROLE ANALYST_ROLE;
USE WAREHOUSE A4_WH;
USE DATABASE A4_DB;
USE SCHEMA BIGDATA;
CREATE OR REPLACE VIEW view_detailed_crime_analysis AS
SELECT 
    uci.INCIDENT_ID,
    uci.OFFENSE_CATEGORY,
    classify_crime_severity(uci.OFFENSE_CATEGORY) AS Severity_Classification,
    gi.GEO_NAME AS Geography_Name,
    uci.CITY AS Incident_Location,
    uci.DATE
FROM 
    URBAN_CRIME_INCIDENT_LOG uci
JOIN 
    GEOGRAPHY_INDEX gi 
ON 
    uci.GEO_ID = gi.GEO_ID;


CREATE OR REPLACE VIEW view_crime_summary AS
SELECT
    Incident_Location,
    COUNT(*) AS Total_Number_of_Crimes,
    SUM(CASE WHEN Severity_Classification = 'High' THEN 1 ELSE 0 END) AS High,
    SUM(CASE WHEN Severity_Classification = 'Medium' THEN 1 ELSE 0 END) AS Medium,
    SUM(CASE WHEN Severity_Classification = 'Low' THEN 1 ELSE 0 END) AS Low
FROM
    view_detailed_crime_analysis
GROUP BY
    Incident_Location;

