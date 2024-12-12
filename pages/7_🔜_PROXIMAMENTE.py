import streamlit as st
from styles.css_functions import custom_title

st.set_page_config(page_title="Estudio Local", page_icon="🔜", layout="wide")

custom_title(
    text="Estamos trabajando en....",
    size="2.5em",
    text_align="center",
    margin_left="0px",
    #margin_right="80px",
)

st.markdown(
    """
    <style>
    .center-wrapper {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 80vh; /* Adjust height to control vertical centering */
    }

    .card {
      width: 500px;
      height: 500px;
      background: #07182E;
      position: relative;
      display: flex;
      flex-direction: column; /* Allow stacking content vertically */
      justify-content: center; /* Center content vertically */
      align-items: center; /* Center content horizontally */
      overflow: hidden;
      border-radius: 20px;
      padding: 20px; /* Optional padding for content */
      text-align: center;
    }

    .card h2 {
      z-index: 1;
      color: white;
      font-size: 2em;
      margin-bottom: 20px; /* Add spacing below the title */
    }

    .card p {
      z-index: 1;
      color: white;
      font-size: 1.2em;
    }

    .card::before {
      content: '';
      position: absolute;
      width: 100px;
      background-image: linear-gradient(180deg, rgb(0, 183, 255), rgb(255, 48, 255));
      height: 200%;
      animation: rotBGimg 3s linear infinite;
      transition: all 0.2s linear;
    }

    @keyframes rotBGimg {
      from {
        transform: rotate(0deg);
      }

      to {
        transform: rotate(360deg);
      }
    }

    .card::after {
      content: '';
      position: absolute;
      background: #07182E;
      inset: 5px;
      border-radius: 15px;
    }
    </style>

    <div class="center-wrapper">
        <div class="card">
          <p style="font-size:1.8em;">Ampliar nuestra cobertura a nivel nacional</p><br><br>
          <p style="font-size:1.8em;">Ampliar nuestra base de datos</p><br><br>
          <p style="font-size:1.8em;">Que estés mas contento aún con nuestra app</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
