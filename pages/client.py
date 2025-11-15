import streamlit as st
from datetime import datetime
import mysql.connector

## removing the sidebar from the streamlit page
hide_sidebar_style = """
    <style>
        [data-testid="stSidebar"] { display: none; }
        [data-testid="stSidebarNav"] { display: none; }
        [data-testid="stHamburgerMenu"] { display: none; }
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

# ---------------------------------------
# creating Database Connection
# ---------------------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="246768@Rag",
        database="project"
    )

# ---------------------------------------
# saving Query into database
# ---------------------------------------
def insert_query(email, phone_number, query_title, query_desc, created_on, state, closed_on):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO queries 
        (email, phone_number, query_title, query_desc, created_on, state, closed_on)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    values = (email, phone_number, query_title, query_desc, created_on, state, closed_on)

    cursor.execute(sql, values)
    conn.commit()

    cursor.close()
    conn.close()


# ---------------------------------------
# creating Streamlit UI
# ---------------------------------------
st.title(" Submit a New Query")

with st.form("query_form"):
    email = st.text_input("Email ID")
    mobile = st.text_input("Mobile Number")
    heading = st.text_input("Query Heading")
    description = st.text_area("Query Description", height=150)

    submit = st.form_submit_button("Submit Query")

if submit:
    # Auto-generated fields
    query_created_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "Open"
    query_closed_time = None  # NULL in MySQL

    try:
        insert_query(email, mobile, heading, description, query_created_time, status, query_closed_time)

        st.success(" Query Submitted Successfully!")
        st.info(f"Created Time: {query_created_time}")
        st.warning("Status: Open")

    except Exception as e:
        st.error(f"Error inserting query: {e}")

if st.button("Login"):
    st.switch_page("login.py")  # redirect to login page