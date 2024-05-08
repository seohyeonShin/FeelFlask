import streamlit as st
import pandas as pd
import numpy as np
import random
import time
import plotly.express as px

def show_v2(file_path, indices):
    df = pd.read_csv(file_path)
    rows = df.iloc[indices]

    name = "name"
    intro = "product_introduction"
    foods = "pairing_food"
    alcohol = "alcohol_content"
    ingredients = "ingredients"
    price = "Naver Price"
    link = "Naver Link"

    for _, row in rows.iterrows():
        st.header("", divider="rainbow")
        st.markdown("### :violet[" + str(row[name]) + "]")
        st.markdown("##### :white[" + str(row[intro]) + "]")

        col1, col2 = st.columns([0.5, 0.5])
        with col1:
            st.markdown("[![naver link](app/lib/img_test.png)]({row[link]})")
            # st.image('./lib/img_test.png', use_column_width=True)
            # st.write("[buy this drink](%s)" % row[link])
        with col2:
            random_5 = random.sample(range(1,6), 5)
            df = pd.DataFrame(dict(
                r=random_5,
                theta=['sweetness','sourness','heaviness',
                       'refreshing', 'alcohol level']))
            fig = px.line_polar(df, r='r', theta='theta', line_close=True)
            st.plotly_chart(fig, use_container_width=True)
        with st.expander("see additional informations"):
            st.markdown("##### alcohol level :red[" + str(row[alcohol]) + "]")
            st.markdown("##### pairing foods :green[" + str(row[foods]) + "]")
            st.markdown("##### ingredients :white[" + str(row[ingredients] + "]"))
            st.markdown("##### price :white[" + str(row[price] + "]"))
