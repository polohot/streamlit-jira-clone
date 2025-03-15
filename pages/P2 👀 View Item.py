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
if 'dictTOPIC0' not in st.session_state:
    st.session_state['dictTOPIC0'] = None
if 'dictTOPIC1' not in st.session_state:
    st.session_state['dictTOPIC1'] = None
if 'dictLOG' not in st.session_state:
    st.session_state['dictLOG'] = None

###########
# CONTENT #
###########

@st.dialog('Save Unsuccessful')
def noChange():
    st.write(f"No Change Detected!")

st.markdown("""
<style>
    .stTextInput input[aria-label="📌 **:red[Topic]**"] {
        background-color: #E8F2FC;
        color: #0E4B87;
        font-size: 20px;
        font-weight: bold;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)
    
def updateState(viewItemFolder):
    alljson = list(pathlib.Path(f"./itemHistory/{viewItemFolder}").rglob('*'))
    alljson = [str(x) for x in alljson]
    lsTOPIC = [x for x in alljson if 'TOPIC' in str(x)]
    lsLOG = [x for x in alljson if 'LOG' in str(x)]
    maxTOPIC = max(lsTOPIC)
    maxLOG = max(lsLOG)
    # LOAD MAX TOPIC0
    with open(maxTOPIC, 'r') as f:
        st.session_state['dictTOPIC0'] = json.load(f)
    with open(maxTOPIC, 'r') as f:
        st.session_state['dictTOPIC1'] = json.load(f)
    # LOAD MAX LOG
    with open(maxLOG, 'r') as f:
        st.session_state['dictLOG'] = json.load(f)



if st.session_state['username'] != None:
    # TITLE
    st.title("👀 View Item")
    # IF ALREADY HAVE ITEM
    if st.session_state['viewItemFolder'] != None:
        ######################
        # SHOW CURRENT TOPIC #
        ######################
        # PULL JSON
        updateState(st.session_state['viewItemFolder'])
        # SHOW FOLDER & REQUEST DATE & CREATOR
        colView1, colView2 = st.columns(2)
        with colView1: 
            st.markdown(f"🔢 Item Id: **{'-'.join(st.session_state['viewItemFolder'].split('---')[:2])}**")
            st.markdown(f"🏷️ Request Type: **{st.session_state['dictTOPIC0']['formRequestType']}**")
        with colView2: 
            st.markdown(f"📅 Created Date: **{st.session_state['dictTOPIC0']['sysCreateDttm']}**")    
            # st.markdown(f"📅 Request Date: **{st.session_state['dictTOPIC0']['formRequestDate']}**")    
            st.markdown(f"👤 Creator: **{st.session_state['dictTOPIC0']['formCreator']}**") 
        # SHOW TOPIC (1)
        st.session_state['dictTOPIC1']['formTopic1'] = st.text_input("📌 **:red[Topic]**", value=st.session_state['dictTOPIC1']['formTopic'])
        colView3, colView4 = st.columns(2)
        with colView3:
            # PIC MAIN
            lsMEMBERSindex = st.session_state['lsMEMBERS'].index(st.session_state['dictTOPIC1']['formAnalyticPICmain'])
            st.session_state['dictTOPIC1']['formAnalyticPICmain'] = st.selectbox("🧑‍💻 **:red[Analytic PIC Main]**", st.session_state['lsMEMBERS'], index=lsMEMBERSindex) 
            # PRIORITY
            lsPRIORITYindex = next(i for i, s in enumerate(st.session_state['lsPRIORITY']) if st.session_state['dictTOPIC1']['formPriority'] in s)
            st.session_state['dictTOPIC1']['formPriority'] = st.selectbox("🚦 **:red[Priority]**", st.session_state['lsPRIORITY'], index=lsPRIORITYindex)
            # STATUS
            lsSTATUSindex = next(i for i, s in enumerate(st.session_state['lsSTATUS']) if st.session_state['dictTOPIC1']['formStatus'] in s)
            st.session_state['dictTOPIC1']['formStatus'] = st.selectbox("📌 **:red[Status]**", st.session_state['lsSTATUS'], index=lsSTATUSindex)  
        with colView4:       
            # CURRENTLY ASSIGNED TO
            lsASSIGNEDindex = st.session_state['lsMEMBERS'].index(st.session_state['dictTOPIC1']['formCurrAssignedTo'])
            st.session_state['dictTOPIC1']['formCurrAssignedTo'] = st.selectbox("🧑‍💻 **:red[Currently Assigned To]**", st.session_state['lsMEMBERS'], index=lsASSIGNEDindex)
            # PIC SUPPORT
            st.session_state['dictTOPIC1']['formAnalyticPICsupport'] = st.text_input("👥 Analytic PIC Support", value=st.session_state['dictTOPIC1']['formAnalyticPICsupport']) 
            # REQUESTOR
            st.session_state['dictTOPIC1']['formRequestor'] = st.text_input("👤 Requestor", value=st.session_state['dictTOPIC1']['formRequestor'])
        colView5, colView6 = st.columns(2)
        with colView5:
            # DUE DATE
            st.session_state['dictTOPIC1']['formDueDate'] = st.text_input("📅 Due Date", value=st.session_state['dictTOPIC1']['formDueDate'])
            # COUNTRY
            st.session_state['dictTOPIC1']['formCountry'] = st.text_input("🌍 Country", value=st.session_state['dictTOPIC1']['formCountry'])
        with colView6:
            # BENEFIT
            st.session_state['dictTOPIC1']['formBenefit'] = st.text_input("💡 Benefit", value=st.session_state['dictTOPIC1']['formBenefit'])
            # CSSC PIC
            st.session_state['dictTOPIC1']['formCSSCPIC'] = st.text_input("👨‍💼 CSSC PIC", value=st.session_state['dictTOPIC1']['formCSSCPIC'])
            # BL
            st.session_state['dictTOPIC1']['formBL'] = st.text_input("📊 BL", value=st.session_state['dictTOPIC1']['formBL'])
        # SHOW DESCRIPTION
        formDescription = st.session_state['dictTOPIC1']["formDescription"]
        countNewLine = formDescription.count('\n')
        st.session_state['dictTOPIC1']['formDescription'] = st.text_area("📋 **:red[Description]**", value=st.session_state['dictTOPIC1']["formDescription"], height=200+(10*countNewLine))
        
        # SAVE BUTTON
        if st.button("Save Edited Data"):
            # MARK TIME
            now = datetime.datetime.now()
            # LOAD ORIGINAL(0) AND UPDATED(1)
            dictTOPIC0 = st.session_state['dictTOPIC0']
            dictTOPIC1 = st.session_state['dictTOPIC1']
            # CLEAN [formPriority]
            if 'Low' in dictTOPIC1['formPriority']: 
                dictTOPIC1['formPriority'] = 'Low'
            elif 'Medium' in dictTOPIC1['formPriority']: 
                dictTOPIC1['formPriority'] = 'Medium'
            elif 'High' in dictTOPIC1['formPriority']: 
                dictTOPIC1['formPriority'] = 'High'
            else:
                dictTOPIC1['formPriority'] = None
            # CLEAN [formStatus]
            if 'Opened' in dictTOPIC1['formStatus']: 
                dictTOPIC1['formStatus'] = 'Opened'
            elif 'In Progress' in dictTOPIC1['formStatus']:
                dictTOPIC1['formStatus'] = 'In Progress'
            elif 'Completed' in dictTOPIC1['formStatus']:
                dictTOPIC1['formStatus'] = 'Completed'
            elif 'Cancelled' in dictTOPIC1['formStatus']:
                dictTOPIC1['formStatus'] = 'Cancelled'
            elif 'On Hold' in dictTOPIC1['formStatus']:
                dictTOPIC1['formStatus'] = 'On Hold'
            else:
                dictTOPIC1['formStatus'] = None
            # ONLY SAVE IF CHANGE
            if dictTOPIC0 != dictTOPIC1:
                # SAVE
                filepath = dictTOPIC1['sysPath']
                filename = 'TOPIC_' + now.strftime("%Y%m%d_%H%M%S")
                with open(f"{filepath}/{filename}.json", 'w') as outfile:
                    json.dump(dictTOPIC1, outfile)
                # RELOAD JSON
                updateState(dictTOPIC1['sysFolderName'])
            else:
                noChange()



        st.divider()

        ############
        # SHOW LOG #
        ############
        st.markdown(f"📋 All Logs")
        for log in st.session_state['dictLOG']:
            with st.container(border=True):
                st.markdown(f"**{log['logAddUsername']}** on **{log['logAddDate']}**")       
                htmlcontent = log['content']['html']
                htmlcontent = htmlcontent.replace('<p>', '').replace('</p>', '</br>')
                st.write(log['content']['html'], unsafe_allow_html=True)
        st.divider()

        ################
        # ADD NEW ITEM #
        ################
        # SHOW INPUT FIELD
        st.markdown(f"➕ Add Log")
        itemAddLog = st_quill("", html=True, readonly=False)
        # BUTTON SUBMIT ADD LOG
        if st.button("Add Log"):
            now = datetime.datetime.now()
            # ADD TO LOG
            dictAddLog = {'logAddUsername': st.session_state['username'],
                          'logAddDate': now.strftime("%Y-%m-%d"),
                          'logAddDatetime': now.strftime("%Y-%m-%d %H:%M:%S"),
                          'content':{'html': itemAddLog,
                                     'files': []}
                          }         
            st.session_state['dictLOG'].append(dictAddLog)
            # SAVE & RELOAD
            dictTOPIC = st.session_state['dictTOPIC1']
            filepath = dictTOPIC['sysPath']
            filename = 'LOG_' + now.strftime("%Y%m%d_%H%M%S")
            with open(f"{filepath}/{filename}.json", 'w') as outfile:
                json.dump(st.session_state['dictLOG'], outfile)
            # RELOAD JSON
            sysFolderName = dictTOPIC['sysFolderName']
            updateState(sysFolderName)
            st.rerun()
   



    else:
        st.header("Select Item from All item page")
        if st.button('📋 All Items'):
            st.switch_page('./pages/P1 📋 All Items.py')

    # DEBUG
    with st.expander('DEBUG'): 
        st.text(st.session_state['viewItemFolder'])
        st.json(st.session_state['dictTOPIC0'])
        st.json(st.session_state['dictTOPIC1'])
        st.json(st.session_state['dictLOG'])

else:
    st.header("Go back to the Login page")
    if st.button('Login'):
        st.switch_page('Login.py')

