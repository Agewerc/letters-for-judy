"""Gallery page for displaying letters."""

import streamlit as st
from utils import load_letters, show_letter
from config import apply_custom_css

def show_gallery_page():
    """Display the letters gallery page."""
    apply_custom_css()
    
    st.markdown(
        """
        <h1 class='page-header'>📚 Galeria de Cartas</h1>
        <p class='page-description'>
            Explore a coleção completa de cartas recebidas por Judith, cada uma contando uma história única
        </p>
        """,
        unsafe_allow_html=True
    )
    
    letters = load_letters()
    
    # Pagination settings
    LETTERS_PER_PAGE = 5
    total_letters = len(letters)
    total_pages = (total_letters - 1) // LETTERS_PER_PAGE + 1
    
    # Page selector
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        page = st.number_input(
            "Página",
            min_value=1,
            max_value=total_pages,
            value=1,
            step=1,
            help=f"Navegue pelas {total_pages} páginas de cartas"
        )
    
    # Calculate indices
    start_idx = (page - 1) * LETTERS_PER_PAGE
    end_idx = min(start_idx + LETTERS_PER_PAGE, total_letters)
    
    # Show current page info
    st.markdown(
        f"""
        <div style='text-align: center; margin: 1rem 0 2rem 0; color: #a569bd; font-size: 1.1em; font-family: Montserrat;'>
            Exibindo cartas {start_idx + 1} a {end_idx} de {total_letters} cartas
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Display letters
    for i, letter in enumerate(letters[start_idx:end_idx]):
        with st.container():
            show_letter(letter)
            
            # Add some spacing between letters
            if i < len(letters[start_idx:end_idx]) - 1:
                st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)
    
    # Navigation help
    if total_pages > 1:
        st.markdown(
            f"""
            <div style='text-align: center; margin: 2rem 0; padding: 1rem; background: rgba(165, 105, 189, 0.1); border-radius: 12px;'>
                <p style='color: #6c3483; font-family: Montserrat; margin: 0;'>
                    💡 Use o seletor acima para navegar entre as {total_pages} páginas de cartas
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
