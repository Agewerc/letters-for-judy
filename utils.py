"""Utility functions for the Judith Tribute App."""

import json
import os
from PIL import Image
import streamlit as st
from config import LETTERS_PATH, EMBEDDINGS_PATH, IMAGES_DIR

@st.cache_data
def load_letters():
    """Load letters data from JSON file."""
    with open(LETTERS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

@st.cache_data
def load_embeddings():
    """Load embeddings data from JSON file."""
    with open(EMBEDDINGS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def show_letter(letter):
    """Display a letter in a beautiful card format."""
    st.markdown("<div class='letter-card'>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    
    with col1:
        img_path = letter.get("image_path")
        if img_path:
            full_img_path = os.path.join(IMAGES_DIR, os.path.basename(img_path))
            if os.path.exists(full_img_path):
                st.image(
                    Image.open(full_img_path),
                    caption="Imagem da carta",
                    use_container_width=True
                )
            else:
                st.write("📸 Imagem não encontrada")
    
    with col2:
        # Only show title if it exists and is not empty
        title = letter.get('title', '').strip()
        if title:
            st.markdown(
                f"<div class='letter-title'>{title}</div>",
                unsafe_allow_html=True
            )
        st.markdown(
            f"""<div class='letter-meta'>
                <strong>De:</strong> {letter.get('from', 'Desconhecido')}<br>
                <strong>Para:</strong> {letter.get('to', 'Desconhecido')}<br>
                <strong>Data:</strong> {letter.get('date', 'Data desconhecida')}
            </div>""",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<div class='letter-text'>{letter.get('text', 'Texto não disponível')}</div>",
            unsafe_allow_html=True
        )
    
    st.markdown("</div>", unsafe_allow_html=True)
