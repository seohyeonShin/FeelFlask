# data_loader.py
import pandas as pd
import json
import streamlit as st

def load_data():
    with open('train_data.json', 'r') as file:
        train_data = json.load(file)
    train_df = pd.DataFrame(train_data['cocktail_info'])

    ingredients = []
    for recipe in train_df['recipe']:
        ingredients.extend(recipe.keys())
    
    ingredient_counts = pd.Series(ingredients).value_counts()
    top_ingredients = ingredient_counts.head(20).index.tolist()
    
    return train_df, top_ingredients

def load_lottie_files(pattern, start, end):
    files = []
    for i in range(start, end + 1):
        files.append(load_lottiefile(pattern.format(i)))
    return files

def load_lottiefile(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

def initialize_session_state():
    if 'page' not in st.session_state:
        st.session_state.page = 0
    if 'drink_type' not in st.session_state:
        st.session_state.drink_type = None
    if 'general_preference' not in st.session_state:
        st.session_state.general_preference = None
    if 'selected_ingredients' not in st.session_state:
        st.session_state.selected_ingredients = None
    if 'cocktail' not in st.session_state:
        st.session_state.cocktail = None
