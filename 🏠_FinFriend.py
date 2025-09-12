import streamlit as st

import ui.components.sidebar

st.set_page_config(
	page_title="FinFriend",
	page_icon="💸",
	layout="wide"
)

ui.components.sidebar.show()

st.toast("Welcome to FinFriend!", icon="💸")

st.markdown("Welcome to FinFriend, your AI-powered personal finance assistant!")
st.write("FinFriend is designed to help you explore and understand your personal finances.")
