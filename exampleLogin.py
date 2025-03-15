import streamlit as st
from datetime import datetime, timedelta
from http.cookies import SimpleCookie

# Define the correct password
PASSWORD_DICT = {'passlong': 'Long',
                 'passgates': 'Gates',
                 'passkwang': 'Kwang',
                 'passminmin': 'Minmin',
                 'passpomm': 'Pomm'}

# Function to set a cookie
def set_cookie(key, value, days_expiry):
    expires_at = (datetime.now() + timedelta(days=days_expiry)).strftime("%a, %d-%b-%Y %H:%M:%S GMT")
    cookie = SimpleCookie()
    cookie[key] = value
    cookie[key]['expires'] = expires_at
    st.query_params(**{key: value})
    st.markdown(f"<script>document.cookie = '{cookie.output(header='', sep='; ')}';</script>", unsafe_allow_html=True)

# Function to get a cookie
def get_cookie(key):
    cookie_string = st.experimental_get_query_params().get(key, [None])[0]
    if cookie_string:
        cookie = SimpleCookie()
        cookie.load(cookie_string)
        return cookie[key].value if key in cookie else None
    return None

# CHECK LOGGED IN ALREADY
username = get_cookie('username')
if username is None:
    # Create a placeholder for the password input
    password_placeholder = st.empty()
    # Get the password input from the user
    password = password_placeholder.text_input("Enter Password:", type="password")
    # Check if the password is correct
    if password in PASSWORD_DICT.keys():
        # Clear the password input and set the cookie
        password_placeholder.empty()
        username = PASSWORD_DICT[password]
        set_cookie('username', username, 7)
        st.rerun()
    elif password != "":
        # Show an error message if the password is incorrect
        st.error("Incorrect password. Please try again.")
else:
    st.header(f"Welcome {username}")
    if st.button('P1 📋 All Items'):
        st.switch_page('./pages/P1 📋 All Items.py')
    if st.button('P2 👀 View Item'):
        st.switch_page('./pages/P2 👀 View Item.py')
    if st.button('P3 ➕ Add Item'):
        st.switch_page('./pages/P3 ➕ Add Item.py')