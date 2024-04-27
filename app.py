import streamlit as st
import json

def show():
  col1, col2 = st.columns(2)
  st.image("image0001.png", width=100)
  with open("image0001.json", "r", encoding="utf-8") as f:
    file = json.load(f)
  st.write("Type:", file["type"])
  # st.write("Ingredients:", file["ingredients"])
  st.write("Alcohol Level:", file["alcohol_level"])
  st.write("Volume:", file["volume"])
  st.write("Introduction:", file["introduction"])
  st.write("Brewery:", file["brewery"])
  st.write("Homepage:", file["homepage"])

alcohol_level = st.slider('alcohol level : ', 0, 100, 1)
sweetness = st.slider('select sweetness you want', 0, 100, 1)
sour = st.slider('select sour taste you want', 0, 100, 1)
# st.write('sweetness : ', sweet)

feeling = st.selectbox(
  'How do you feel today?',
  ('very bad', 'bad', 'soso', 'good', 'very good')
)
main_ingredient = st.selectbox(
  'What main ingredient you want to taste',
  ('rice', 'wheat', 'grape', 'xylitol')
)
kind = st.selectbox(
  'the heaviness of alcohol',
  ('very light', 'light', 'heavy', 'very heavy')
)




clicked = st.button('전통주 찾기!!')
if clicked:
  show()

