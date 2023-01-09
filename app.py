# streamlit_app.py

import streamlit as st
from supabase import create_client, Client

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    url = st.secrets["supabase_url"]
    key = st.secrets["supabase_key"]
    return create_client(url, key)

supabase = init_connection()


# allow user to create account with google account using supabase module

# allow user to sign out using supabase module
def sign_out():
    if st.button("Sign out"):
        user = supabase.auth.sign_out()
        st.write(user)

# allow user to reset password using supabase module
def reset_password():
    email = st.text_input("Email")
    if st.button("Reset password"):
        user = supabase.auth.api.reset_password_for_email(email)

# allow user to update password using supabase module
def update_password():
    new_password = st.text_input("New password", type="password")
    if st.button("Update password"):
        user = supabase.auth.update(email=email, password=password, data={"password": new_password})

# allow user to update email using supabase module
def update_email():
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    new_email = st.text_input("New email")
    if st.button("Update email"):
        user = supabase.auth.update(email=email, password=password, data={"email": new_email})

# allow user to update user data using supabase module
def update_user_data():
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    new_data = st.text_input("New data")
    if st.button("Update user data"):
        user = supabase.auth.update(email=email, password=password, data={"user_metadata": new_data})

    


# create wine table on supabase
def create_wine_table():
    if st.button("Create wine table"):
        wine_table = supabase.create_table("wine", schema="id SERIAL PRIMARY KEY, name TEXT, year INTEGER, grapes TEXT, country TEXT, region TEXT, description TEXT, picture BYTEA")
        st.write(wine_table)

# Allow user to upload photo to supabase storage
def upload_photo():
    file = st.file_uploader("Upload a file")
    if file is not None:
        file_details = {"file": file, "name": file.name, "size": file.size}

        # Upload file to Supabase wine table
        if st.button("Upload photo"):
            photo = supabase.storage.from_("wine").upload(file_details["name"], file_details["file"])


# # Perform query.
# # Uses st.experimental_memo to only rerun when the query changes or after 10 min.
# @st.experimental_memo(ttl=600)
# def run_query():
#     return supabase.table("mytable").select("*").execute()

# rows = run_query()

# # Print results.
# for row in rows.data:
#     st.write(f"{row['name']} has a :{row['pet']}:")

# create login screen with title "Wine Wednesday" and subtitle "Sign in to your account" with functionality to create and sign into account


def login_page():
    st.title("Wine Wednesday")
    st.subheader("Sign in to your account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign up"):
        user = supabase.auth.sign_up(email=email, password=password)
        st.write(user)
        st.write(f"Signed up {email}")

    if st.button("Sign in"):
        user = supabase.auth.sign_in(email=email, password=password)
        st.session_state['logged_in'] = True
    # sign_out()
    # reset_password()
    # update_password()
    # update_email()
    # update_user_data()

# create page that allows user to add wine to database
def app_page():
    create_wine_table()
    upload_photo()

try:
    if st.session_state['logged_in']:
        st.success('Logged in')
        app_page()

        # if st.button("Restart"):
        # 	init_connection()
    else:
        login_page()
except:
    st.session_state['logged_in'] = False
    login_page()