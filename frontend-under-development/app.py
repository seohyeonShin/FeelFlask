import streamlit as st
from streamlit_lottie import st_lottie
from session_mangement import initialize_session_state, load_lottie_files, load_lottiefile
from page_handler import *
import json
import numpy as np
import subprocess
import atexit
from fastapi_srv import app as fastapi_app
import socket
import os
print("Current working directory:", os.getcwd())
def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def start_fastapi():
    if not is_port_in_use(8000):
        subprocess.Popen(["python", "fastapi_srv.py"])
        time.sleep(5)  # FastAPI 앱이 시작될 때까지 잠시 대기

def stop_fastapi():
    if is_port_in_use(8000):
        requests.post("http://localhost:8000/shutdown")

# Load Lottie animations
welcome_animations = load_lottie_files("lottie_files/welcome ({}).json", 1, 10)
loading_animations = load_lottie_files("lottie_files/loading ({}).json", 1, 10)
cocktail_animations = load_lottie_files("lottie_files/cocktail ({}).json", 1, 41)
base_path = os.path.dirname(os.path.abspath(__file__))  # 현재 파일의 절대 경로를 기준으로 디렉토리 경로를 구합니다.
flavor_update_file_path = os.path.join(base_path, 'flavor_update.json') 
with open(flavor_update_file_path, 'r') as fr:
    flavor_info = json.load(fr)

# Initialize session state
initialize_session_state()
def main():
    # Main app logic
    if st.session_state.page == 0:
        handle_welcome_page(welcome_animations)
    elif st.session_state.page == 1:
        handle_drink_type_page()
    elif st.session_state.page == 2:
        handle_input_by_images(st.session_state.drink_type)
    elif st.session_state.page == 3:
        handle_input_seed_ingredient(loading_animations)
    elif st.session_state.page == 4:
        show_loading_page()
    elif st.session_state.page == 5:
        if 'prediction_result' in st.session_state:
            show_recommendation(st.session_state.prediction_result,
                                cocktail_animations)
# elif st.session_state.page == 9:
    # handle_feedback_page()

# def push_data(inputs, pred_ingredients, pred_amounts, feedback):

if __name__ == "__main__":
    start_fastapi()
    atexit.register(stop_fastapi)
    main()