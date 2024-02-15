from datetime import datetime

import streamlit as st

from services.api_services import get_thread_id_list


def add_item():
    #thread id를 만드는 api를 만들자
    #api에서 받아온 thread_id를 세션 스테이트에 추가하자
    #추가하면 채팅창 리스트에 어떻게 뿌려지는지 확인하자
    tst = int(datetime.timestamp(datetime.now()))
    thread_id = str(tst)
    st.session_state["thread_id_list"].append(thread_id)
    print(st.session_state["thread_id_list"])
    # thread_id_list = st.session_state["thread_id_list"]

    # thread_id_list.append(thread_id)
    # st.session_state[thread_id] = []
    # if thread_id + 'first_recommendation' not in st.session_state:
    #     st.session_state[thread_id + 'is_first_recommendation'] = True


def set_thread_id_list_to_session_state():
    thread_id_list = get_thread_id_list()
    for thread in thread_id_list['data']['threads']:
        st.session_state["thread_id_list"].append(thread['thread_id'])



def set_app_id_via_selected_app_name():
    for app in st.session_state['app_list']:
        if app['app_name'] == st.session_state["selected_app_name"]:
            return app['app_id']
