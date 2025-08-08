"""RAG search page for intelligent letter search."""

import streamlit as st
import numpy as np
import os
from utils import load_letters, load_embeddings, show_letter
from config import apply_custom_css

def show_rag_page():
    """Display the RAG search page."""
    apply_custom_css()
    
    st.markdown(
        """
        <h1 class='page-header'>🔍 Busca Inteligente</h1>
        <p class='page-description'>
            Faça perguntas sobre as cartas e encontre as mais relevantes usando inteligência artificial
        </p>
        """,
        unsafe_allow_html=True
    )
    
    # Search input
    st.markdown(
        """
        <div style='margin: 2rem 0 1rem 0;'>
            <h3 style='color: #6c3483; font-family: Montserrat; margin-bottom: 0.5rem;'>
                💭 Faça sua pergunta
            </h3>
            <p style='color: #a569bd; font-family: Montserrat; margin-bottom: 1rem;'>
                Exemplos: "Quem escreveu mais cartas?", "Cartas sobre família", "Mensagens de aniversário"
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    question = st.text_input(
        "Pergunta:",
        placeholder="Digite sua pergunta sobre as cartas...",
        help="Use linguagem natural para buscar cartas relacionadas ao seu interesse"
    )
    
    if question:
        with st.spinner("🔎 Buscando cartas relevantes..."):
            try:
                # Load data
                embeddings = load_embeddings()
                letters = load_letters()
                
                # Get embedding for the question using OpenAI
                import openai
                client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                
                try:
                    response = client.embeddings.create(
                        input=question,
                        model="text-embedding-3-small"
                    )
                    q_emb = np.array(response.data[0].embedding)
                except Exception as e:
                    st.error(f"❌ Erro ao gerar embedding da pergunta: {e}")
                    st.info("💡 Verifique se a variável de ambiente OPENAI_API_KEY está configurada")
                    return
                
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
                
                # Filter and show top 10 relevant letters above threshold
                threshold = 0.2
                top = sorted([x for x in scored if x[0] > threshold], reverse=True)[:10]
                
                if top:
                    st.markdown(
                        f"""
                        <div style='text-align: center; margin: 2rem 0; padding: 1rem; background: linear-gradient(135deg, #a569bd, #6c3483); border-radius: 16px; color: white;'>
                            <h3 style='margin: 0; font-family: Montserrat;'>
                                ✨ Encontradas {len(top)} cartas relevantes
                            </h3>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    for i, (score, idx) in enumerate(top):
                        st.markdown(
                            f"""
                            <div style='margin: 2rem 0 1rem 0;'>
                                <h4 style='color: #6c3483; font-family: Montserrat;'>
                                    📄 Carta {i + 1} 
                                    <span class='similarity-score'>Similaridade: {score:.1%}</span>
                                </h4>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        show_letter(letters[idx])
                else:
                    st.markdown(
                        """
                        <div style='text-align: center; margin: 2rem 0; padding: 2rem; background: rgba(165, 105, 189, 0.1); border-radius: 16px;'>
                            <h3 style='color: #6c3483; font-family: Montserrat; margin-bottom: 1rem;'>
                                🔍 Nenhuma carta relevante encontrada
                            </h3>
                            <p style='color: #a569bd; font-family: Montserrat;'>
                                Tente reformular sua pergunta ou usar termos diferentes
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
            except Exception as e:
                st.error(f"❌ Erro na busca: {e}")
                st.info("💡 Verifique se todos os arquivos de dados estão disponíveis")
    else:
        # Show example queries when no question is entered
        st.markdown(
            """
            <div style='margin: 2rem 0; padding: 2rem; background: linear-gradient(135deg, #fff8f0 0%, #f8f1ff 100%); border-radius: 20px;'>
                <h4 style='color: #6c3483; font-family: Montserrat; margin-bottom: 1rem;'>
                    💡 Sugestões de perguntas:
                </h4>
                <ul style='color: #4d3c4c; font-family: Montserrat; font-size: 1.1em; line-height: 1.8;'>
                    <li>"Cartas sobre aniversários ou celebrações"</li>
                    <li>"Mensagens de amigos da infância"</li>
                    <li>"Cartas recebidas durante os feriados"</li>
                    <li>"Correspondências sobre trabalho ou carreira"</li>
                    <li>"Mensagens de apoio e encorajamento"</li>
                    <li>"Cartas de familiares distantes"</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
