import streamlit as st
import json

def show(drink, image_path):
    col1, col2 = st.columns([0.3, 0.7])
    with col1:
        # st.image("image0001.png", width=100)
        st.image(image_path)
    with btn1:
        st.button(":thumbsup:")
    with btn2:
        st.button(":thumbsdown:")
    with col2:
        st.write("name:", drink['name'])
        st.write("ingredients:", drink['ingredients'])
        st.write("alcohol_content:", drink['alcohol_content'])
        st.write("product_introduction:", drink['product_introduction'])
        st.write("pairing_food:", drink['pairing_food'])
        st.write("brewery:", drink['brewery'])
        st.write("website:", drink['website'])
        st.write("type:", drink['type'])

st.header('korean traditional liquor recommender', divider='rainbow')
alcohol_content = st.slider('alcohol level : ', 0, 100, 1)
sweetness = st.slider('select sweetness you want', 0, 100, 1)
sour = st.slider('select sour taste you want', 0, 100, 1)
feeling = st.selectbox(
  'How do you feel today?',
  ('very bad', 'bad', 'soso', 'good', 'very good')
)
ingredients = st.selectbox(
  'What main ingredient you want to taste',
  ('rice', 'wheat', 'grape', 'xylitol')
)
kind = st.selectbox(
  'the heaviness of alcohol',
  ('very light', 'light', 'heavy', 'very heavy')
)
btn1, btn2, _, pred_btn = st.columns([0.2, 0.2, 0.4, 0.2])
with pred_btn:
    clicked = st.button('recommend')
if clicked:
    ### predict

    ### get drink from mongo db

    ### for debug
    with open("lib/image0001.json", "r", encoding="utf-8") as f:
        drink = json.load(f)
    img = "lib/image0001.png"
    ### show
    show(drink, img)

