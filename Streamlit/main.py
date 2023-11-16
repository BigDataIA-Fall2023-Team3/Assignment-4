import streamlit as st
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from langchain.llms import OpenAI
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain

# Load environment variables
load_dotenv()

# Snowflake credentials
snowflake_user = os.getenv('SNOWFLAKE_USER')
snowflake_password = os.getenv('SNOWFLAKE_PASSWORD')
snowflake_account = os.getenv('SNOWFLAKE_ACCOUNT')
snowflake_warehouse = os.getenv('SNOWFLAKE_WAREHOUSE')
snowflake_database = os.getenv('SNOWFLAKE_DATABASE')
snowflake_schema = os.getenv('SNOWFLAKE_SCHEMA')
snowflake_role = os.getenv('SNOWFLAKE_ROLE')

# Create a connection URL using SQLAlchemy
# Create a connection URL using SQLAlchemy
connection_url = URL.create(
    "snowflake",
    username=snowflake_user,
    password=snowflake_password,
    host=snowflake_account,
    database=snowflake_database,
    query={
        'warehouse': snowflake_warehouse,
        'role': snowflake_role,
        'schema': snowflake_schema  # Moved schema here
    }
)


# Create an engine
engine = create_engine(connection_url)

# Initialize the LangChain with OpenAI client
llm = OpenAI(api_key=os.getenv('OPENAI_API_KEY'), temperature=0, verbose=True)
db = SQLDatabase(engine)  # Update this line to use the engine directly
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

def get_snowflake_conn():
    # Connect to Snowflake using the engine
    return engine.connect()

def fetch_schema():
    with get_snowflake_conn() as conn:
        query = "SELECT TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = %(schema)s"
        result = conn.execute(query, {'schema': snowflake_schema})
        schema_details = result.fetchall()

    schema_info = {}
    for table, column in schema_details:
        if table not in schema_info:
            schema_info[table] = []
        schema_info[table].append(column)
    return schema_info

def generate_sql_query(prompt):
    response = db_chain.run(prompt)
    return response



def run_query(query):
    with get_snowflake_conn() as conn:
        result = conn.execute(query)
        rows = result.fetchall()
    return rows

# Streamlit interface
st.title('Natural Language to SQL Query using LangChain')

schema_info = fetch_schema()
user_input = st.text_area("Enter your query in natural language:")

if st.button('Generate SQL'):
    sql_query = generate_sql_query(user_input)
    st.text("Generated SQL Query:")
    st.write(sql_query)

    if st.button('Run SQL Query'):
        query_results = run_query(sql_query)
        st.text("Query Results:")
        st.write(query_results)
