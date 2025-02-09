import streamlit as st
if "login_state" not in st.session_state:
    st.session_state["login_state"] = None
pg1 = st.Page(
    page="login.py",
    title="登录"
)

pg2 = st.Page(
    page="calculate.py",
    title="计算"
)

if st.session_state["login_state"]:
    st.navigation([pg2])
else:
    st.navigation([pg1])

