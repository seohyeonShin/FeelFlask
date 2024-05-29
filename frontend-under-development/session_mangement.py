import streamlit as st
import json

def initialize_session_state():
    if 'page' not in st.session_state:
        st.session_state.page = 0
    if 'drink_type' not in st.session_state:
        st.session_state.drink_type = None
    if 'main_feature_values' not in st.session_state:
        st.session_state.main_feature_values = None
    if 'predict_result' not in st.session_state:
        st.session_state.predict_result = None

def load_lottie_files(pattern, start, end):
    files = []
    for i in range(start, end + 1):
        files.append(load_lottiefile(pattern.format(i)))
    return files

def load_lottiefile(filepath):
    with open(filepath, "r") as f:
        return json.load(f)
