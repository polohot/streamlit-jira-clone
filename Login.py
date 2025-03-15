import streamlit as st
import datetime
import os
import json
import pathlib
import pandas as pd
import numpy as np
from streamlit_quill import st_quill

###############
# PAGE CONFIG #
###############

st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

#################
# SESSION STATE #
#################

# USERNAME
if 'username' not in st.session_state:
    st.session_state['username'] = None
# LS FOR FORM
if 'lsSTATUS' not in st.session_state:
    st.session_state['lsSTATUS'] = ['📋 Opened', '🔄 In Progress', '✅ Completed', '❌ Cancelled', '⏳ On Hold']
if 'lsMEMBERS' not in st.session_state:
    st.session_state['lsMEMBERS'] = ['Kwang','Long','Minmin','Gates','Pomm']
if 'lsPRIORITY' not in st.session_state:
    st.session_state['lsPRIORITY'] = ["🟢 Low", "🟡 Medium", "🔴 High"]
# P1
if 'dfALL' not in st.session_state:
    st.session_state['dfALL'] = pd.DataFrame()
if 'dfTAB1' not in st.session_state:
    st.session_state['dfTAB1'] = pd.DataFrame()
if 'dfTAB2' not in st.session_state:
    st.session_state['dfTAB2'] = pd.DataFrame() 
if 'dfTAB3' not in st.session_state:
    st.session_state['dfTAB3'] = pd.DataFrame() 
if 'dfTAB4' not in st.session_state:
    st.session_state['dfTAB4'] = pd.DataFrame() 
if 'eventT1' not in st.session_state:
    st.session_state['eventT1'] = None
if 'eventT2' not in st.session_state:
    st.session_state['eventT2'] = None
if 'eventT3' not in st.session_state:
    st.session_state['eventT3'] = None
if 'eventT4' not in st.session_state:
    st.session_state['eventT4'] = None
# P2 - VIEW ITEM
if 'viewItemFolder' not in st.session_state:
    st.session_state['viewItemFolder'] = None
# P2 - TOPIC / LOG DICT
if 'dictTOPIC0' not in st.session_state:
    st.session_state['dictTOPIC0'] = None
if 'dictTOPIC1' not in st.session_state:
    st.session_state['dictTOPIC1'] = None
if 'dictLOG' not in st.session_state:
    st.session_state['dictLOG'] = None

##################
# AUTHENTICATION #
##################

# Define the correct password
PASSWORD_DICT = {'passlong':'Long',
                 'passgates':'Gates',
                 'passkwang':'Kwang',
                 'passminmin':'Minmin',
                 'passpomm':'Pomm'}

# CHECK LOGGED IN ALREADY
if st.session_state['username'] == None:
    # Create a placeholder for the password input
    password_placeholder = st.empty()    
    # Get the password input from the user
    password = password_placeholder.text_input("Enter Password:", type="password")    
    # Check if the password is correct
    if password in PASSWORD_DICT.keys():
        # Clear the password input and return True
        password_placeholder.empty()
        st.session_state['username'] = PASSWORD_DICT[password]
        st.rerun()
    elif password != "":
        # Show an error message if the password is incorrect
        st.error("Incorrect password. Please try again.")
else:
    st.header(f"Welcome {st.session_state['username']}")
    if st.button('P1 📋 All Items'):
        st.switch_page('./pages/P1 📋 All Items.py')
    if st.button('P2 👀 View Item'):
        st.switch_page('./pages/P2 👀 View Item.py')
    if st.button('P3 ➕ Add Item'):
        st.switch_page('./pages/P3 ➕ Add Item.py')


