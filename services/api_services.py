import uuid

import requests
import streamlit as st
import time
from pprint import pp

base_url = 'https://hsxyp0kgk2.execute-api.ap-northeast-2.amazonaws.com/dev'


"""
로그인을 시도하는 함수로 
response의 결과가 200일 경우에는 로그인 세션 상태를 변경한다.
실패할 경우에는 변경하지 않는다.
:param email: 이메일
:param pwd: 비밀번호
:return: Bool
"""
def login_with_linkus(email, pwd) -> bool:
    header = {}
    parameter = {
        "email": email,
        "password": pwd,
    }
    url = f'{base_url}/users/signin'
    response = requests.post(url, headers=header, json=parameter)

    if response.status_code == 200:
        st.session_state['is_login'] = True
        st.session_state['email'] = email
        return True
    else:
        st.session_state['is_login'] = False
        st.session_state['email'] = None
        return False


def get_thread_id_list():
    header = {
        'Authorization': st.secrets["52genie_token"],
    }
    parameter = {
    }
    url = 'https://hsxyp0kgk2.execute-api.ap-northeast-2.amazonaws.com/dev/threads'
    data = requests.get(url, headers=header, params=parameter)
    json_data = data.json()
    for thread in json_data['data']['threads']:
        st.session_state["thread_id_list"].append(thread['thread_id'])


def ask(prompt, thread_id):
    header = {
        'Authorization': st.secrets["52genie_token"],
    }
    parameter = {
        "message_from": "HUMAN",
        "messages": [
            {"type": "text", "text": prompt}
        ],
        "is_test": True,
    }
    url = f'{base_url}/messages/query/{thread_id}'
    data = requests.post(url, headers=header, json=parameter)
    return data.json()


def get_answer(thread_id, message_id):
    # full_response = ""
    # header = {
    #     'Authorization': st.secrets["52genie_token"],
    #     'accept': 'application/json'
    # }
    # parameter = {
    #     "thread_id": thread_id,
    #     "message_id": message_id,
    # }
    # url = f'https://hsxyp0kgk2.execute-api.ap-northeast-2.amazonaws.com/dev/answers/{thread_id}/{message_id}'
    # stay_in_loop = True
    # with st.spinner("잠시만 기다려주세요..."):
    #     while stay_in_loop:
    #         data = requests.get(url, headers=header, params=parameter)
    #         result = data.json()
    #         answer = result['data']['messages'][0]['answer']
    #
    #         if answer is None:
    #             time.sleep(3)
    #         else:
    #             full_response += result['data']['messages'][0]['answer']
    #             prompt_recommendation_list = result['data']['messages'][0]['prompt_recommendation_list']
    #             stay_in_loop = False
    #
        # st.markdown(full_response)
    # st.markdown('응답')
    st.session_state[thread_id].append(
        {"role": "assistant", "content": '응답'}
    )



