
USE ROLE ANALYST_ROLE;
USE WAREHOUSE A4_WH;

USE DATABASE A4_DB;


-- ----------------------------------------------------------------------------
-- Step #1: Connect to weather data in Marketplace
-- ----------------------------------------------------------------------------

/*---
But what about data that needs constant updating - like the WEATHER data? We would
need to build a pipeline process to constantly update that data to keep it fresh.

Perhaps a better way to get this external data would be to source it from a trusted
data supplier. Let them manage the data, keeping it accurate and up to date.

Enter the Snowflake Data Cloud...

Weather Source is a leading provider of global weather and climate data and their
OnPoint Product Suite provides businesses with the necessary weather and climate data
to quickly generate meaningful and actionable insights for a wide range of use cases
across industries. Let's connect to the "Weather Source LLC: frostbyte" feed from
Weather Source in the Snowflake Data Marketplace by following these steps:

    -> Snowsight Home Button
         -> Marketplace
             -> Search: "Crime Stastics" (and click on tile in results)
                 -> Click the blue "Get" button
                     -> Under "Options", adjust the Database name to read "Crime Stastics" (all capital letters)
                        -> Grant to "ANALYST_ROLE"
    
That's it... we don't have to do anything from here to keep this data updated.
The provider will do that for us and data sharing means we are always seeing
whatever they they have published.

Use case 1 :Crime Analysis:

Law Enforcement: Law enforcement agencies could use this information to identify areas with high levels of robbery incidents. This can help them allocate resources effectively, increase patrols, or implement targeted crime prevention strategies in specific neighborhoods.
City Planners: City planners and policymakers may use this data to assess the safety of different neighborhoods and make informed decisions about urban development and resource allocation.                                                                       

--List of zip codes with highest levels of specific crimes (e.g., robbery) in 2022




---*/
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
    YEAR(ts.date) = '2022'
    AND ts.variable_name = 'Daily count of incidents, robbery'
GROUP BY
    ts.geo_id, ic.city, year
ORDER BY
    annual_robbery DESC;
