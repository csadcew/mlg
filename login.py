import streamlit as st

p = ["96f0a81e13b6d23ecaa4a1db8322a28b", "123"]
pwd = st.text_input("请输入软件密码：")
if st.button("登录"):
    if pwd in p:
        st.session_state.login_state = True
        st.info("登录成功")
        st.rerun()
    else:
        st.session_state.login_state = False
        st.error("密码错误!!!")
