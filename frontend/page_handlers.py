# page_handlers.py
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import requests
import random
import time
from streamlit_lottie import st_lottie

FASTAPI_URL = "http://localhost:8000/recommend"
FLAVORS_API_URL = "http://localhost:8000/flavors"


def next_page():
    st.session_state.page += 1
    st.rerun()


def handle_welcome_page(welcome_animations):
    welcome_animation = random.choice(welcome_animations)
    st_lottie(welcome_animation, height=300, key="welcome_animation")

    st.markdown(
        """
        <div style="text-align: center;">
            <h1>Welcome to the Cocktail Recommender System</h1>
            <p>Discover your perfect cocktail based on your personal preferences!</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # Center the button using columns
    col1, col2, col3 = st.columns([3, 2, 3])
    with col2:
        if st.button("Start Your Journey"):
            next_page()



def handle_drink_type_page():
    # CSS 스타일링 추가
    st.markdown("""
    <style>
    .element-container:has(#alcoholic_button_span) + div button {
        background-color: #ffb6c1; /* 파스텔 핑크 */
        color: white;
        font-size: 24px;
        padding: 70px; /* 위아래로 길게 */
        border: none;
        border-radius: 50px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
        width: 300px;
        height: 300px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
    }
    .element-container:has(#alcoholic_button_span) + div button:hover {
        background-color: #ff99aa;
    }
    .element-container:has(#non_alcoholic_button_span) + div button {
        background-color: #c5e1a5; /* 파스텔 연두 */
        color: white;
        font-size: 24px;
        padding: 70px; /* 위아래로 길게 */
        border: none;
        border-radius: 50px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
        width: 300px;
        height: 300px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
    }
    .element-container:has(#non_alcoholic_button_span) + div button:hover {
        background-color: #aed581;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        <div style="text-align: center;">
            <h1>Choose Your Drink Type</h1>
            <h2></h2>
        </div>
        """, 
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([3, 1, 3])

    with col1:
        st.markdown('<span id="alcoholic_button_span"></span>', unsafe_allow_html=True)
        if st.button(
            "Alcoholic",
            key="alcoholic_button",
            help="Select this for alcoholic drinks",
            use_container_width=True
        ):
            st.session_state.drink_type = "Alcoholic"
            next_page()

    with col3:
        st.markdown('<span id="non_alcoholic_button_span"></span>', unsafe_allow_html=True)
        if st.button(
            "Non-Alcoholic",
            key="non_alcoholic_button",
            help="Select this for non-alcoholic drinks",
            use_container_width=True
        ):
            st.session_state.drink_type = "Non-Alcoholic"
            next_page()



def handle_flavor_preference_page():
    # CSS 스타일링 추가
    st.markdown("""
    <style>
    .element-container:has(#sweet_button_span) + div button {
        background-color: #ffcccb; /* 파스텔 핑크 */
        color: black;
        font-size: 24px;
        padding: 70px; /* 위아래로 길게 */
        border: none;
        border-radius: 50px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
        width: 200px;
        height: 200px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
    }
    .element-container:has(#sweet_button_span) + div button:hover {
        background-color: #ffb6c1;
    }
    .element-container:has(#sour_button_span) + div button {
        background-color: #ffe4b5; /* 파스텔 노란색 */
        color: black;
        font-size: 24px;
        padding: 70px;
        border: none;
        border-radius: 50px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
        width: 200px;
        height: 200px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
    }
    .element-container:has(#sour_button_span) + div button:hover {
        background-color: #ffd700;
    }
    .element-container:has(#fruity_button_span) + div button {
        background-color: #b0e0e6; /* 파스텔 블루 */
        color: black;
        font-size: 24px;
        padding: 70px;
        border: none;
        border-radius: 50px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
        width: 200px;
        height: 200px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
    }
    .element-container:has(#fruity_button_span) + div button:hover {
        background-color: #add8e6;
    }
    .element-container:has(#spicy_button_span) + div button {
        background-color: #ffb347; /* 파스텔 오렌지 */
        color: black;
        font-size: 24px;
        padding: 70px;
        border: none;
        border-radius: 50px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
        width: 200px;
        height: 200px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
    }
    .element-container:has(#spicy_button_span) + div button:hover {
        background-color: #ffa07a;
    }
    .element-container:has(#herbal_button_span) + div button {
        background-color: #98fb98; /* 파스텔 그린 */
        color: black;
        font-size: 24px;
        padding: 70px;
        border: none;
        border-radius: 50px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
        width: 200px;
        height: 200px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
    }
    .element-container:has(#herbal_button_span) + div button:hover {
        background-color: #90ee90;
    }
    .element-container:has(#bitter_button_span) + div button {
        background-color: #d3d3d3; /* 파스텔 그레이 */
        color: black;
        font-size: 24px;
        padding: 70px;
        border: none;
        border-radius: 50px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
        width: 200px;
        height: 200px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
    }
    .element-container:has(#bitter_button_span) + div button:hover {
        background-color: #c0c0c0;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        <div style="text-align: center;">
            <h1>Choose Your General Preference</h1>
            <h2></h2>
        </div>
        """, 
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.markdown('<span id="sweet_button_span"></span>', unsafe_allow_html=True)
        if st.button(
            "Sweet",
            key="sweet_button",
            help="Expect a deliciously sweet taste with this choice.",
            use_container_width=True
        ):
            st.session_state.general_preference = "Sweet"
            next_page()
        
        st.markdown('<span id="spicy_button_span"></span>', unsafe_allow_html=True)
        if st.button(
            "Spicy",
            key="spicy_button",
            help="Prepare for a kick of spice with this selection.",
            use_container_width=True
        ):
            st.session_state.general_preference = "Spicy"
            next_page()

    with col2:
        st.markdown('<span id="sour_button_span"></span>', unsafe_allow_html=True)
        if st.button(
            "Sour",
            key="sour_button",
            help="This choice brings a tangy and sour experience.",
            use_container_width=True
        ):
            st.session_state.general_preference = "Sour"
            next_page()

        st.markdown('<span id="herbal_button_span"></span>', unsafe_allow_html=True)
        if st.button(
            "Herbal",
            key="herbal_button",
            help="Enjoy a refreshing herbal flavor with this option.",
            use_container_width=True
        ):
            st.session_state.general_preference = "Herbal"
            next_page()

    with col3:
        st.markdown('<span id="fruity_button_span"></span>', unsafe_allow_html=True)
        if st.button(
            "Fruity",
            key="fruity_button",
            help="Select this for a burst of fruity flavors.",
            use_container_width=True
        ):
            st.session_state.general_preference = "Fruity"
            next_page()

        st.markdown('<span id="bitter_button_span"></span>', unsafe_allow_html=True)
        if st.button(
            "Bitter",
            key="bitter_button",
            help="Expect a rich, bitter taste with this choice.",
            use_container_width=True
        ):
            st.session_state.general_preference = "Bitter"
            next_page()



def handle_ingredient_selection_page(top_ingredients, loading_animations):
    st.markdown(
        """
        <div style="text-align: center;">
            <h1>Select Specific Ingredients</h1>
            <h2></h2>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # 초기 맛 그래프 값 설정
    initial_flavors = {
        "boozy": 0.0,
        "sweet": 0.0,
        "sour": 0.0,
        "bitter": 0.0,
        "umami": 0.0,
        "salty": 0.0,
        "astringent": 0.0,
        "perceived_temperature": 0.0,
        "spicy": 0.0,
        "herbal": 0.0,
        "floral": 0.0,
        "fruity": 0.0,
        "nutty": 0.0,
        "creamy": 0.0,
        "smoky": 0.0
    }

    # 초기 맛 그래프 데이터 표시
    if "initial_flavors" not in st.session_state:
        st.session_state.initial_flavors = initial_flavors

    flavors = st.session_state.initial_flavors

    def update_flavor_profile(selected_ingredients):
        if not selected_ingredients:
            return initial_flavors
        
        preferences = {
            "flavor": st.session_state.general_preference,
            "strength": "Medium",  # Static value for now
            "glass_type": "Any",   # Static value for now
            "include_ingredients": selected_ingredients,
            "exclude_ingredients": [],
            "alcoholic": st.session_state.drink_type == "Alcoholic"
        }

        response = requests.post(FLAVORS_API_URL, json=preferences)
        if response.status_code == 200:
            return response.json()
        else:
            st.write("Failed to get flavor prediction. Please try again later.")
            return initial_flavors

    selected_ingredients = st.multiselect("Choose your ingredients", top_ingredients, key="selected_ingredients_multiselect")

    # 재료가 변경될 때마다 맛 프로파일 업데이트
    if selected_ingredients != st.session_state.get("last_selected_ingredients", []):
        flavors = update_flavor_profile(selected_ingredients)
        st.session_state.initial_flavors = flavors
        st.session_state.last_selected_ingredients = selected_ingredients

    # 맛 그래프 표시
    st.markdown("### Flavor Profile")
    radar_data = {
        "labels": list(flavors.keys()),
        "values": list(flavors.values())
    }
    values = radar_data["values"] + [radar_data["values"][0]]  # 첫 번째 값을 다시 추가하여 차원 맞추기
    theta = np.linspace(0.0, 2 * np.pi, len(radar_data["labels"]), endpoint=False)
    theta = np.append(theta, theta[0])  # 첫 번째 값을 다시 추가하여 차원 맞추기

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.fill(theta, values, 'b', alpha=0.1)
    ax.plot(theta, values, 'b', marker='o')
    ax.set_xticks(theta[:-1])
    ax.set_xticklabels(radar_data["labels"])
    st.pyplot(fig)


    if st.button("Get Recommendation"):
        st.session_state.selected_ingredients = selected_ingredients
        st.session_state.loading_animation = random.choice(loading_animations)
        next_page()


def show_loading_page():
    # Scroll to the top of the page
    st.markdown("""
        <style>
        /* Hide scrollbar */
        ::-webkit-scrollbar {
            display: none;
        }
        </style>
        <script>
        window.scrollTo(0, 0);
        </script>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        <div style="text-align: center;">
            <h1>Loading Your Recommendation...</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    st_lottie(st.session_state.loading_animation, height=500, key=f"loading_animation_{random.randint(0, 1000)}")
    # Simulate random latency between 0.5 and 2 seconds
    time.sleep(random.uniform(0.5, 2))

    preferences = {
        "flavor": st.session_state.general_preference,
        "strength": "Medium",
        "glass_type": "Any",
        "include_ingredients": st.session_state.selected_ingredients,
        "exclude_ingredients": [],
        "alcoholic": st.session_state.drink_type == "Alcoholic"
    }

    response = requests.post(FASTAPI_URL, json=preferences)

    if response.status_code == 200:
        cocktail = response.json()
        st.session_state.cocktail = cocktail
        next_page()
    else:
        st.write("Failed to get a cocktail recommendation. Please try again later.")


def show_recommendation(cocktail, cocktail_animations):
    st.markdown(
        """
        <div style="text-align: center;">
            <h1>Your Cocktail Recommendation</h1>
            <h2></h2>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # Calculate the height for the animation
    num_ingredients = len(cocktail['recipe'])
    base_height = 250
    additional_height_per_ingredient = 50
    animation_height = base_height + (num_ingredients * additional_height_per_ingredient)

    # Create tabs
    tab1, tab2 = st.tabs(["Details", "Graphs"])

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            cocktail_animation = random.choice(cocktail_animations)
            st_lottie(cocktail_animation, height=animation_height, key="cocktail_animation")
            # # Display image
            # st.image(cocktail['image_path'], width=300)

        with col2:
            st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
            st.write(f"**Cocktail Name:** {cocktail['cocktail_name']}")
            st.write(f"**Glass Type:** {cocktail['cocktail_glass']}")
            st.write(f"**Category:** {cocktail['category']}")
            st.write(f"**Alcoholic:** {cocktail['alcoholic']}")
            st.write("**Recipe:**")
            for ingredient, amount in cocktail['recipe'].items():
                st.write(f"- {ingredient}: {amount}ml")
            st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        col3, col4 = st.columns(2)

        with col3:
            # Plot Recipe as a Pie Chart
            fig1, ax1 = plt.subplots()
            ax1.pie(cocktail['recipe'].values(), labels=cocktail['recipe'].keys(), autopct='%1.1f%%', startangle=90)
            ax1.axis('equal')
            st.pyplot(fig1)
        
        with col4:
            # Plot Combined Flavors as a Radar Chart
            fig2, ax2 = plt.subplots(subplot_kw={'projection': 'polar'})
            flavors = cocktail['combined_flavors']
            labels = list(flavors.keys())
            values = list(flavors.values())
            values += values[:1]
            theta = np.linspace(0.0, 2 * np.pi, len(labels), endpoint=False)
            theta = np.append(theta, theta[0])
            ax2.fill(theta, values, 'b', alpha=0.1)
            ax2.plot(theta, values, 'b', marker='o')
            ax2.set_xticks(theta[:-1])
            ax2.set_xticklabels(labels)
            st.pyplot(fig2)

    # Center the Restart button
    st.markdown("<div style='text-align: center; margin-top: 20px;'>", unsafe_allow_html=True)
    if st.button("Restart", key="restart"):
        st.session_state.page = 0
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # CSS for button styling
    st.markdown("""
    <style>
    .stButton button {
        background-color: #ff4081; /* 핑크계열 빨강 */
        color: white;
        font-size: 20px;
        padding: 10px 20px;
        border: none;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
    }
    .stButton button:hover {
        background-color: #e91e63;
    }
    </style>
    """, unsafe_allow_html=True)

