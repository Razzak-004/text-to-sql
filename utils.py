import sqlite3
import pandas as pd
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def create_db():
    df = pd.read_csv("indiavotes.csv")
    conn = sqlite3.connect("indiavotes.db")
    df.to_sql("votes", conn, if_exists="replace", index=False)
    conn.close()

def run_query(query):
    conn = sqlite3.connect("indiavotes.db")
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    col_names = [description[0] for description in cursor.description]
    conn.close()
    return pd.DataFrame(rows, columns=col_names)

def get_gemini_response(prompt):
    model = genai.GenerativeModel(model_name="models/gemini-pro")
    response = model.generate_content(prompt)
    return response.text