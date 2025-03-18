from utils123456 import *
initconfig()
loadconfig()

###############
# PAGE CONFIG #
###############
st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

#################
# SESSION STATE #
#################
# USERNAME
if 'username' not in st.session_state: st.session_state['username'] = None

###
#
###

if st.session_state['username'] != None and st.session_state['username'] in ['Gates','Pomm']:
    # TITLE
    st.title("🛠️ Admin Console")  


elif st.session_state['username'] != None and st.session_state['username'] not in ['Gates','Pomm']:
    st.header("You are not authorized to view this page")
    if st.button('Go back to the Login page'):
        st.switch_page('Login.py')

else:
    st.header("Go back to the Login page")
    if st.button('Login'):
        st.switch_page('Login.py')