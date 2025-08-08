"""Photo gallery page for displaying Judith's photos."""

import streamlit as st
import glob
import os
from PIL import Image
from config import apply_custom_css, PHOTOS_DIR

def show_photo_gallery_page():
    """Display the photo gallery page."""
    apply_custom_css()
    
    st.markdown(
        """
        <h1 class='page-header'>📷 Galeria de Fotos</h1>
        <p class='page-description'>
            Uma coleção de fotografias preciosas que capturam momentos especiais da vida de Judith
        </p>
        """,
        unsafe_allow_html=True
    )
    
    # Get all photo files
    exts = ["*.jpg", "*.jpeg", "*.png", "*.heic", "*.JPG", "*.JPEG", "*.PNG", "*.HEIC"]
    files = []
    for ext in exts:
        files += glob.glob(os.path.join(PHOTOS_DIR, ext))
    files = sorted(list(set(files)))
    
    if not files:
        st.markdown(
            """
            <div style='text-align: center; margin: 3rem 0; padding: 2rem; background: rgba(165, 105, 189, 0.1); border-radius: 20px;'>
                <h3 style='color: #6c3483; font-family: Montserrat; margin-bottom: 1rem;'>
                    📸 Nenhuma foto encontrada
                </h3>
                <p style='color: #a569bd; font-family: Montserrat;'>
                    Adicione fotos na pasta data/photos para visualizá-las aqui
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        return
    
    st.markdown(
        f"""
        <div style='text-align: center; margin: 1rem 0 2rem 0; color: #a569bd; font-size: 1.2em; font-family: Montserrat;'>
            ✨ {len(files)} fotografias encontradas
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Display photos in a responsive grid
    num_cols = 3
    for row_start in range(0, len(files), num_cols):
        cols = st.columns(num_cols, gap="medium")
        for col_idx, img_path in enumerate(files[row_start:row_start + num_cols]):
            with cols[col_idx]:
                st.markdown("<div class='photo-card' style='padding: 1rem;'>", unsafe_allow_html=True)
                try:
                    if img_path.lower().endswith(".heic"):
                        try:
                            from pillow_heif import open_heif
                            heif_file = open_heif(img_path)
                            img = Image.frombytes(
                                heif_file.mode,
                                heif_file.size,
                                heif_file.data,
                                "raw"
                            )
                        except ImportError:
                            st.warning("⚠️ pillow-heif não instalado. Não é possível exibir arquivos HEIC.")
                            continue
                    else:
                        img = Image.open(img_path)
                    
                    # Create a nice frame effect
                    st.image(
                        img,
                        caption=f"📸 {os.path.basename(img_path)}",
                        use_container_width=True,
                        output_format="auto"
                    )
                    
                except Exception as e:
                    st.markdown(
                        f"""
                        <div style='text-align: center; padding: 2rem; background: rgba(255, 0, 0, 0.1); border-radius: 12px; color: #d63384;'>
                            <p style='margin: 0; font-family: Montserrat;'>
                                ❌ Erro ao carregar<br>
                                <small>{os.path.basename(img_path)}</small>
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                
                st.markdown("</div>", unsafe_allow_html=True)
        
        # Add some spacing between rows
        st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)
    
    # Footer with tips
    st.markdown(
        """
        <div style='text-align: center; margin: 3rem 0 1rem 0; padding: 1.5rem; background: rgba(165, 105, 189, 0.1); border-radius: 16px;'>
            <p style='color: #6c3483; font-family: Montserrat; margin: 0; font-size: 1.1em;'>
                💡 Clique nas imagens para visualizá-las em tamanho completo
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
