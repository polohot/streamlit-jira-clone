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

    # List all config files
    config_files = [f for f in os.listdir('./config/') if f.endswith('.config')]
    config_files.sort(reverse=True)
    #st.json(config_files)
    # SELECT
    selected_file = st.selectbox('Select a config file', config_files)
    # SHOW SELECTED
    if selected_file:
        with open(f"./config/{selected_file}", 'r') as file:
            datatxt = file.read()
        config_txt = st.text_area('config content',datatxt,height=300)
        if st.button('Save'):
            # VALIDATION
            error = 0           
            try:
                exec(config_txt)
                st.text(config_txt)
                st.text(ITEM_DIRECTORY)
                st.text(PASSWORD_DICT)
                st.text(ADMIN_LIST)
            except Exception as emsg:
                error = 1
            # SAVE
            if error == 0:
                # SAVE
                dttmstr = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                st.text(dttmstr)
                with open(f"./config/{dttmstr}.config", "w") as text_file:
                    text_file.write(config_txt)
            else:
                st.error(emsg)

elif st.session_state['username'] != None and st.session_state['username'] not in ['Gates','Pomm']:
    st.header("You are not authorized to view this page")
    if st.button('Go back to the Login page'):
        st.switch_page('Login.py')

else:
    st.header("Go back to the Login page")
    if st.button('Login'):
        st.switch_page('Login.py')