"""Configuration and constants for the Judith Tribute App."""

import streamlit as st

# File paths
LETTERS_PATH = "data/letters.json"
IMAGES_DIR = "data/all_letters"
EMBEDDINGS_PATH = "data/letter_embeddings.json"
PHOTOS_DIR = "data/photos"

# App configuration
PAGE_TITLE = "Tribute to Judith"
PAGE_ICON = "💌"

def apply_custom_css():
    """Apply custom CSS styling to the app."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');
        
        .stApp {
            background: linear-gradient(135deg, #fbeee6 0%, #e8d7f1 100%) !important;
            font-family: 'Montserrat', sans-serif;
        }
        
        .main-header {
            background: linear-gradient(135deg, #fff8f0 0%, #f8f1ff 100%);
            padding: 3rem 2rem;
            border-radius: 24px;
            margin-bottom: 2rem;
            box-shadow: 0 8px 32px rgba(108, 52, 131, 0.12);
            border: 1px solid rgba(108, 52, 131, 0.08);
            text-align: center;
        }
        
        .main-title {
            color: #6c3483;
            font-size: 3.5em;
            font-weight: 700;
            margin-bottom: 0.5rem;
            font-family: 'Montserrat', sans-serif;
            text-shadow: 2px 2px 4px rgba(108, 52, 131, 0.1);
        }
        
        .main-subtitle {
            color: #a569bd;
            font-size: 1.8em;
            font-weight: 400;
            margin-bottom: 1rem;
            font-family: 'Montserrat', sans-serif;
        }
        
        .main-description {
            font-size: 1.2em;
            color: #4d3c4c;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            font-family: 'Montserrat', sans-serif;
        }
        
        .letter-card, .photo-card {
            background: linear-gradient(135deg, #fff8f0 0%, #ffffff 100%);
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(108, 52, 131, 0.12);
            padding: 2rem;
            margin-bottom: 2rem;
            border: 1px solid rgba(108, 52, 131, 0.08);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .letter-card:hover, .photo-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 40px rgba(108, 52, 131, 0.18);
        }
        
        .letter-title {
            color: #6c3483;
            font-size: 1.8em;
            font-weight: 700;
            margin-bottom: 1rem;
            font-family: 'Montserrat', sans-serif;
        }
        
        .letter-meta {
            color: #a569bd;
            font-size: 1.1em;
            margin-bottom: 1.5rem;
            font-weight: 500;
            font-family: 'Montserrat', sans-serif;
        }
        
        .letter-text {
            font-size: 1.1em;
            color: #4d3c4c;
            line-height: 1.7;
            font-family: 'Montserrat', sans-serif;
        }
        
        .hero-image {
            border-radius: 20px;
            box-shadow: 0 12px 48px rgba(108, 52, 131, 0.2);
            border: 3px solid rgba(255, 255, 255, 0.8);
            margin: 2rem auto;
            display: block;
        }
        
        .sidebar .sidebar-content {
            background: linear-gradient(135deg, #fbeee6 0%, #f0e6f7 100%);
            border-radius: 16px;
        }
        
        .stSelectbox > div > div {
            background: white;
            border-radius: 12px;
            border: 2px solid #e8d7f1;
        }
        
        .similarity-score {
            background: linear-gradient(135deg, #a569bd, #6c3483);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: 600;
            display: inline-block;
            margin-top: 1rem;
        }
        
        .page-header {
            color: #6c3483;
            font-size: 2.5em;
            font-weight: 700;
            margin-bottom: 1rem;
            text-align: center;
            font-family: 'Montserrat', sans-serif;
        }
        
        .page-description {
            color: #a569bd;
            font-size: 1.2em;
            text-align: center;
            margin-bottom: 2rem;
            font-family: 'Montserrat', sans-serif;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
