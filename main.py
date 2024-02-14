from pprint import pp

import streamlit as st
from streamlit_option_menu import option_menu

from functions.functions import add_item
from services.api_services import login_with_linkus, ask, get_thread_id_list, get_answer


def run():
    st.set_page_config(page_title='52genie', menu_items=None,
                       page_icon='assets/logo_favicon.svg')
    print('main_page.py run()')
    #session state에서 사용하는 값들을 초기화 하기 위한 코드.
    #streamlit은 action이 발생하면 코드를 처음부터 끝까지 다시 실행하므로 아래같은 초기화 코드가 필요하다.
    #session state에 is login이 없으면 False로 초기화
    if 'is_login' not in st.session_state:
        st.session_state['is_login'] = False

    if "selected_app" not in st.session_state:
        st.session_state["selected_app"] = None

    #placeholder는 로그인 여부에 따라 다른 화면을 보여주기 위한 컨테이너
    #placeholder 없이 화면을 그릴경우 로그인 여부에 따라 화면이 바뀌지 않는다. 로그인이 성공해도 아이디, 비밀번호, 로그인 버튼이 그대로 남아있게 된다.

    placeholder = st.empty()
    if not st.session_state['is_login']:
        with placeholder.container():
            left_co, cent_co, last_co = st.columns(3)
            with cent_co:
                st.image('assets/52g_logo.png', width=200)
                st.title("Login")
                email = st.text_input('Email', value='bob@gs.co.kr')
                pw = st.text_input('Password', value='Lunabear910!', type='password')

                with st.form("my_form"):
                    submitted = st.form_submit_button("Submit")
                    if submitted:
                        #login with linkus의 응답이 false면 로그인 실패 alert를 띄운다.
                        if not login_with_linkus(email, pw):
                            st.error('로그인 실패')

    if st.session_state['is_login']:
        #login에 성공하면 내 아이디에 해당하는 thread_list를 가져온다.
        #화면이 새로 불릴때마다 thread들을 새로 불러오는 이슈가 있어서 이를 방지하기 위해 thread_id_list 초기화는 로그인 직후에 실행한다.
        #thread_id_list를 가져오는 시점은 로그인 성공시에만 실행되도록 한다.
        if "thread_id_list" not in st.session_state:
            st.session_state["thread_id_list"] = []
            get_thread_id_list()
            for thread_id in st.session_state["thread_id_list"]:
                pass


        #login창 지우기용도
        with placeholder:
            st.empty()

        with st.sidebar:
            st.image('assets/new_logo.svg', width=200)
            st.session_state["selected_app"] = st.selectbox('app 선택', ['app1', 'app2', 'app3'])
            button = st.button(""
                               "\+ 새로운 채팅", on_click=add_item, key='add_item_button')
            default_index = len(st.session_state["thread_id_list"]) - 1

            if len(st.session_state["thread_id_list"]) > 0:
                current_thread = option_menu("", st.session_state["thread_id_list"],
                                          key="unique_key_for_option_menu",
                                          icons=['house', 'camera fill', 'kanban', 'book', 'person lines fill'],
                                          menu_icon='kanban', default_index=default_index,
                                          manual_select=default_index,
                                          )
                st.session_state['current_thread'] = current_thread
                print('current_thread : ', st.session_state['current_thread'])

        #채팅창 출력라인이다.

        st.session_state
        if st.session_state['current_thread'] not in st.session_state:
            st.session_state[st.session_state['current_thread']] = []

        for message in st.session_state[st.session_state['current_thread']]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])


        if prompt := st.chat_input("AI 어시스턴트 오이지니에게 물어보세요."):
            st.session_state[st.session_state['current_thread']].append(
                {"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
                response = ask(prompt, st.session_state['current_thread'])
                message_id = response['data']['message_id']
            with st.chat_message("assistant"):
                get_answer(st.session_state['current_thread'], message_id)
                # st.markdown('답변입니다')


if __name__ == "__main__":
    run()
