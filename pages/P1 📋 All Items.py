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

def refreshdfALL():
    #########
    # dfALL #
    #########
    dfALL = pd.DataFrame()
    dfALL['ITEM_PATH'] = [str(p).replace('\\','/')+'/' for p in pathlib.Path(st.session_state['ITEM_DIRECTORY']).iterdir() if p.is_dir()]
    dfALL['ITEM_ID_FULL'] = dfALL['ITEM_PATH'].str.split('/').str[-2]
    # GET ALL JSON IN PATH
    def getAllJson(path):
        lsallJson = [str(p).replace('\\','/') for p in pathlib.Path(f"{path}").rglob('*') if 'json' in str(p)]
        lsallJson = [x.split('/')[-1] for x in lsallJson]
        return lsallJson
    dfALL['ALL_JSON'] = dfALL['ITEM_PATH'].apply(getAllJson)
    # GET MAX JSON FILENAME USING JSON NAME IF 'TOPIC/LOG' IN JSON FILENAME
    def getMaxPath(ls, contains):
        lsname = [x for x in ls if contains in x]
        maxname = max(lsname)
        return maxname
    dfALL['MAX_TOPIC'] = dfALL['ALL_JSON'].apply(getMaxPath, contains='TOPIC')
    dfALL['MAX_TOPIC_PATH'] = dfALL['ITEM_PATH'] + dfALL['MAX_TOPIC']
    dfALL['MAX_LOG'] = dfALL['ALL_JSON'].apply(getMaxPath, contains='LOG')
    dfALL['MAX_LOG_PATH'] = dfALL['ITEM_PATH'] + dfALL['MAX_LOG']
    # GET DATE FROM FILENAME
    dfALL['TOPIC_DTTM'] = dfALL['MAX_TOPIC'].str.replace('TOPIC_','').str.replace('.json','')
    dfALL['LOG_DTTM'] = dfALL['MAX_LOG'].str.replace('LOG_','').str.replace('.json','')
    dfALL['LAST_MODIFIED_STR'] = dfALL[['TOPIC_DTTM','LOG_DTTM']].max(axis=1)
    dfALL['LAST_MODIFIED_DTTM'] = pd.to_datetime(dfALL['LAST_MODIFIED_STR'], format='%Y%m%d_%H%M%S')
    dfALL['TOPIC_CONTENT'] = dfALL['MAX_TOPIC_PATH'].apply(lambda x: json.load(open(x)))
    dfALL['ITEM_ID_SHORT'] = dfALL['ITEM_ID_FULL'].str.replace('---','-')
    dfALL['ITEM_ID_SHORT2'] = dfALL['ITEM_ID_FULL'].str.split('---').str[0] + '-' + dfALL['ITEM_ID_FULL'].str.split('---').str[1]
    dfALL['TOPIC_NAME'] = dfALL['TOPIC_CONTENT'].apply(lambda x: x['formTopic'])
    dfALL['CREATED_BY'] = dfALL['TOPIC_CONTENT'].apply(lambda x: x['sysUserID'])
    dfALL['CREATED_DTTM'] = pd.to_datetime(dfALL['TOPIC_CONTENT'].apply(lambda x: x['sysCreateDttm']), format='%Y-%m-%d %H:%M:%S')
    dfALL['PIC_MAIN'] = dfALL['TOPIC_CONTENT'].apply(lambda x: x['formAnalyticPICmain'])
    dfALL['CURR_ASSIGNED'] = dfALL['TOPIC_CONTENT'].apply(lambda x: x['formCurrAssignedTo'])
    dfALL['ITEM_TYPE'] = dfALL['TOPIC_CONTENT'].apply(lambda x: x['formRequestType'])
    def modItemType(x):
        if x == 'NEW_REQUEST': return '✨ New Request'
        elif x == 'ISSUE': return '🛠️ Issue'
        else: return None 
    dfALL['ITEM_TYPE2'] = dfALL['ITEM_TYPE'].apply(modItemType)
    dfALL['STATUS'] = dfALL['TOPIC_CONTENT'].apply(lambda x: x['formStatus'])
    def modStatus(x):
        if x == 'Opened': return '📋 Opened'
        elif x == 'In Progress': return '🔄 In Progress'
        elif x == 'Completed': return '✅ Completed'
        elif x == 'Cancelled': return '❌ Cancelled'
        elif x == 'On Hold': return '⏳ On Hold'
        else: return None
    dfALL['STATUS2'] = dfALL['STATUS'].apply(modStatus)
    dfALL['PRIORITY'] = dfALL['TOPIC_CONTENT'].apply(lambda x: x['formPriority'])
    def modePriority(x):
        if x == 'Low': return '🟢 Low'
        elif x == 'Medium': return '🟡 Medium'
        elif x == 'High': return '🔴 High'
        else: return None
    dfALL['PRIORITY2'] = dfALL['PRIORITY'].apply(modePriority)
    st.session_state['dfALL'] = dfALL.copy()
    ##########
    # dfTAB1 #
    ##########
    dftab1 = st.session_state['dfALL'].copy()
    dftab1 = dftab1[['ITEM_ID_FULL','ITEM_ID_SHORT2','TOPIC_NAME','CREATED_BY','PIC_MAIN','CURR_ASSIGNED','ITEM_TYPE2','PRIORITY2','STATUS2','LAST_MODIFIED_DTTM']].reset_index(drop=True)
    dftab1.columns = ['ITEM_ID_FULL','ID','NAME','CREATOR','PIC MAIN','ASSIGNED TO','TYPE','PRIORITY','STATUS','LAST MODIFIED']
    st.session_state['dfTAB1'] = dftab1.copy() 
    

