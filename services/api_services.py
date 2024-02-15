import uuid

import requests
import streamlit as st
import time
from pprint import pp

base_url = 'https://hsxyp0kgk2.execute-api.ap-northeast-2.amazonaws.com/dev'
genie_token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4ODk2MDE5OCwianRpIjoiZTBhNzkyYWEtN2EwNC00ZDJiLTkyNjMtMDk2MmEzNTMzNGRhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFwcHNtaXRoIiwibmJmIjoxNjg4OTYwMTk4LCJzY29wZSI6IkFETUlOIn0.MncQ5BGfCAo5W0h-pYiD7bNtgphk0bQWNi_KRLDPoo0"

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
    return json_data


def ask(prompt, thread_id, app_id):
    header = {
        'Authorization': st.secrets["52genie_token"],
    }
    parameter = {
                    "app_id": app_id,
                    "thread_id": thread_id,
                    "query": prompt
                }

    url = f'{base_url}/apps/query/'
    data = requests.post(url, headers=header, json=parameter)
    return data.json()


def get_answer(thread_id, message_id,app_name):
    full_response = f"({app_name}) "
    header = {
        'Authorization': st.secrets["52genie_token"],
        'accept': 'application/json'
    }
    parameter = {
        "thread_id": thread_id,
        "message_id": message_id,
    }
    url = f'{base_url}/messages/history/{thread_id}'
    stay_in_loop = True
    with st.spinner("잠시만 기다려주세요..."):
        while stay_in_loop:
            data = requests.get(url, headers=header, params=parameter)
            result = data.json()
            answer = result['data']['message_list'][-1]['messages'][0]['text']

            if answer is None:
                time.sleep(3)
            else:
                full_response += result['data']['message_list'][-1]['messages'][0]['text']
                # prompt_recommendation_list = result['data']['messages'][0]['prompt_recommendation_list']
                stay_in_loop = False

        st.markdown(full_response)
    # st.markdown('응답')
    st.session_state[thread_id].append(
        {"role": "assistant", "content": full_response}
    )


def load_chat_history(thread_id):
    header = {
        'Authorization': genie_token,
    }

    parameter = {"thread_id": thread_id}
    url = f'{base_url}/messages/history/{thread_id}'
    data = requests.get(url, headers=header, params=parameter)
    pp(data.json())
    # print(data)
    # answers = data.json()['data']['messages']


def get_app_list():
    url = f'{base_url}/apps'
    header = {
        'Authorization': genie_token,
    }

    response = requests.get(url, headers=header)
    app_list = list()
    app_map_dict = {}
    for app in response.json()['data']:
        app_list.append({'app_id': app['app_id'], 'app_name': app['name']})
        app_map_dict[app['name']] = app['app_id']

    return app_list, app_map_dict


if __name__ == "__main__":
    load_chat_history('5dd2a96c-f846-49a0-854d-8d4e0cbe8f93')



