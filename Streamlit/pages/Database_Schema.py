import streamlit as st


st.title("Urban Crime Data Analysis")

st.write("Here are the datasets available for analysis:")

# GEOGRAPHY_INDEX Dataset
st.header("GEOGRAPHY_INDEX Dataset")
st.write("""
**Schema:** GEO_ID (VARCHAR), GEO_NAME (VARCHAR), LEVEL (VARCHAR), ISO_NAME (VARCHAR), ISO_ALPHA2 (VARCHAR), ISO_ALPHA3 (VARCHAR), ISO_NUMERIC_CODE (VARCHAR), ISO_3166_2_CODE (VARCHAR)
**Explanation:** Stores basic information about different geographical locations, including their names, identifiers, and ISO standard codes.
**Example Query:** `SELECT GEO_NAME, LEVEL, ISO_NAME FROM GEOGRAPHY_INDEX WHERE LEVEL = 'City';`
""")

# GEOGRAPHY_RELATIONSHIPS Dataset
st.header("GEOGRAPHY_RELATIONSHIPS Dataset")
st.write("""
**Schema:** GEO_NAME (VARCHAR), GEO_ID (VARCHAR), LEVEL (VARCHAR), RELATED_GEO_NAME (VARCHAR), RELATED_GEO_ID (VARCHAR), RELATED_LEVEL (VARCHAR), RELATIONSHIP_TYPE (VARCHAR)
**Explanation:** Describes relationships between different geographical locations, such as overlaps or connections.
**Example Query:** `SELECT GEO_NAME, RELATED_GEO_NAME, RELATIONSHIP_TYPE FROM GEOGRAPHY_RELATIONSHIPS WHERE RELATIONSHIP_TYPE = 'Overlaps';`
""")

# URBAN_CRIME_ATTRIBUTES Dataset
st.header("URBAN_CRIME_ATTRIBUTES Dataset")
st.write("""
**Schema:** VARIABLE (VARCHAR), VARIABLE_NAME (VARCHAR), OFFENSE_CATEGORY (VARCHAR), MEASURE (VARCHAR), UNIT (VARCHAR), FREQUENCY (VARCHAR)
**Explanation:** Holds attributes related to urban crimes, including types of offenses and measurement details.
**Example Query:** `SELECT OFFENSE_CATEGORY, COUNT(*) FROM URBAN_CRIME_ATTRIBUTES GROUP BY OFFENSE_CATEGORY;`
""")

# URBAN_CRIME_INCIDENT_LOG Dataset
st.header("URBAN_CRIME_INCIDENT_LOG Dataset")
st.write("""
**Schema:** GEO_ID (VARCHAR), INCIDENT_ID (VARCHAR), REPORTING_LEVEL (VARCHAR), OFFENSE_CATEGORY (VARCHAR), ORIGINAL_DESCRIPTION (VARCHAR), CODE (VARCHAR), REPORTING_SYSTEM (VARCHAR), CITY (VARCHAR), DATE (DATE), PROVENANCE_DOMAIN (VARCHAR), PROVENANCE_URL (VARCHAR)
**Explanation:** Logs individual crime incidents, including their details, locations, and reporting information.
**Example Query:** `SELECT CITY, COUNT(*) FROM URBAN_CRIME_INCIDENT_LOG WHERE OFFENSE_CATEGORY = 'Theft' GROUP BY CITY;`
""")

# URBAN_CRIME_TIMESERIES Dataset
st.header("URBAN_CRIME_TIMESERIES Dataset")
st.write("""
**Schema:** DATE (DATE), GEO_ID (VARCHAR), CITY (VARCHAR), VARIABLE (VARCHAR), VARIABLE_NAME (VARCHAR), VALUE (NUMBER)
**Explanation:** Tracks crime statistics over time for different locations, offering a timeseries perspective on urban crime data.
**Example Query:** `SELECT CITY, VARIABLE_NAME, SUM(VALUE) FROM URBAN_CRIME_TIMESERIES WHERE DATE BETWEEN '2021-01-01' AND '2021-12-31' GROUP BY CITY, VARIABLE_NAME;`
""")


