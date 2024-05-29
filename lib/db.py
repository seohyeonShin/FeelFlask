from streamlit_gsheets import GSheetsConnection
import pandas as pd
import streamlit as st

conn = st.experimental_connection("gsheets", type=GSheetsConnection)

def pull_data():
    existing_data = conn.read(worksheet="feedbacks", usecols=list(range(4)), ttl=5)
    existing_data = existing_data.dropna(how='all')
    st.dataframe(existing_data)
    return existing_data

# inputs = [0.0, 0.0, 10.0, 0.0, 5.0, 20.0, 0.0, 0.0, 20.0, 0.0, 0.0, 0.0, 0.0, 80.0, 20.0, 0.0]
# pred_ingredients = ["재료4", "재료5", "재료6"]
# pred_amounts = [10, 20, 30]
# feedback = 1
def push_data(inputs, pred_ingredients, pred_amounts, feedback):
    existing_data = conn.read(worksheet="feedbacks", usecols=list(range(3)), ttl=5)
    new_data = pd.DataFrame(
        {
            "input": [", ".join(str(inputs))],
            "pred_ingredients": [", ".join(pred_ingredients)],
            "pred_amounts": [", ".join(str(pred_amounts))],
            "feedback": [feedback]
        }
    )
    updated_df = pd.concat([existing_data, new_data], ignore_index=True)

    conn.update(worksheet="feedbacks", data=updated_df)

    return True