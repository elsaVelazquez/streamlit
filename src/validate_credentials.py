import toml
import snowflake.connector
import streamlit as st  # Change this line

# Load the secrets
secrets = toml.load(".streamlit/secrets.toml")

# Establish a connection
conn = snowflake.connector.connect(
    user=st.secrets["user"]["username"],
    password=st.secrets["user"]["password"],
    account=st.secrets["user"]["account"],
    warehouse=st.secrets["user"]["warehouse"],
    database=st.secrets["user"]["database"],
    schema=st.secrets["user"]["schema"]
)

# Rest of your code...

# Create a cursor object
cur = conn.cursor()

# Now you can use cur to execute queries

conn = st.connection("snowflake")
st.write(conn.connection_parameters)
df = conn.query("select current_warehouse()")
st.write(df)

## Validate OpenAI connection ##
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": "What is Streamlit?"}
  ]
)

st.write(completion.choices[0].message.content)
