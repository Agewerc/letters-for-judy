"""
Judith Tribute App - A beautiful memorial application
Main entry point for the Streamlit application
"""

import streamlit as st
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.dirname(__file__))

from config import PAGE_TITLE, PAGE_ICON, apply_custom_css
from page_modules.home import show_home_page
from page_modules.gallery import show_gallery_page
from page_modules.rag_search import show_rag_page
from page_modules.photo_gallery import show_photo_gallery_page

# Configure the Streamlit page
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main application function."""
    # Apply custom styling
    apply_custom_css()
    
    # Sidebar navigation
    st.sidebar.markdown(
        """
        <div style='text-align: center; padding: 2rem 1rem; background: linear-gradient(135deg, #fff8f0 0%, #f8f1ff 100%); border-radius: 16px; margin-bottom: 2rem;'>
            <h2 style='color: #6c3483; font-family: Montserrat; margin: 0; font-size: 1.5em;'>
                💌 Judith
            </h2>
            <p style='color: #a569bd; font-family: Montserrat; margin: 0.5rem 0 0 0; font-size: 0.9em;'>
                Em Memória Eterna
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Navigation menu
    page_options = {
        "🏠 Início": "home",
        "📚 Galeria de Cartas": "gallery", 
        "🔍 Busca Inteligente": "rag",
        "📷 Galeria de Fotos": "photos"
    }
    
    selected_page = st.sidebar.selectbox(
        "Navegação",
        options=list(page_options.keys()),
        index=0,
        help="Escolha uma seção para explorar"
    )
    
    # Add some information in the sidebar
    st.sidebar.markdown(
        """
        <div style='margin-top: 2rem; padding: 1.5rem; background: rgba(165, 105, 189, 0.1); border-radius: 12px;'>
            <h4 style='color: #6c3483; font-family: Montserrat; margin: 0 0 0.5rem 0; font-size: 1.1em;'>
                ℹ️ Sobre este tributo
            </h4>
            <p style='color: #4d3c4c; font-family: Montserrat; font-size: 0.9em; line-height: 1.5; margin: 0;'>
                Uma coleção cuidadosamente preservada de cartas e memórias que celebram 
                a vida e o legado de Judith.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Route to the selected page
    page_key = page_options[selected_page]
    
    if page_key == "home":
        show_home_page()
    elif page_key == "gallery":
        show_gallery_page()
    elif page_key == "rag":
        show_rag_page()
    elif page_key == "photos":
        show_photo_gallery_page()

if __name__ == "__main__":
    main()
