# example_prompts1.py
import streamlit as st

SCHEMA_PATH = st.secrets.get("SCHEMA_PATH", "FROSTY_SAMPLE.CHATBOT")

table_name = "" # initialize variable

QUALIFIED_TABLE_NAME = f"{SCHEMA_PATH}.{table_name}"

TABLE_DESCRIPTION = """
This table has various metrics for financial entities (also referred to as banks) since 1983.
The user may describe the entities interchangeably as banks, financial institutions, or financial entities.
"""

METADATA_QUERY = f'SELECT "VARIABLE_NAME", DEFINITION FROM {SCHEMA_PATH}.{table_name}'

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

Now to get started, please briefly introduce yourself, describe each of the tables 
at a high level in 2-3 sentences and include 3 example questions using bullet points for each table.
"""

@st.cache_data(show_spinner="Loading Frosty's context...")
def get_table_context(tables: dict):
    table_contexts = []
    for table_name, table_description in tables.items():
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
            metadata_query = f'SELECT "VARIABLE_NAME", DEFINITION FROM {table_name}'
            metadata = conn.query(metadata_query, show_spinner=False)
            metadata = "\n".join(
                [
                    f"- **{metadata['VARIABLE_NAME'][i]}**: {metadata['DEFINITION'][i]}"
                    for i in range(len(metadata["VARIABLE_NAME"]))
                ]
            )
            context = f"""
            Here is the table name <tableName> {'.'.join(table)} </tableName>
            Description: {table_description}

            Here are the columns of the {'.'.join(table)}

            <columns>\n\n{columns}\n\n</columns>
            """
            table_contexts.append(context)
            # st.write(context)
        except Exception as e:
            table_contexts.append(f"Failed to fetch data for table: {table_name}. Error: {str(e)}")
    return table_contexts

def get_system_prompt():
    table_names = {
        'FROSTY_SAMPLE.CHATBOT.Synthetic_Sales_Data': 'This table has various metrics for financial entities (also referred to as banks) since 2020. The user may describe the entities interchangeably as banks, financial institutions, or financial entities.',
        'FROSTY_SAMPLE.CHATBOT.Synthetic_Retail_Data': 'This table has various metrics for retail entities (also referred to as stores) since 2020. The user may describe the entities interchangeably as stores, retail institutions, or retail entities, and ranking data as traffic.'
    }

    table_contexts = get_table_context(tables=table_names)
    # Join all table contexts with a separator
    all_table_contexts = "\n---\n".join(table_contexts)
    
    return GEN_SQL.format(context=all_table_contexts)

# do `streamlit run prompts.py` to view the initial system prompt in a Streamlit app
if __name__ == "__main__":
    st.header("System prompt for Frosty")
    st.markdown(get_system_prompt())
