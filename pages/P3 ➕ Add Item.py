from utils123456 import *
initconfig()
loadconfig()

###############
# PAGE CONFIG #
###############
st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

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
            
            #############
            # V1 - JSON #
            #############

            # GET FILE NAME
            stryyyy = str(now.year)
            lsHistory = [folder.name for folder in pathlib.Path(st.session_state['ITEM_DIRECTORY']).iterdir() if folder.is_dir()]
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
            jsonMetadata['sysPath'] = f"{st.session_state['ITEM_DIRECTORY']}{foldername}/"
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

            ############
            # V2 - SQL #
            ############



    with st.expander('DEBUG'): 
        st.text(st.session_state['viewItemFolder'])
        if 'lsID' in globals(): st.json(lsID)
        if 'maxID' in globals(): st.text(maxID)
        if 'thisID' in globals(): st.text(thisID)
        if 'foldername' in globals(): st.text(foldername)
        if 'jsonMetadata' in globals(): st.json(jsonMetadata)
        st.text(st.session_state['ITEM_DIRECTORY'])
        st.text(st.session_state['PASSWORD_DICT'])
        st.text(st.session_state['ADMIN_LIST'])

else:
    st.header("Go back to the Login page")
    if st.button('Login'):
        st.switch_page('Login.py')