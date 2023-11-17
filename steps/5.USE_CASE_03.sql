
USE ROLE ANALYST_ROLE;
USE WAREHOUSE A4_WH;

USE DATABASE A4_DB;



--Use Case 3 : Analyzing Driving Under the Influence (DUI) Incidents in 2022   
--To analyze and understand the trend of Driving Under the Influence (DUI) incidents in urban areas during the year 2022, focusing on incident counts, locations, and offense categories.      

-- 1. Policy Evaluation:

--Policymakers can assess the impact of existing DUI prevention measures and make informed decisions about the need for adjustments or additional interventions based on the trends observed in 2022.                                                     Evaluation of Intervention Programs:

--If there were specific DUI prevention or awareness programs implemented in 2022, this analysis can help evaluate their effectiveness and identify areas for improvement.
-- 2. Research and Policy Advocacy:

-- Researchers can use this data to study patterns and trends related to DUI incidents, contributing valuable insights to academic studies. Advocacy groups can also leverage this information to support evidence-based policy recommendations.

SELECT
    YEAR(ts.DATE)::STRING AS Year,
    ts.GEO_ID,
    ts.CITY,
    ca.OFFENSE_CATEGORY,
    ts.VARIABLE_NAME AS Original_Variable_Name,
    ts.VALUE
FROM
    CRIME_STATISTICS.CYBERSYN.URBAN_CRIME_TIMESERIES AS ts
JOIN
    CRIME_STATISTICS.CYBERSYN.URBAN_CRIME_ATTRIBUTES AS ca ON ts.VARIABLE = ca.VARIABLE
WHERE
    ca.OFFENSE_CATEGORY = 'Driving Under The Influence'
    AND YEAR(ts.DATE) = '2022'
ORDER BY
    ts.DATE, ts.VALUE DESC;