if st.session_state['username'] != None:
    refreshdfALL()
    # WELCOME
    st.header(f"Welcome :blue[{st.session_state['username']}]")

    # 3 TABS
    tab1, tab2, tab3, tab4 = st.tabs(['📂 All Items','🧑‍💻 PIC is me','🎯Assigned to me','✍️ Created by me'])
    with tab1:
        st.header("📂 All Items")
        # TOP MENU
        tab1_col1, tab1_col2, tab1_col3 = st.columns(3)
        with tab1_col1:
            # REFRESH BUTTON
            if st.button('Refresh Data'):
                refreshdfALL()
                st.rerun()
        with tab1_col2:            
            # REFRESH BUTTON
            if st.button('View Item'):
                if st.session_state['eventT1'].selection['rows'] == []:
                    pass
                else:
                    selIndex = st.session_state['eventT1'].selection['rows'][0]
                    st.session_state['viewItemFolder'] = st.session_state['dfTAB1']['ITEM_ID_FULL'].iat[selIndex]
                    st.switch_page('pages/P2 👀 View Item.py')
        # SHOW DF
        st.session_state['eventT1'] = st.dataframe(st.session_state['dfTAB1'], 
                                                   column_order = ['ID','NAME','CREATOR','PIC MAIN','ASSIGNED TO','TYPE','PRIORITY','STATUS','LAST MODIFIED'],                                                           
                                                   on_select="rerun", 
                                                   #on_select=on_select, 
                                                   hide_index=True,
                                                   selection_mode='single-row')      

    with tab2:
        st.header("🧑‍💻 PIC is me")
    with tab3:
        st.header("🎯Assigned to me")
    with tab4:
        st.header("✍️ Created by me")


    with st.expander('DEBUG'): 
        #st.json(lsallJson)
        st.dataframe(st.session_state['dfALL'])
        st.text(st.session_state['viewItemFolder'])
        # st.dataframe(dfAJ)
        # st.json(dictJson)
        #st.dataframe(st.session_state['dfALL'])

else:
    st.header("Go back to the Login page")
    if st.button('Login'):
        st.switch_page('Login.py')



