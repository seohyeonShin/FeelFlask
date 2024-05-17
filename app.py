import streamlit as st
import numpy as np
import json
import pandas
from lib.utils import show_v2

st.markdown("# :rainbow[MixMaster] :cocktail:")

### sample categories for debug
categories = []
with open('./lib/categories.json', 'r') as file:
    categories = json.load(file)

with st.sidebar:
    alcohol_content = st.slider('alcohol level : ', 0, 61, 1)
    sweetness = st.slider('select sweetness you want', 1, 5, 1)
    sourness = st.slider('select sour taste you want', 1, 5, 1)
    heaviness = st.slider('select heaviness of drink', 1, 5, 1)
    ingredients = st.multiselect(
        'What ingredients do you want to taste?',
        categories
    )
    clicked = st.button('recommend')
if clicked:
    ### predict

    ### get drink from mongo db

    ### for debug
    file_path = './backend/data_works/preprocessed_alcohol.csv'
    random_integers = np.random.randint(1, 545, size=10)
    ### outputs
    show_v2(file_path, random_integers)

