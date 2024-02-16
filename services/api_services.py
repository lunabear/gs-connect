import requests
import streamlit as st
import time
from pprint import pp

base_url = 'https://hsxyp0kgk2.execute-api.ap-northeast-2.amazonaws.com/dev'


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
        st.session_state.token = f"Bearer {response.json()['data']['jwt_token']}"
        return True
    else:
        st.session_state['is_login'] = False
        st.session_state['email'] = None
        return False


def get_thread_id_list():
    header = {
        'Authorization': st.session_state.token,
    }
    parameter = {
    }
    url = 'https://hsxyp0kgk2.execute-api.ap-northeast-2.amazonaws.com/dev/threads'
    data = requests.get(url, headers=header, params=parameter)
    json_data = data.json()
    return json_data


def ask(prompt, thread_id, app_id):
    header = {
        'Authorization': st.session_state.token,
    }
    parameter = {
                    "app_id": app_id,
                    "thread_id": thread_id,
                    "query": prompt
                }

    url = f'{base_url}/apps/query/'
    data = requests.post(url, headers=header, json=parameter)
    return data.json()


def get_app_list():
    url = f'{base_url}/apps'
    header = {
        'Authorization': st.session_state.token,
    }

    response = requests.get(url, headers=header)
    app_list = list()
    app_map_dict = {}
    for app in response.json()['data']:
        app_list.append({'app_id': app['app_id'], 'app_name': app['name']})
        app_map_dict[app['name']] = app['app_id']

    return app_list, app_map_dict


def get_thread_id():
    header = {
        'Authorization': st.session_state.token,
    }
    parameter = {
                    "name": "new_chat",
                }

    url = f'{base_url}/threads'
    data = requests.post(url, headers=header, json=parameter)
    return data


def get_chat_history_via_thread_id(thread_id: str):
    header = {
        'Authorization': st.session_state.token,
    }
    parameter = {
    }
    url = f'{base_url}/messages/history/{thread_id}'
    data = requests.get(url, headers=header, params=parameter)
    json_data = data.json()
    return json_data

