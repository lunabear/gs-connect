import streamlit as st
from streamlit_option_menu import option_menu

from functions.functions import add_thread, set_app_id_via_selected_app_name, \
    set_thread_id_list_to_session_state, set_chat_history_via_thread_id
from services.api_services import login_with_linkus, ask, get_app_list


def run():
    st.set_page_config(page_title='52genie', menu_items=None,
                       page_icon='assets/logo_favicon.svg')
    print('main_page.py run()')

    if 'is_login' not in st.session_state:
        st.session_state['is_login'] = False

    if "selected_app_name" not in st.session_state:
        st.session_state["selected_app_name"] = None
        st.session_state["selected_app_id"] = None

    if 'token' not in st.session_state:
        st.session_state['token'] = ''

    placeholder = st.empty()
    if not st.session_state['is_login']:
        with placeholder.container():
            left_co, cent_co, last_co = st.columns(3)
            with cent_co:
                st.image('assets/algo_52g_logo.svg', width=200)
                st.title("Login")
                email = st.text_input('Email', value='bob@gs.co.kr')
                pw = st.text_input('Password', value='Lunabear910!', type='password')

                with st.form("my_form"):
                    submitted = st.form_submit_button("Submit")
                    if submitted:
                        if not login_with_linkus(email, pw):
                            st.error('등록되지 않은 사용자입니다')

    if st.session_state['is_login']:
        if "thread_id_list" not in st.session_state:
            st.session_state["thread_id_list"] = []
            # add_thread()
            set_thread_id_list_to_session_state()
            for thread_id in st.session_state["thread_id_list"]:
                if thread_id not in st.session_state:
                    st.session_state[thread_id] = []
                set_chat_history_via_thread_id(thread_id)

        if 'app_list' not in st.session_state:
            st.session_state['app_list'] = []
            _app_list, app_map_dict = get_app_list()
            st.session_state['app_map_dict'] = app_map_dict
            for app in _app_list:
                st.session_state['app_list'].append(app)

        with placeholder:
            st.empty()

        with st.sidebar:
            st.image('assets/algo_52g_logo.svg', width=200)
            st.session_state["selected_app_name"] = st.selectbox('app 선택', [app['app_name']
                                                                            for app in st.session_state['app_list']])
            st.session_state["selected_app_id"] = set_app_id_via_selected_app_name()
            st.button("\+ 새로운 채팅", on_click=add_thread, key='add_thread_button')
            default_index = len(st.session_state["thread_id_list"]) - 1

            if len(st.session_state["thread_id_list"]) > 0:
                current_thread = option_menu("", st.session_state["thread_id_list"],
                                          key="unique_key_for_option_menu",
                                          icons=['house', 'camera fill', 'kanban', 'book', 'person lines fill'],
                                          menu_icon='kanban', default_index=default_index,
                                          manual_select=default_index,
                                  )
                st.session_state['current_thread'] = current_thread

        if st.session_state['current_thread'] not in st.session_state:
            st.session_state[st.session_state['current_thread']] = []

        for message in st.session_state[st.session_state['current_thread']]:
            with st.chat_message(message["role"]):
                #f'({st.session_state["selected_app_name"]}) ' + content
                if message["role"] == "assistant":
                    st.markdown(f'({message["app_name"]}) {message["content"]}')
                else:
                    st.markdown(message["content"])


        if prompt := st.chat_input(f"{st.session_state['selected_app_name']}에게 물어보세요."):
            st.session_state[st.session_state['current_thread']].append(
                {"role": "user", "content": prompt, "app_name": st.session_state["selected_app_name"]})
            with st.chat_message("user"):
                st.markdown(prompt)
                st.session_state["app_id"] = st.session_state['app_map_dict'][st.session_state["selected_app_name"]]


            with st.chat_message("assistant"):
                with st.spinner("많이 답답하시지요? 저희가 답변을 만들고 있어요."):
                    response = ask(prompt, st.session_state['current_thread'], st.session_state["app_id"])
                    print(response)
                    content = response['data']['result']
                    # st.markdown(content)
                    def fake_streaming(content):
                        content = f'({st.session_state["selected_app_name"]}) ' + content
                        import time
                        for word in content.split():
                            yield word + " "
                            time.sleep(0.1)

                st.write_stream(fake_streaming(content))
                st.session_state[st.session_state['current_thread']].append(
                    {"role": "assistant", "content": content, "app_name": st.session_state["selected_app_name"]}
                )


if __name__ == "__main__":
    run()
