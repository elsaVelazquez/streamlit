# example_prompts1.py
import streamlit as st

SCHEMA_PATH = st.secrets.get("SCHEMA_PATH", "FROSTY_SAMPLE.CHATBOT")
QUALIFIED_TABLE_NAME = f"{SCHEMA_PATH}.Synthetic_Sales_Data"
TABLE_DESCRIPTION = """
This table has various metrics for financial entities (also referred to as banks) since 1983.
The user may describe the entities interchangeably as banks, financial institutions, or financial entities.
"""

METADATA_QUERY = f"SELECT \"VARIABLE_NAME\", DEFINITION FROM {SCHEMA_PATH}.Synthetic_Sales_Data";

GEN_SQL = """
You will be acting as an AI Snowflake SQL Expert named Frosty.
Your goal is to give correct, executable sql query to users.
You will be replying to users who will be confused if you don't respond in the character of Frosty.
You are given one table, the table name is in <tableName> tag, the columns are in <columns> tag.
The user will ask questions, for each question you should respond and include a sql query based on the question and the table. 

{context}

Here are 6 critical rules for the interaction you must abide:
<rules>
1. You MUST MUST wrap the generated sql code within ``` sql code markdown in this format e.g
```sql
(select 1) union (select 2)
```
2. If I don't tell you to find a limited set of results in the sql query or question, you MUST limit the number of responses to 10.
3. Text / string where clauses must be fuzzy match e.g ilike %keyword%
4. Make sure to generate a single snowflake sql code, not multiple. 
5. You should only use the table columns given in <columns>, and the table given in <tableName>, you MUST NOT hallucinate about the table names
6. DO NOT put numerical at the very front of sql variable.
</rules>

Don't forget to use "ilike %keyword%" for fuzzy match queries (especially for VARIABLE_NAME column)
and wrap the generated sql code with ``` sql code markdown in this format e.g:
```sql
(select 1) union (select 2)
```

For each question from the user, make sure to include a query in your response.

Now to get started, please briefly introduce yourself, describe the table at a high level, and share the available metrics in 2-3 sentences.
Then provide 3 example questions using bullet points.
"""

@st.cache_data(show_spinner="Loading Frosty's context...")
def get_table_context(table_names: list, metadata_query: str = None):
    table_contexts = []
    for table_name in table_names:
        try:
            table = table_name.split(".")
            conn = st.connection("snowflake")
            columns = conn.cursor().execute(f"""
                SELECT COLUMN_NAME, DATA_TYPE FROM {table[0].upper()}.INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = '{table[1].upper()}' AND TABLE_NAME = '{table[2].upper()}'
                """).fetchall()
            columns = "\n".join(
                [
                    f"- **{column_name}**: {data_type}"
                    for column_name, data_type in columns
                ]
            )
            context = f"""
            Here is the table name <tableName> {'.'.join(table)} </tableName>

            Here are the columns of the {'.'.join(table)}

            <columns>\n\n{columns}\n\n</columns>
            """
            if metadata_query:
                metadata = conn.query(metadata_query, show_spinner=False)
                metadata = "\n".join(
                    [
                        f"- **{metadata['VARIABLE_NAME'][i]}**: {metadata['DEFINITION'][i]}"
                        for i in range(len(metadata["VARIABLE_NAME"]))
                    ]
                )
                # context = context + f"\n\nAvailable variables by VARIABLE_NAME:\n\n{metadata}"
            table_contexts.append(context)
        except Exception as e:
            table_contexts.append(f"Failed to fetch data for table: {table_name}. Error: {str(e)}")
    return table_contexts

def get_user_friendly_table_description(table_names: list):
    table_descriptions = []
    for table_name in table_names:
        table = table_name.split(".")
        conn = st.connection("snowflake")
        columns = conn.cursor().execute(f"""
            SELECT COLUMN_NAME FROM {table[0].upper()}.INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = '{table[1].upper()}' AND TABLE_NAME = '{table[2].upper()}'
            """).fetchall()
        columns = ", ".join(column_name for column_name, in columns)
        description = f"""
    The available metrics in the {table_name} table are {columns}.

    Here are three example questions you can ask me:

    "What is the total sales value in a specific city and year?"
    "Can you give me the sales data for a specific variable and year?"
    "Which entity had the highest sales value in a particular state?"
        """
        table_descriptions.append(description)
    return table_descriptions

def get_system_prompt():
    table_names = ['FROSTY_SAMPLE.CHATBOT.Synthetic_Sales_Data', 'FROSTY_SAMPLE.CHATBOT.Synthetic_Retail_Data']
    
    table_contexts = get_table_context(
        table_names=table_names,
        metadata_query=METADATA_QUERY
    )
    # Join all table contexts with a separator
    all_table_contexts = "\n---\n".join(table_contexts)
    
    return GEN_SQL.format(context=all_table_contexts)

# do `streamlit run prompts.py` to view the initial system prompt in a Streamlit app
if __name__ == "__main__":
    st.header("System prompt for Frosty")
    st.markdown(get_system_prompt())

