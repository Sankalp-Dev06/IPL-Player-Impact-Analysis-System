import streamlit as st

def load_theme():
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    section[data-testid="stSidebar"] h2 {
        color: white;
    }

    section[data-testid="stSidebar"] .stMarkdown {
        color: #9CA3AF;
    }

    .block-container {
        padding-top: 2rem;
    }

    h1, h2, h3 {
        font-weight: 600;
    }

    </style>
    """, unsafe_allow_html=True)