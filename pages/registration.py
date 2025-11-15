import streamlit as st
import mysql.connector
import pandas as pd
import hashlib

## removing the sidebar from the streamlit page
hide_sidebar_style = """
    <style>
        [data-testid="stSidebar"] { display: none; }
        [data-testid="stSidebarNav"] { display: none; }
        [data-testid="stHamburgerMenu"] { display: none; }
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

# Function to get DB connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="246768@Rag",
        database="project"
    )

# Function to hash passwords
def hashed_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Streamlit registration page
st.title("Sign Up")

with st.form(key="registration_form"):
    username = st.text_input("USER_NAME")
    name = st.text_input("NAME")
    email = st.text_input("EMAIL")
    number = st.text_input("MOBILE NUMBER")
    password = st.text_input("PASSWORD", type="password")
    role = st.selectbox("ROLE", ["Client", "Support"])
    submit = st.form_submit_button(label="SUBMIT")

if submit:
    if not username or not name or not email or not number or not password:
        st.error(" Please fill in all fields before submitting.")
    elif not number.isdigit():
        st.error(" Please enter a valid mobile number (numbers only).")
    else:
        try:
            # Connect to the DB here
            mydb = get_connection()
            if mydb.is_connected():
                st.success("Connected to MySQL database.")
            else:
                st.error("Failed to connect to MySQL database.")
            
            cursor = mydb.cursor()

            # Check if username/email exists
            cursor.execute("SELECT * FROM user WHERE username = %s OR email = %s", (username, email))
            existing_user = cursor.fetchone()

            if existing_user:
                st.error(" Username or Email already exists. Please choose another.")
            else:
                # Hash password
                hashed_pw = hashed_password(password)

                # Insert user
                query = """
                    INSERT INTO user (username, email, name, phone_number, hashed_password, role)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                values = (username, email, name, number, hashed_pw, role)
                cursor.execute(query, values)
                mydb.commit()

                st.success("✅ Registration Successful!")

                # Display entered data
                reg_data = {
                    "Username": username,
                    "Name": name,
                    "Email": email,
                    "Phone": number,
                    "Role": role
                }
                st.write("### Your Information:")
                st.table(pd.DataFrame([reg_data]))

        except mysql.connector.Error as e:
            st.error(f"❌ Database Error: {e}")

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'mydb' in locals() and mydb.is_connected():
                mydb.close()
else:
    st.info("ℹ️ Please provide the requested information and click **Submit**.")

    st.write("Already have an account?")
if st.button("Login"):
    st.switch_page("login.py")  # redirect to login page