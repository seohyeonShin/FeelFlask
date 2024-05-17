import streamlit as st
import pandas as pd
import numpy as np
import random
import time
import plotly.express as px
import os

# DrinkName,ModifiedDate,DrinkID,Alcoholic,Category,ImageUrlPath,Glass,IBA,Instruction,Ingredients,Measures

def show_v2(file_path, indices):
    df = pd.read_csv(file_path)
    rows = df.iloc[indices]

    name = "DrinkName"
    intro = "Instruction"
    category = "Category"
    alcoholic = "Alcoholic"
    ingredients = "Ingredients"
    
    ### idx : index for printing images
    idx = 0

    for _, row in rows.iterrows():
        st.header("", divider="rainbow")
        st.markdown("### :violet[" + str(row[name]) + "]")
        st.markdown("##### :white[" + str(row[intro]) + "]")

        col1, col2 = st.columns([0.5, 0.5])
        with col1:
            show_image (indices, idx)
            idx += 1
        with col2:
            random_5 = random.sample(range(1,6), 5)
            df = pd.DataFrame(dict(
                r=random_5,
                theta=['sweetness','sourness','heaviness',
                       'refreshing', 'alcohol level']))
            fig = px.line_polar(df, r='r', theta='theta', line_close=True)
            st.plotly_chart(fig, use_container_width=True)
        with st.expander("see additional informations"):
            is_alcoholic (alcoholic)
            st.markdown("##### :green[category] :white[" + row[category] + "]")
            st.markdown("##### :green[ingredients] :white[" + str(row[ingredients] + "]"))

def show_image(indices, i):
    image_path = f'./backend/data_works/drinks_img/img_{indices[i]}.jpg'
    if os.path.exists(image_path):
        st.image(image_path, use_column_width=True)
    else:
        st.error(f"Image not found at path: {image_path}")

def is_alcoholic (alcoholic):
    if alcoholic == 'Alcoholic':
        st.markdown("##### :red[alcoholic]")
    else:
        st.markdown("##### :green[non-alcoholic]")