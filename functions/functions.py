from datetime import datetime

import streamlit as st


def add_item():
    print('add_item_called')
    tst = int(datetime.timestamp(datetime.now()))
    thread_id = str(tst)
    st.session_state["thread_id_list"].append(thread_id)
    print(st.session_state["thread_id_list"])
    # thread_id_list = st.session_state["thread_id_list"]

    # thread_id_list.append(thread_id)
    # st.session_state[thread_id] = []
    # if thread_id + 'first_recommendation' not in st.session_state:
    #     st.session_state[thread_id + 'is_first_recommendation'] = True


def set_app_id_via_selected_app_name():
    for app in st.session_state['app_list']:
        if app['app_name'] == st.session_state["selected_app_name"]:
            return app['app_id']
