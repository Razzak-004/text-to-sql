import streamlit as st
from utils import create_db, get_gemini_response, run_query

st.set_page_config(page_title="Text-to-SQL App", layout="centered")
st.title("Text to SQL using Google Gemini")

# Create database if not already created
create_db()

user_input = st.text_input("Ask your question:")

if st.button("Generate SQL and Get Result") and user_input:
    prompt = f"""
You are a SQL expert. Convert the user's question to SQL.
Use table: votes

Question: {user_input}
Only return SQL query.
"""
    sql_query = get_gemini_response(prompt)
    st.code(sql_query, language="sql")

    try:
        result = run_query(sql_query)
        st.dataframe(result)
    except Exception as e:
        st.error(f"Error: {e}")