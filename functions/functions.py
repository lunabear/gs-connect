from datetime import datetime
from pprint import pp

import streamlit as st

from services.api_services import get_thread_id_list, get_thread_id, get_chat_history_via_thread_id


def add_thread():
    thread_info = get_thread_id().json()
    thread_id = thread_info['data']['thread_id']
    st.session_state["thread_id_list"].append(thread_id)



def set_thread_id_list_to_session_state():
    thread_id_list = get_thread_id_list()
    for thread in thread_id_list['data']['threads']:
        st.session_state["thread_id_list"].append(thread['thread_id'])



def set_app_id_via_selected_app_name():
    for app in st.session_state['app_list']:
        if app['app_name'] == st.session_state["selected_app_name"]:
            return app['app_id']


def set_chat_history_via_thread_id(thread_id: str) -> None:
    chat_history = get_chat_history_via_thread_id(thread_id)

    for chat in chat_history['data']['message_list']:
        if chat['message_from'] == "BOT":
            chat['message_from'] = "assistant"
        st.session_state[thread_id].append(
            {"role": chat['message_from'], "content": chat['messages'][0]['text']}
        )




