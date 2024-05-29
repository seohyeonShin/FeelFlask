import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import requests
import random
import time
from streamlit_lottie import st_lottie
from PIL import Image


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
            st.session_state.drink_type = "Non_Alcoholic"
            next_page()


def handle_input_main_features_page(drinktype): # input st.session_state.drink_type !
    # sweet, sour, bitter, spicy, herbal 값을 입력으로 받습니다.
    
    st.markdown(
        """
        <div style="text-align: center;">
            <h1>Input your taste!</h1>
            <h2></h2>
        </div>
        """,
        unsafe_allow_html=True
    )
    ABV = 0.0 # in case Non-Alcoholic

    if drinktype=="Alcoholic":
        ABV = st.slider("ABV", 0.0, 60.0, 30.0, step=0.1)

    sweet = st.slider("Sweetness", 0.0, 100.0, 50.0, step=0.1)
    sour = st.slider("Sourness", 0.0, 100.0, 50.0, step=0.1)
    bitter = st.slider("Bitterness", 0.0, 100.0, 50.0, step=0.1)
    spicy = st.slider("Spiciness", 0.0, 100.0, 50.0, step=0.1)
    herbal = st.slider('Herbal', 0.0, 100.0, 50.0, step=0.1)

    if st.button("Get Recipe"):
        input_features = {
            "ABV": ABV,
            "sweet": sweet,
            "sour": sour,
            "bitter": bitter,
            "spicy": spicy,
            "herbal": herbal
        }
    st.session_state.main_feature_values = input_features
    next_page()



# fruity, nutty, floral의 값은 수치값이 아닌 그림 선택형으로 입력받습니다.
def handle_flavor_preference_page():

    st.markdown(
        """
        <div style="text-align: center;">
            <h1>Select Strength Option</h1>
            <h2></h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    strength_options = ["Very Strong", "Strong", "Moderate", "Weak", "None"]

    floral_op = st.selectbox('Strength of Floral', strength_options)
    fruity_op = st.selectbox('Strength of Fruity', strength_options)
    nutty_op = st.selectbox('Strength of Nutty', strength_options)
    
    floral = 0.0
    fruity = 0.0
    nutty = 0.0
    if floral_op == "Very Strong":
        floral = random.uniform(0.8, 1) * 100
    elif floral_op == "Strong":
        floral = random.uniform(0.6, 0.8) * 100
    elif floral_op == "Moderate":
        floral = random.uniform(0.4, 0.6) * 100
    elif floral_op == "Weak":
        floral = random.uniform(0.2, 0.4)* 100
    elif floral_op == "None":
        floral = 0.0
        
    if fruity_op == "Very Strong":
        fruity = random.uniform(0.8, 1) * 100
    elif fruity_op == "Strong":
        fruity = random.uniform(0.6, 0.8) * 100
    elif fruity_op == "Moderate":
        fruity = random.uniform(0.4, 0.6) * 100
    elif fruity_op == "Weak":
        fruity = random.uniform(0.2, 0.4)* 100
    elif fruity_op == "None":
        fruity = 0.0
        
    if nutty_op == "Very Strong":
        nutty = random.uniform(0.8, 1) * 100
    elif nutty_op == "Strong":
        nutty = random.uniform(0.6, 0.8) * 100
    elif nutty_op == "Moderate":
        nutty = random.uniform(0.4, 0.6) * 100
    elif nutty_op == "Weak":
        nutty = random.uniform(0.2, 0.4)* 100
    elif nutty_op == "None":
        nutty = 0.0

    if st.button(
        "Determine",
        key="determine_choice",
        help="finishing the choice",
        use_container_width=True
    ):
        input_features = st.session_state.main_feature_values
        input_features['floral'] = floral
        input_features['fruity'] = fruity
        input_features['nutty'] = nutty
        st.session_state.main_feature_values = input_features
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

    main_features = st.session_state.main_feature_values
    main_features['boozy'] = main_features['ABV']*0.9
    main_features['astringent'] = main_features['bitter']*0.9
    main_features['umami'] = main_features['herbal'] * 0.5 + main_features['spicy'] * 0.5
    main_features['salty'] = random.uniform(0, 1)*100
    main_features['perceived_t'] = random.randint(30, 50)
    main_features['creamy'] = random.uniform(0, 1)*100
    main_features['smoky'] = random.uniform(0, 1)*100
    
    response = requests.post('http://localhost:8000/predict/', json=main_features)

    if response.status_code == 200:
        predict = response.json()
        st.session_state.prediction_result = predict
        next_page()
    else:
        st.write("Failed to get a cocktail recommendation. Please try again later.")


def show_recommendation(cocktail, cocktail_animations, ind_to_flavor):
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
            st.write("**Recommend Recipe:**")
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

            # 모델의 출력 결과를 다시 레시피 이름으로 변환할 필요가 있습니다.
            # 각 레시피 마다 갖는 flavor 정보를 이용하여 레시피의 총체적인 flavor를 계산합니다.

            # Plot Combined Flavors as a Radar Chart
            fig2, ax2 = plt.subplots(subplot_kw={'projection': 'polar'})

            cocktail_flavor = {}
            sum_amounts = sum(cocktail['recipe'].values())
            for key, amounts in enumerate(cocktail['recipe']):
                for flavor, feature_value in ind_to_flavor[key].items():
                    if flavor not in cocktail_flavor.keys(): # key is ingredient's unique index
                        cocktail_flavor[flavor] = amounts * feature_value / sum_amounts
                    else:
                        cocktail_flavor[flavor] += amounts * feature_value / sum_amounts

            labels = list(cocktail_flavor.keys())
            values = list(cocktail_flavor.values())
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
