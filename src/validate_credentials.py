# validate_credentials.py
import streamlit as st
from openai import OpenAI
import snowflake.connector

# Singleton for Snowflake connection
@st.cache_resource
def get_snowflake_connection():
    return snowflake.connector.connect(
        user=st.secrets['connections.snowflake']['user'],
        password=st.secrets['connections.snowflake']['password'],  # Correct way to access password
        account=st.secrets['connections.snowflake']['account'],
        warehouse=st.secrets['connections.snowflake']['warehouse'],
        role=st.secrets['connections.snowflake']['role'],
    )
# Singleton for OpenAI client
@st.cache_resource
def get_openai_client():
    return OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

## Validate Snowflake connection ##
conn = get_snowflake_connection()  # Use the singleton function

# Create a cursor object
cur = conn.cursor()

# Now you can use cur to execute queries
# ... Your SQL queries ...

## Validate OpenAI connection ##
client = get_openai_client()  # Use the singleton function

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": "What is Streamlit?"}
  ]
)

st.write(completion.choices[0].message.content)
