-- Step #1: Accept Anaconda Terms & Conditions
-- Refer to Snowflake Documentation for Third-Party Python Packages

-- Step #2: Create the account level objects
USE ROLE ACCOUNTADMIN;

-- Roles
SET MY_USER = CURRENT_USER();
CREATE OR REPLACE ROLE MY_PROJECT_ROLE;
GRANT ROLE MY_PROJECT_ROLE TO ROLE SYSADMIN;
GRANT ROLE MY_PROJECT_ROLE TO USER IDENTIFIER($MY_USER);

GRANT EXECUTE TASK ON ACCOUNT TO ROLE MY_PROJECT_ROLE;
GRANT MONITOR EXECUTION ON ACCOUNT TO ROLE MY_PROJECT_ROLE;

-- Databases
CREATE OR REPLACE DATABASE BIGDATA;
GRANT OWNERSHIP ON DATABASE BIGDATA TO ROLE MY_PROJECT_ROLE;

-- Warehouses
CREATE OR REPLACE WAREHOUSE WH-BIGDATA WAREHOUSE_SIZE = XSMALL, AUTO_SUSPEND = 300, AUTO_RESUME = TRUE;
GRANT OWNERSHIP ON WAREHOUSE WH-BIGDATA TO ROLE MY_PROJECT_ROLE;

-- Step #3: Create the database level objects
USE ROLE MY_PROJECT_ROLE;
USE WAREHOUSE WH-BIGDATA;
USE DATABASE BIGDATA;

-- Schemas
CREATE OR REPLACE SCHEMA SOCIAL_MEDIA;
CREATE OR REPLACE SCHEMA FOURSQUARE_PLACES;
CREATE OR REPLACE SCHEMA CONSUMER_PAYMENTS;
CREATE OR REPLACE SCHEMA DOMAIN_PERFORMANCE;

-- Further steps to create tables, stages, and other objects specific to your datasets can be added here
