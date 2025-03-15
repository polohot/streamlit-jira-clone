import streamlit as st
import pandas as pd
import json
import os
import glob
import pathlib
from datetime import datetime

########
# INIT #
########
st.set_page_config(page_title="Main",layout='wide')

tab1, tab2, tab3 = st.tabs(['View Item','All Items','Add Item'])

if 'selected_items' not in st.session_state:
    st.session_state['selected_item'] = None
###################
# tab1: View Item #
###################

with tab1:
    st.header("Item Details")

    if st.session_state['selected_item'] != None:
        selected_item = st.query_params['selected_item']


        # GET DATA
        lsMotherJson = list(pathlib.Path(f"./itemHistory/{selected_item}").rglob('*'))
        lsMotherJson = [str(x) for x in lsMotherJson]
        motherJsonPath = max(lsMotherJson)
        # OPEN MOTHER JSON
        with open(motherJsonPath, 'r') as f:
            motherJson = json.load(f)
        # SHOW MOTHER JSON
        st.markdown(f"Item Number: **{selected_item}**")
        st.info(f"**{motherJson['formTopic']}**")   
        colView1, colView2 = st.columns(2)
        with colView1:
            st.markdown(f"Analytic PIC Main: **{motherJson['formDataAnalyticPICmain']}**")
            st.markdown(f"Priority: **{motherJson['formPriority']}**")
            st.markdown(f"Request Type: **{motherJson['formRequestType']}**")
            st.markdown(f"Request Date: **{motherJson['formRequestDate']}**")
            st.markdown(f"Due Date: **{motherJson['formDueDate']}**")
        with colView2:
            st.markdown(f"Analytic PIC Support: **{motherJson['formDataAnalyticPICsupport']}**")
            st.markdown(f"Requestor: **{motherJson['formRequestor']}**")
            st.markdown(f"CSSC PIC: **{motherJson['formCSSCPIC']}**")
            st.markdown(f"Country: **{motherJson['formCountry']}**")
            st.markdown(f"BL: **{motherJson['formBL']}**")

        # Editable text box, prefilled with motherJson['formDescription']        
        st.text_area("Description", value=motherJson['formDescription'], height=200)

        



        

        # DEBUG
        with st.expander('DEBUG'):
            st.json(lsMotherJson)
            st.write(motherJsonPath)
            st.json(motherJson)


    else:
        st.info("Select an item from the 'All Items' tab to view details.")


###################
# tab2: All Items #
###################


with tab2:
    st.header("All Items")

    if st.button('Reload/Refresh'):
        # GET JSON LOG
        allJson = list(pathlib.Path('./itemHistory/').rglob('*'))
        dfJson = pd.DataFrame()
        dfJson['FILE_PATH'] = allJson
        dfJson['FILE_PATH'] = dfJson['FILE_PATH'].astype(str)
        dfJson = dfJson[dfJson['FILE_PATH'].str.endswith('json')]
        dfJson['ITEM'] = dfJson['FILE_PATH'].str.split("\\").str[1]
        dfJson['FILE_NAME'] = dfJson['FILE_PATH'].str.split("\\").str[-1]
        # SELECT LATEST JSON OF THAT ITEM
        dfmax = dfJson.groupby('ITEM').agg({'FILE_NAME':'max'}).reset_index()
        dfmax['LATEST'] = 1
        dfJson = dfJson.merge(dfmax, on=['ITEM','FILE_NAME'], how='left')
        dfJson = dfJson[dfJson['LATEST']==1].reset_index(drop=True)
        # LOAD JSON DATA
        dfJson['JSON'] = None
        for i in range(len(dfJson)):
            jsonpath = dfJson['FILE_PATH'].iat[i]
            with open(jsonpath, 'r') as f:
                thisdict = json.load(f)
                dfJson['JSON'].iat[i] = thisdict            
        # PARSE JSON
        dfJson['TOPIC'] = [x['formTopic'] for x in dfJson['JSON']]
        dfJson['CREATE_DATE'] = [x['sysCreateYYYYMMDD'] for x in dfJson['JSON']]
        dfJson['PIC_MAIN'] = [x['formDataAnalyticPICmain'] for x in dfJson['JSON']]

        dfJson['LINK'] = dfJson.apply(lambda row: f"[🔗 LINK](?selected_item={row['ITEM']})", axis=1)
        st.write(dfJson[['ITEM','CREATE_DATE','PIC_MAIN','TOPIC','LINK']].to_markdown(index=False), unsafe_allow_html=True)

        # DEBUG
        with st.expander('DEBUG'):
            st.dataframe(dfJson)

