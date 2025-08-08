def gallery_page():
    letters = load_letters()
    st.header("Galeria de Cartas")
    LETTERS_PER_PAGE = 10
    total_letters = len(letters)
    total_pages = (total_letters - 1) // LETTERS_PER_PAGE + 1
    page = st.number_input("Página", min_value=1, max_value=total_pages, value=1, step=1)
    start_idx = (page - 1) * LETTERS_PER_PAGE
    end_idx = min(start_idx + LETTERS_PER_PAGE, total_letters)
    st.write(f"Exibindo cartas {start_idx+1} a {end_idx} de {total_letters}")
    for letter in letters[start_idx:end_idx]:
        show_letter(letter)

def rag_page():
    import numpy as np
    st.header("Pesquisa")
    st.markdown("Faça uma pesquisa sobre as cartas da Judith.")
    question = st.text_input("", "")
    if question:
        # Load embeddings and letters
        embeddings = load_embeddings()
        letters = load_letters()
        # Get embedding for the question using OpenAI v1.x API
        import openai
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        try:
            response = client.embeddings.create(
                input=question,
                model="text-embedding-3-small"
            )
            q_emb = np.array(response.data[0].embedding)
        except Exception as e:
            st.error(f"Erro ao gerar embedding da pergunta: {e}")
            return
        # Find most similar letter using precomputed embeddings
        # Compute similarity for all valid embeddings
        scored = []
        for i, emb in enumerate(embeddings):
            if isinstance(emb, dict) and 'embedding' in emb:
                emb_vec = np.array(emb['embedding'])
            else:
                emb_vec = np.array(emb)
            if emb_vec is None or emb_vec.ndim != 1:
                continue
            if emb_vec.dtype.kind not in {'f', 'i'}:
                continue
            if np.any([v is None for v in emb_vec]):
                continue
            score = np.dot(q_emb, emb_vec) / (np.linalg.norm(q_emb) * np.linalg.norm(emb_vec))
            scored.append((score, i))
        # Filter and show top 20 relevant letters above threshold
        threshold = 0.2
        top = sorted([x for x in scored if x[0] > threshold], reverse=True)[:20]
        if top:
            st.write(f"Cartas mais relevantes para: '{question}' (top {len(top)})")
            for score, idx in top:
                show_letter(letters[idx])
                st.success(f"Similaridade: {score:.2f}")
        else:
            st.info("Nenhuma carta relevante encontrada.")

import streamlit as st
import json
import os
from PIL import Image

st.set_page_config(page_title="Tribute to Judith", layout="wide")

LETTERS_PATH = "data/letters.json"
IMAGES_DIR = "data/all_letters"
EMBEDDINGS_PATH = "data/letter_embeddings.json"

