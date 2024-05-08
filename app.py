import streamlit as st
import json
import pandas
from lib.utils import show_v2

st.markdown("# :rainbow[korean traditional liquor recommender] :cocktail:")

with st.sidebar:
    alcohol_content = st.slider('alcohol level : ', 0, 61, 1)
    sweetness = st.slider('select sweetness you want', 1, 5, 1)
    sourness = st.slider('select sour taste you want', 1, 5, 1)
    heaviness = st.slider('select heaviness of drink', 1, 5, 1)
    ingredients = st.selectbox(
        'What main ingredient you want to taste',
        ('rice', 'wheat', 'grape', 'xylitol')
    )
    clicked = st.button('recommend')
if clicked:
    ### predict

    ### get drink from mongo db

    ### for debug
    file_path = './data/df_products.csv'
    indices = [1, 2, 3, 4]
    show_v2(file_path, indices)

