# streamlit run app.py
import streamlit as st
import random
from streamlit_lottie import st_lottie
from data_loader import load_data, load_lottie_files, initialize_session_state
from page_handlers import show_recommendation, handle_welcome_page, handle_drink_type_page, handle_flavor_preference_page, show_loading_page, handle_ingredient_selection_page

# Load data
train_df, top_ingredients_list = load_data()

# Load Lottie animations
welcome_animations = load_lottie_files("lottie_files/welcome ({}).json", 1, 10)
loading_animations = load_lottie_files("lottie_files/loading ({}).json", 1, 10)
cocktail_animations = load_lottie_files("lottie_files/cocktail ({}).json", 1, 41)

# Initialize session state
initialize_session_state()

# Main app logic
if st.session_state.page == 0:
    handle_welcome_page(welcome_animations)
elif st.session_state.page == 1:
    handle_drink_type_page()
elif st.session_state.page == 2:
    handle_flavor_preference_page()
elif st.session_state.page == 3:
    handle_ingredient_selection_page(top_ingredients_list, loading_animations)
elif st.session_state.page == 4:
    show_loading_page()
elif st.session_state.page == 5:
    if 'cocktail' in st.session_state:
        show_recommendation(st.session_state.cocktail, cocktail_animations)