import streamlit as st
import datetime
import os
import json
import pathlib
import pandas as pd
import numpy as np
from streamlit_quill import st_quill

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
if 'dictTOPIC' not in st.session_state:
    st.session_state['dictTOPIC'] = None
if 'dictLOG' not in st.session_state:
    st.session_state['dictLOG'] = None

###########
# CONTENT #
###########

@st.dialog('Notice')
def submitOK(foldername):
    foldername = foldername.replace('---','-')
    st.write(f"Item successfully added!")
    st.write(f"Item number: **{foldername}**")
    if st.button('👀 View Item'):
        st.switch_page('pages/P2 👀 View Item.py')

if st.session_state['username'] != None:
    # TITLE
    st.title("➕ Add Item")

    # FORM
    with st.form('formAddItem', clear_on_submit=False, enter_to_submit=False):
        formTopic = st.text_input("📌 **:red[Topic (Text)]**", key="formTopic")   
        colform1, colform2 = st.columns(2)
        with colform1:
            formAnalyticPICmain = st.selectbox("🧑‍💻 **:red[Analytic PIC Main (Dropdown)]**", ['---'] + st.session_state['lsMEMBERS'], index=0)  
            formPriority = st.selectbox("🚦 **:red[Priority (Dropdown)]**", ['---'] + st.session_state['lsPRIORITY'], index=0)  
            formRequestType = st.selectbox("🏷️ **:red[Request Type (Dropdown)]**", ['---',"✨ New Request", "🛠️ Issue"], index=0)          
        with colform2:
            formCurrAssignedTo = st.selectbox("🧑‍💻 **:red[Currently Assigned To (Dropdown)]**", ['---'] + st.session_state['lsMEMBERS'], index=0)  
            formAnalyticPICsupport = st.text_input("👥 Analytic PIC Support (Text)")   
            formRequestor = st.text_input("👤 Requestor (Text)") 

        formDescription = st.text_area("📋 **:red[Description (Text)]**")
        #formDescription = st_quill("", html=True, readonly=False)
        colform3, colform4 = st.columns(2)
        with colform3:
            formRequestDate = st.date_input("📅 Request Date (Date)", value=datetime.datetime.today(), format="YYYY-MM-DD")     
            formDueDate = st.text_input("📅 Due Date (Text)")  
            formStatus = st.selectbox("📌 Status", ['📋 Opened'], index=0)       
            formCreator = st.selectbox("👤 Creator", [st.session_state['username']], index=0) 
        with colform4:
            formBenefit = st.text_input("💡 Benefit (Text)")
            formCSSCPIC = st.text_input("👨‍💼 CSSC PIC (Text)")  
            formCountry = st.text_input("🌍 Country (Text)")  
            formBL = st.text_input("📊 BL (Text)")

        # SUBMIT
        submitted = st.form_submit_button("Submit")

    # VALIDATE
    if submitted:
        error = 0
        if not formTopic or not formDescription:
            error = 1
            st.error("Topic and Description cannot be blank!")
        if formAnalyticPICmain == '---':
            error = 1
            st.error("Select Analytic PIC Main!")
        if formCurrAssignedTo == '---':
            error = 1
            st.error("Select Currently Assigned To!")
        if formPriority == '---':
            error = 1
            st.error("Select Priority!")
        if formRequestType == '---':
            error = 1
            st.error("Select Request Type!")  

        if error == 0:
            ### PREP JSON
            # CLEAN [formPriority]
            if 'Low' in formPriority: formPriority = 'Low'
            elif 'Medium' in formPriority: formPriority = 'Medium'
            elif 'High' in formPriority: formPriority = 'High'
            # CLEAN [formRequestType]
            if 'New Request' in formRequestType: formRequestType = 'NEW_REQUEST'
            elif 'Issue' in formRequestType: formRequestType = 'ISSUE'
            # CLEAN [formStatus]
            formStatus = 'Opened'
            # BUILD JSON
            now = datetime.datetime.now()
            jsonMetadata = {
                "sysFolderName": None, # CHECK WHEN CREATE
                "sysCreateDttm": now.strftime("%Y-%m-%d %H:%M:%S"),
                "sysCreateDttm2": now.strftime("%Y%m%d_%H%M%S"),
                "sysTopicName": 'TOPIC_' + now.strftime("%Y%m%d_%H%M%S"),
                "sysPath": None,
                "sysUserID": st.session_state['username'],

                "formTopic": formTopic,
                "formAnalyticPICmain": formAnalyticPICmain,
                "formCurrAssignedTo": formCurrAssignedTo,
                "formAnalyticPICsupport": formAnalyticPICsupport,                    
                "formPriority": formPriority,
                "formRequestType": formRequestType,
                "formRequestor": formRequestor,
                "formBenefit": formBenefit,                    
                "formDescription": formDescription,
                "formRequestDate": formRequestDate.strftime("%Y-%m-%d"),
                "formDueDate": formDueDate,
                "formStatus": formStatus,
                "formCreator": formCreator,
                "formCSSCPIC": formCSSCPIC,
                "formCountry": formCountry,
                "formBL": formBL
                }                   
            # GET FILE NAME
            stryyyy = str(now.year)
            lsHistory = [folder.name for folder in pathlib.Path('./itemHistory').iterdir() if folder.is_dir()]
            lsHistory = [x for x in lsHistory if x[:4] == stryyyy]            
            if len(lsHistory) == 0:
                foldername = f"{stryyyy}---000001---{jsonMetadata['formRequestType']}"
            else:
                lsID = [x[7:13] for x in lsHistory]
                maxID = int(max(lsID))
                thisID = maxID + 1     
                thisID = str(thisID).zfill(6)
                foldername = f"{stryyyy}---{thisID}---{jsonMetadata['formRequestType']}"
            jsonMetadata['sysFolderName'] = foldername
            jsonMetadata['sysPath'] = f"./itemHistory/{foldername}/"
            # SAVE JSON
            filepath = jsonMetadata['sysPath']
            filename = jsonMetadata['sysTopicName']
            if not os.path.exists(filepath):
                os.makedirs(filepath) 
            with open(f"{filepath}/{filename}.json", 'w') as outfile:
                json.dump(jsonMetadata, outfile)
            with open(f"{filepath}/LOG_{jsonMetadata["sysCreateDttm2"]}.json", 'w') as outfile:
                json.dump([], outfile)
            # SWITCH
            st.session_state['viewItemFolder'] = foldername
            submitOK(foldername)

    with st.expander('DEBUG'): 
        st.text(st.session_state['viewItemFolder'])
        if 'lsID' in globals(): st.json(lsID)
        if 'maxID' in globals(): st.text(maxID)
        if 'thisID' in globals(): st.text(thisID)
        if 'foldername' in globals(): st.text(foldername)
        if 'jsonMetadata' in globals(): st.json(jsonMetadata)

else:
    st.header("Go back to the Login page")
    if st.button('Login'):
        st.switch_page('Login.py')