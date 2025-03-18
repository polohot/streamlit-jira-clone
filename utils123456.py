import streamlit as st
import datetime
import os
import json
import pathlib
import glob
import sqlite3
import zipfile
import pandas as pd
import numpy as np
from streamlit_quill import st_quill

# if 'connsql' not in st.session_state or st.session_state['connsql'] == None:
#     connsql = sqlite3.connect(f"{st.session_state['ITEM_DIRECTORY']}allItems.db")


#################
# SESSION STATE #
#################

def initconfig():
    # CONFIG
    if 'ITEM_DIRECTORY' not in st.session_state: st.session_state['ITEM_DIRECTORY'] = None
    if 'PASSWORD_DICT' not in st.session_state: st.session_state['PASSWORD_DICT'] = {}
    if 'ADMIN_LIST' not in st.session_state: st.session_state['ADMIN_LIST'] = None
    # USERNAME
    if 'username' not in st.session_state: st.session_state['username'] = None
    # INIT SQL
    if 'connsql' not in st.session_state: st.session_state['connsql'] = None
    # LS FOR FORM
    if 'lsSTATUS' not in st.session_state: st.session_state['lsSTATUS'] = ['📋 Opened', '🔄 In Progress', '✅ Completed', '❌ Cancelled', '⏳ On Hold']
    if 'lsMEMBERS' not in st.session_state: st.session_state['lsMEMBERS'] = ['Kwang','Long','Minmin','Gates','Pomm']
    if 'lsPRIORITY' not in st.session_state: st.session_state['lsPRIORITY'] = ["🟢 Low", "🟡 Medium", "🔴 High"]
    # P1
    if 'dfALL' not in st.session_state: st.session_state['dfALL'] = pd.DataFrame()
    if 'dfTAB1' not in st.session_state: st.session_state['dfTAB1'] = pd.DataFrame()
    if 'dfTAB2' not in st.session_state: st.session_state['dfTAB2'] = pd.DataFrame() 
    if 'dfTAB3' not in st.session_state: st.session_state['dfTAB3'] = pd.DataFrame() 
    if 'dfTAB4' not in st.session_state: st.session_state['dfTAB4'] = pd.DataFrame() 
    if 'eventT1' not in st.session_state: st.session_state['eventT1'] = None
    if 'eventT2' not in st.session_state: st.session_state['eventT2'] = None
    if 'eventT3' not in st.session_state: st.session_state['eventT3'] = None
    if 'eventT4' not in st.session_state: st.session_state['eventT4'] = None
    # P2 - VIEW ITEM
    if 'viewItemFolder' not in st.session_state: st.session_state['viewItemFolder'] = None
    # P2 - TOPIC / LOG DICT
    if 'dictTOPIC0' not in st.session_state: st.session_state['dictTOPIC0'] = None
    if 'dictTOPIC1' not in st.session_state: st.session_state['dictTOPIC1'] = None
    if 'dictLOG' not in st.session_state: st.session_state['dictLOG'] = None

####################
# LOAD CONFIG FILE #
####################

def loadconfig():
    st.session_state['ITEM_DIRECTORY'] = './itemHistory/V1/'
    st.session_state['PASSWORD_DICT'] = {
        'passlong':'Long',
        'passgates':'Gates',
        'passkwang':'Kwang',
        'passminmin':'Minmin',
        'passpomm':'Pomm'}
    st.session_state['ADMIN_LIST'] = ['Gates','Pomm']

