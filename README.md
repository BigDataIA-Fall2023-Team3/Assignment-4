# Assignment-4 : Snowflake Data Engineering and Streamlit Analytics Project

Welcome to the Snowflake Data Engineering and Streamlit Analytics Project repository! This project aims to demonstrate the integration of Snowflake, a cloud-based data warehousing platform, with Streamlit, a Python framework for building data applications. The goal is to process and analyze datasets stored in Snowflake using Streamlit's natural language to SQL query capabilities.

## Componenets:

- [Codelabs](https://codelabs-preview.appspot.com/?file_id=1YcEUEzPHETJZ2M912GP5cZDNx_fwh1KMA367BFW6Tng#0)
- [Streamlit]()
- [Dataset](https://app.snowflake.com/hyugzmi/nfb65118/#/data/shared/SNOWFLAKE_DATA_MARKETPLACE/listing/GZTSZAS2KIE?originTab=databases&database=CRIME_STATISTICS)

## Project Overview

In this project, we have implemented the following key components:

- Snowflake Data Management:
  - Created a Snowflake database, roles, and warehouse.
  - Loaded datasets (CRIME_STATISTICS database and 6 datasets) using SQL scripts.
  - Defined User Defined Functions (UDFs) in SQL for data transformation.
  - Created views to support specific use cases.
  - Developed dashboards for data visualization and analysis within Snowflake.

- Streamlit Data Analytics:
  - Built a Streamlit application that allows users to input natural language queries.
  - Utilized Langchain and OpenAI API to convert natural language queries into SQL queries.
  - Executed SQL queries on Snowflake views.
  - Displayed query results within the Streamlit app.

### Architecture Diagram:

![snowflake_architecture](https://github.com/BigDataIA-Fall2023-Team3/Assignment-4/assets/114708712/1a63ba2d-5273-4605-b5c9-2ec6af8ad57e)
The Snowflake architecture consists of Snowflake Database, Python Scripts for SQL and UDFs, Views, Tables, Datasets, and Dashboards. Data flows from datasets into Snowflake, where it is processed, transformed, and made accessible through views and dashboards.

![streamlit_architecture](https://github.com/BigDataIA-Fall2023-Team3/Assignment-4/assets/114708712/82ca9a45-f9e2-492f-9d04-d1362960ca0b)
The Streamlit architecture involves user interaction with a Streamlit application. Natural language queries provided by users are converted into SQL queries using Langchain and OpenAI. These SQL queries are executed on Snowflake views, and the results are displayed within the Streamlit app.

## Getting Started

To get started with this project, follow these steps:

1. Clone the repository to your local machine
2. Install the required Python packages
   `pip install -r requirements.txt`
3. Set up Snowflake credentials and OpenAI API key as environment variables.
4. Run the Streamlit application
   `streamlit run streamlit_app.py`


##### WE ATTEST THAT WE HAVEN’T USED ANY OTHER STUDENTS’ WORK IN OUR ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK

Contributions:
- Sumanayana Konda: 25%
- Akshatha Patil: 25%
- Ruthwik Bommenahalli Gowda: 25%
- Pavan Madhav Manikantha Sai Nainala: 25%
