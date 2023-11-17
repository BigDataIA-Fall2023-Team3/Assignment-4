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

user_input = st.text_area("Enter your query in natural language:")

# Check if 'response' is in the session state, if not initialize it
if 'response' not in st.session_state:
    st.session_state.response = ''

if st.button('Generate SQL'):
    st.session_state.response = chain.invoke({"question": user_input})
    # This will re-run the script and preserve the response in the session state

# Use the session state for the text input's default value
edited_response = st.text_input("Edit SQL Response", value=st.session_state.response)

if st.button('Run SQL Query'):
    try:
        with engine.connect() as connection:
            # Execute the edited response
            results = connection.execute(edited_response).fetchall()
            df = pd.DataFrame(results)
            st.table(df)     
    except Exception as e:
        st.write("Error in executing query:", e)

