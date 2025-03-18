from utils123456 import *
initconfig()
loadconfig()

###############
# PAGE CONFIG #
###############
st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

##################
# AUTHENTICATION #
##################

# CHECK LOGGED IN ALREADY
if st.session_state['username'] == None:  
    # Create a placeholder for the password input
    password_placeholder = st.empty()    
    # Get the password input from the user
    password = password_placeholder.text_input("Enter Password:", type="password")    
    # Check if the password is correct
    if password in st.session_state['PASSWORD_DICT'].keys():
        # Clear the password input and return True
        password_placeholder.empty()
        st.session_state['username'] = st.session_state['PASSWORD_DICT'][password]
        st.rerun()
    elif password != "":
        # Show an error message if the password is incorrect
        st.error("Incorrect password. Please try again.")
else:
    st.header(f"Welcome :blue[{st.session_state['username']}]")
    if st.button('P1 📋 All Items'):
        st.switch_page('./pages/P1 📋 All Items.py')
    if st.button('P2 👀 View Item'):
        st.switch_page('./pages/P2 👀 View Item.py')
    if st.button('P3 ➕ Add Item'):
        st.switch_page('./pages/P3 ➕ Add Item.py')