def load_letters():
    with open(LETTERS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def load_embeddings():
    with open(EMBEDDINGS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def show_letter(letter):
    st.markdown("<div class='letter-card'>", unsafe_allow_html=True)
    col1, col2 = st.columns([1,2])
    with col1:
        img_path = letter.get("image_path")
        if img_path:
            full_img_path = os.path.join(IMAGES_DIR, os.path.basename(img_path))
            if os.path.exists(full_img_path):
                st.image(Image.open(full_img_path), caption="Imagem", use_container_width=True)
            else:
                st.write("Imagem não encontrada.")
    with col2:
        st.markdown(f"<div class='letter-title'>{letter.get('title', '')}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='letter-meta'><b>De:</b> {letter.get('from', 'Desconhecido')}<br><b>Para:</b> {letter.get('to', 'Desconhecido')}<br><b>Data:</b> {letter.get('date', 'Desconhecido')}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='letter-text'>{letter.get('text', '')}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
def photo_gallery_page():
    import glob
    st.header("Galeria de Fotos da Judith")
    st.markdown("Fotos lindas da Judith ao longo da vida.")
    photo_dir = "data/photos"
    exts = ["*.jpg", "*.jpeg", "*.png", "*.heic", "*.JPG", "*.JPEG", "*.PNG", "*.HEIC"]
    files = []
    for ext in exts:
        files += glob.glob(os.path.join(photo_dir, ext))
    files = sorted(list(set(files)))
    if not files:
        st.info("Nenhuma foto encontrada.")
        return
    num_cols = 3
    for row_start in range(0, len(files), num_cols):
        cols = st.columns(num_cols, gap="small")
        for col_idx, img_path in enumerate(files[row_start:row_start+num_cols]):
            with cols[col_idx]:
                st.markdown("<div class='photo-card' style='margin-top:0;'>", unsafe_allow_html=True)
                try:
                    if img_path.lower().endswith(".heic"):
                        from pillow_heif import open_heif
                        heif_file = open_heif(img_path)
                        img = Image.frombytes(
                            heif_file.mode,
                            heif_file.size,
                            heif_file.data,
                            "raw"
                        )
                    else:
                        img = Image.open(img_path)
                    st.image(img, caption=os.path.basename(img_path), use_container_width=False, width=450)
                except Exception as e:
                    st.warning(f"Não foi possível abrir {img_path}: {e}")
                st.markdown("</div>", unsafe_allow_html=True)

def main():
    st.markdown(
        """
        <style>
        body {
            background: linear-gradient(135deg, #fbeee6 0%, #e8d7f1 100%) !important;
            font-family: 'Montserrat', 'Arial', sans-serif;
        }
        .stApp {
            background: linear-gradient(135deg, #fbeee6 0%, #e8d7f1 100%) !important;
        }
        .letter-card, .photo-card {
            background: #fff8f0;
            border-radius: 18px;
            box-shadow: 0 4px 24px rgba(108,52,131,0.08);
            padding: 24px;
            margin-bottom: 32px;
            border: 1px solid #e8d7f1;
        }
        .letter-title {
            color: #6c3483;
            font-size: 1.5em;
            font-weight: 700;
            margin-bottom: 8px;
        }
        .letter-meta {
            color: #a569bd;
            font-size: 1em;
            margin-bottom: 12px;
        }
        .letter-text {
            font-size: 1.1em;
            color: #4d3c4c;
            margin-bottom: 8px;
        }
        .photo-img {
            border-radius: 16px;
            box-shadow: 0 2px 12px rgba(108,52,131,0.10);
            margin-bottom: 8px;
        }
        .sidebar .sidebar-content {
            background: #fbeee6;
        }
        .wordcloud-word {
            display: inline-block;
            margin: 6px;
            cursor: pointer;
            font-family: Montserrat, Arial, sans-serif;
            color: #6c3483;
            transition: color 0.2s;
        }
        .wordcloud-word:hover {
            color: #a569bd;
            text-decoration: underline;
        }
        </style>
        <link href=\"https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap\" rel=\"stylesheet\">
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <div style='background-color:#fff8f0;padding:32px 24px;border-radius:24px;margin-bottom:32px;box-shadow:0 4px 24px rgba(108,52,131,0.08);'>
            <h1 style='color:#6c3483;font-family:Montserrat,sans-serif;'>Tributo à Judith</h1>
            <h2 style='color:#a569bd;font-family:Montserrat,sans-serif;'>Em Memória de Judith</h2>
            <p style='font-size:20px;color:#4d3c4c;font-family:Montserrat,sans-serif;'>Este aplicativo celebra a vida de Judith através das cartas que ela recebeu de familiares e amigos ao longo de sua vida. Explore as mensagens e memórias compartilhadas com ela.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    page = st.sidebar.selectbox("Escolha uma página", ["Galeria", "Pesquisa", "Galeria de Fotos"])
    if page == "Galeria":
        gallery_page()
    elif page == "Pesquisa":
        rag_page()
    elif page == "Galeria de Fotos":
        photo_gallery_page()

if __name__ == "__main__":
    main()