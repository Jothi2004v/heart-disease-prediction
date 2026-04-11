import streamlit as st
from streamlit_option_menu import option_menu
import Home
import About
import Prediction


st.set_page_config(page_title="Heart Disease Prediction", page_icon=":man_health_worker:", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "Home"
    
st.markdown("<style>div.block-container{margin-top:-60px;}</style>", unsafe_allow_html=True)
st.markdown(
    """
    <style>
        .centered-title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            font-style: italic;
        }
    </style>
    <h1 class="centered-title">HEART DISEASE ANALYSIS🫀</h1>
    """,
    unsafe_allow_html=True
)
st.markdown("<br>", unsafe_allow_html=True)



with st.sidebar:
    selected_menu = option_menu(
        menu_title=None,
        options=["Home", "About", "Prediction"],
        icons=["house-fill","exclamation-circle-fill","activity"],
        default_index=0
    )

if selected_menu == "Home":
    Home.show_home()

if selected_menu == "About":
    About.show_about()

if selected_menu == "Prediction":
    Prediction.predict()

