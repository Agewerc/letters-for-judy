"""Home page for the Judith Tribute App."""

import streamlit as st
import os
from PIL import Image
from config import apply_custom_css, PHOTOS_DIR

def show_home_page():
    """Display the beautiful home page."""
    apply_custom_css()
    
    # Main header section with side-by-side layout
    col1, col2 = st.columns([2, 1], gap="large")
    
    with col1:
        st.markdown(
            """
            <div class='main-header' style='text-align: left; margin-right: 1rem;'>
                <h1 class='main-title'>💌 Tributo à Judith</h1>
                <h2 class='main-subtitle'>Em Memória Eterna</h2>
                <p class='main-description' style='text-align: left;'>
                    Este aplicativo é uma homenagem carinhosa à querida Judith, celebrando sua vida 
                    através das preciosas cartas que ela recebeu de familiares e amigos ao longo de 
                    sua jornada. Cada carta conta uma história, cada palavra preserva uma memória, 
                    e cada imagem eterniza um momento especial.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        # Hero image section
        hero_image_path = os.path.join(PHOTOS_DIR, "IMG_7240.jpg")
        if os.path.exists(hero_image_path):
            try:
                image = Image.open(hero_image_path)
                st.markdown(
                    "<div style='text-align: center; margin-top: 1rem;'>",
                    unsafe_allow_html=True
                )
                st.image(
                    image,
                    caption="Judith - Uma vida repleta de amor e memórias",
                    use_container_width=True,
                    output_format="auto"
                )
                st.markdown("</div>", unsafe_allow_html=True)
            except Exception as e:
                st.warning(f"Não foi possível carregar a imagem principal: {e}")
        else:
            st.info("📸 Imagem principal não encontrada em data/photos/IMG_7240.jpg")
    
    # Features section
    st.markdown(
        """
        <div style='margin: 3rem 0;'>
            <h3 style='color: #6c3483; font-size: 2em; text-align: center; margin-bottom: 2rem; font-family: Montserrat;'>
                ✨ Explore as Memórias
            </h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Feature cards
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        st.markdown(
            """
            <div class='photo-card' style='text-align: center; padding: 2rem;'>
                <h4 style='color: #6c3483; font-size: 1.5em; margin-bottom: 1rem;'>📚 Galeria de Cartas</h4>
                <p style='color: #4d3c4c; font-size: 1.1em; line-height: 1.6;'>
                    Navegue pela coleção completa de cartas recebidas por Judith, organizadas 
                    de forma elegante e fácil de explorar.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div class='photo-card' style='text-align: center; padding: 2rem;'>
                <h4 style='color: #6c3483; font-size: 1.5em; margin-bottom: 1rem;'>🔍 Busca Inteligente</h4>
                <p style='color: #4d3c4c; font-size: 1.1em; line-height: 1.6;'>
                    Encontre cartas específicas usando nossa busca semântica avançada. 
                    Faça perguntas e descubra memórias relacionadas.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            """
            <div class='photo-card' style='text-align: center; padding: 2rem;'>
                <h4 style='color: #6c3483; font-size: 1.5em; margin-bottom: 1rem;'>📷 Galeria de Fotos</h4>
                <p style='color: #4d3c4c; font-size: 1.1em; line-height: 1.6;'>
                    Explore uma bela coleção de fotografias que capturam momentos 
                    especiais da vida de Judith.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Footer message
    st.markdown(
        """
        <div style='text-align: center; margin: 3rem 0 2rem 0; padding: 2rem; background: linear-gradient(135deg, #fff8f0 0%, #f8f1ff 100%); border-radius: 20px;'>
            <p style='color: #a569bd; font-size: 1.2em; font-style: italic; margin-bottom: 1rem; font-family: Montserrat;'>
                "As cartas são pontes entre corações, e as memórias são tesouros que o tempo não pode apagar."
            </p>
            <p style='color: #6c3483; font-weight: 600; font-family: Montserrat;'>
                Use o menu lateral para navegar pelas diferentes seções deste tributo.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