###################
# tab3: Add Items #
###################
with tab3:
    st.header("Add Item")

    with st.form('formAddItem', clear_on_submit=True, enter_to_submit=False):
        # Topic (text input, cannot be blank)
        formTopic = st.text_input("Topic (Text) *", key="formTopic")   
        # SPLIT COLUMNS 1
        colform1, colform2 = st.columns(2)
        with colform1:
            # Data & Analytic PIC Main
            formDataAnalyticPICmain = st.selectbox("Analytic PIC Main (Dropdown) *", ['---','Kwang','Long','Minmin','Gates','Pomm'], index=0, key="formDataAnalyticPICmain")  
            # Priority (dropdown with Low/Medium/High, default Low)
            formPriority = st.selectbox("Priority (Dropdown) *", ['---',"Low", "Medium", "High"], index=0, key="formPriority")  
            # RequestType
            formRequestType = st.selectbox("Request Type (Dropdown) *", ['---',"New Request", "Issue"], index=0, key="formRequestType")  
        with colform2:
            # Data & Analytic PIC Support
            formDataAnalyticPICsupport = st.text_input("Analytic PIC Support (Text)", key="formDataAnalyticPICsupport")   
            # Requestor
            formRequestor = st.text_input("Requestor (Text)", key="formRequestor") 
        # Description (text input, cannot be blank)
        formDescription = st.text_area("Description (Text)", key="formDescription")   
        # SPLIT COLUMNS 2
        colform3, colform4 = st.columns(2)
        with colform3:
            # Request date (default to today, but adjustable)
            formRequestDate = st.date_input("Request Date (Date)", value=datetime.today(), key="formRequestDate", format="YYYY-MM-DD")     
            # Due Date
            formDueDate = st.text_input("Due Date (Text)", key="formDueDate")  
        with colform4:
            # CSSC PIC
            formCSSCPIC = st.text_input("CSSC PIC (Text)", key="formCSSCPIC")  
            # Country
            formCountry = st.text_input("Country (Text)", key="formCountry")  
            # BL
            formBL = st.text_input("BL (Text)", key="formBL")  

        # Submit button
        submitted = st.form_submit_button("Submit")        
        # Validate inputs and add to list
        if submitted:
            error = 0
            if not formTopic or not formDescription:
                error = 1
                st.error("Topic and Description cannot be blank!")
            if formDataAnalyticPICmain == '---':
                error = 1
                st.error("Select Analytic PIC Main!")
            if formPriority == '---':
                error = 1
                st.error("Select Priority!")
            if formRequestType == '---':
                error = 1
                st.error("Select Request Type!")

            if error == 0:
                # CREATE NEW DICT FOR THE REQUEST
                dttmnow = datetime.now()
                jsonItem = {
                    "sysCreateDttm": dttmnow.strftime("%Y%m%d-%H%M%S"),
                    "sysCreateYYYY": dttmnow.strftime('%Y'),
                    "sysCreateYYYYMM": dttmnow.strftime('%Y-%m'),
                    "sysCreateYYYYMMDD": dttmnow.strftime('%Y-%m-%d'),  
                    "sysPath": f"./itemHistory/{dttmnow.strftime("%Y%m%d-%H%M%S")}",                    
                    "sysTopicName": dttmnow.strftime("%Y%m%d-%H%M%S"),  
                    "sysFileName": dttmnow.strftime("%Y%m%d-%H%M%S"),
                    "formTopic": formTopic,
                    "formPriority": formPriority,
                    "formRequestType": formRequestType,
                    "formRequestor": formRequestor,
                    "formDescription": formDescription,
                    "formRequestDate": formRequestDate.strftime('%Y-%m-%d'),
                    "formDueDate": formDueDate,
                    "formCountry": formCountry,
                    "formBL": formBL,
                    "formCSSCPIC": formCSSCPIC,
                    "formDataAnalyticPICmain": formDataAnalyticPICmain,
                    "formDataAnalyticPICsupport": formDataAnalyticPICsupport                   
                    }
                # SAVE JSON
                filepath = jsonItem['sysPath']
                filename = jsonItem['sysFileName']
                if not os.path.exists(filepath):
                    os.makedirs(filepath) 
                with open(f"{filepath}/{filename}.json", 'w') as outfile:
                    json.dump(jsonItem, outfile)

                # MSG
                st.success(f"Item {filename} Created")

                # INSIDE st.success, go to another link
                st.success(f"[🔗 LINK](?selected_item={filename})")

                # DEBUG
                with st.expander('DEBUG'):
                    st.write(jsonItem)
                           




