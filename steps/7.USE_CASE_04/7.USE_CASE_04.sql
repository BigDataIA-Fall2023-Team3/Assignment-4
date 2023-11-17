USE ROLE ANALYST_ROLE;
USE DATABASE A4_DB;
USE SCHEMA BIGDATA;

--Urban Crime Analysis with Geographical Relationships
CREATE OR REPLACE VIEW crime_data_with_relationship_type_view AS
SELECT
    geo.geo_name AS base_geo_name,
    ts.city,
    ts.date,
    ts.variable_name,
    ts.value,
    ROW_NUMBER() OVER (PARTITION BY ts.variable_name ORDER BY ts.date) AS row_num,
    rel.related_geo_name,
    rel.related_geo_id,
    rel.related_level,
    classify_relationship_type(rel.relationship_type) AS classified_relationship_type
FROM A4_DB.BIGDATA.urban_crime_timeseries AS ts
JOIN A4_DB.BIGDATA.geography_index AS geo ON ts.geo_id = geo.geo_id
INNER JOIN A4_DB.BIGDATA.geography_relationships AS rel ON geo.geo_id = rel.geo_id
WHERE geo.geo_name = '11221' --zip code of interest
ORDER BY ts.date;
