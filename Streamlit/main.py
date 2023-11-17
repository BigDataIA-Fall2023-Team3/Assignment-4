import streamlit as st
import openai
import os
from langchain.chains import create_sql_query_chain
from langchain.chat_models import ChatOpenAI
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL
import pandas as pd


# Load environment variables for Snowflake credentials
snowflake_user = st.secrets['SNOWFLAKE_USER']
snowflake_password = st.secrets['SNOWFLAKE_PASSWORD']
snowflake_account = st.secrets['SNOWFLAKE_ACCOUNT']
snowflake_warehouse = st.secrets['SNOWFLAKE_WAREHOUSE']
snowflake_database = st.secrets['SNOWFLAKE_DATABASE']
snowflake_schema = st.secrets['SNOWFLAKE_SCHEMA']
snowflake_role = st.secrets['SNOWFLAKE_ROLE']
openai_api_key = st.secrets['OPENAI_API_KEY']

# Custom wrapper class for the SQLAlchemy engine
class CustomEngineWrapper:
    def __init__(self, engine):
        self.engine = engine

    def get_table_info(self, table_names=None):
        # Logic to retrieve table information
        with self.engine.connect() as connection:
            if table_names:
                # If specific table names are provided, retrieve information for those tables
                query = """
                    SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE 
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_SCHEMA = '{}' AND TABLE_NAME IN ({})""".format(
                        snowflake_schema, ','.join(f"'{name}'" for name in table_names))
            else:
                # If no specific table names are provided, retrieve information for all tables in the schema
                query = """
                    SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE 
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_SCHEMA = '{}'""".format(snowflake_schema)
            result = connection.execute(query)
            return result.fetchall()

    def __getattr__(self, name):
        return getattr(self.engine, name)
    

    def get_all_tables_info(self):
        # Logic to retrieve information about all tables
        with self.engine.connect() as connection:
            query = """
                SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = '{}'
                ORDER BY TABLE_NAME, COLUMN_NAME""".format(snowflake_schema)
            result = connection.execute(query)
            return pd.DataFrame(result.fetchall(), columns=['Table Name', 'Column Name', 'Data Type'])

# Create a SQLAlchemy engine for Snowflake
engine = create_engine(URL(
    user=snowflake_user,
    password=snowflake_password,
    account=snowflake_account,
    warehouse=snowflake_warehouse,
    database=snowflake_database,
    schema=snowflake_schema,
    role=snowflake_role
))

# Wrap the engine with the custom wrapper
wrapped_engine = CustomEngineWrapper(engine)

# Initialize the Langchain chain for SQL query generation
chat_model = ChatOpenAI(api_key=openai_api_key, temperature=0)
chain = create_sql_query_chain(chat_model, wrapped_engine)

# Streamlit interface
st.title('Natural Language to SQL Query')

# Check if 'session_data' is in the session state, if not initialize it
if 'session_data' not in st.session_state:
    st.session_state.session_data = {
        'table_names': [],
        'selected_table': None,
        'response': '',
        'table_definition': None  # Added a new key for table definition
    }

# Create a button to fetch and display table names
if st.button('Fetch Table Names'):
    try:
        # Retrieve table names from the schema
        with wrapped_engine.connect() as connection:
            query = f"SHOW TABLES IN SCHEMA {snowflake_schema}"
            result = connection.execute(query)
            table_names = [row[1] for row in result.fetchall()]

        # Store the table names in the session
        st.session_state.session_data['table_names'] = table_names

    except Exception as e:
        st.write("Error in fetching table names:", e)

# Use the session state to select a table
selected_table = st.selectbox("Select a table:", st.session_state.session_data['table_names'])


# Add a button to fetch and display the table definition when a table is selected
if selected_table:
    st.write(f"Table Definition for '{selected_table}':")
    try:
        with wrapped_engine.connect() as connection:
            # Retrieve table information for the selected table
            table_info = wrapped_engine.get_table_info([selected_table])

            # Generate the SQL CREATE TABLE statement
            create_table_sql = f"CREATE OR REPLACE TABLE {snowflake_schema}.{selected_table} (\n"
            for row in table_info:
                column_name, data_type = row[1], row[2]
                create_table_sql += f"\t{column_name} {data_type},\n"
            create_table_sql = create_table_sql.rstrip(',\n') + "\n);"

            st.code(create_table_sql, language='sql')  # Display the SQL code
        st.session_state.session_data['table_definition'] = create_table_sql  # Store the table definition in session
    except Exception as e:
        st.write("Error in fetching table definition:", e)


# Allow user to enter a query for the selected table
user_input = st.text_area("Enter your query in natural language:")

# Add a button to fetch and display the table definition when a table is selected



if st.button('Generate SQL'):
    # Generate SQL query based on user input and selected table
    st.session_state.session_data['response'] = chain.invoke({"question": user_input, "selected_table": selected_table})

# Use the session state for the text input's default value
edited_response = st.text_input("Edit SQL Response", value=st.session_state.session_data['response'])

if st.button('Run SQL Query'):
    try:
        with wrapped_engine.connect() as connection:
            # Execute the edited response
            results = connection.execute(edited_response).fetchall()
            df = pd.DataFrame(results)
            st.table(df)
    except Exception as e:
        st.write("Error in executing query:", e)
