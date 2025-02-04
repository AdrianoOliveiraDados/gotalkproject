import time
import streamlit as st
import pandas as pd
import os
from io import BytesIO
from gtts import gTTS
from utils import cria_chain_conversa, PASTA_ARQUIVOS
from pathlib import Path
from io import StringIO
from configs import get_config

st.set_page_config(layout="wide")

def exibir_resposta_digitando(placeholder, resposta):
    """Exibe a resposta de forma gradual, simulando uma digitação."""
    placeholder.text_area("GoTalk:", "⏳ Processando resposta...", height=500)
    time.sleep(2)  # Simula um pequeno tempo de espera inicial

    texto_exibido = ""
    for palavra in resposta.split():
        texto_exibido += palavra + " "
        placeholder.text_area("GoTalk:", texto_exibido, height=500)
        time.sleep(0.1)  # Ajuste o tempo entre cada palavra para um efeito mais lento

def gerar_audio(texto, idioma='pt'):
    tts = gTTS(texto, lang=idioma)
    audio_data = BytesIO()
    tts.write_to_fp(audio_data)
    audio_data.seek(0)
    return audio_data

def sidebar():
    st.sidebar.image("./arquivos/unimed.jpg", width=100)
    st.sidebar.title("📚 Ánalise seus documentos")
    st.sidebar.markdown("Faça o upload dos seus documentos para começar.")

    uploaded_pdfs = st.sidebar.file_uploader(
        'Adicione seus arquivos PDF',
        type=['pdf'],
        accept_multiple_files=True
    )

    pasta = Path(PASTA_ARQUIVOS)
    if uploaded_pdfs:
        for arquivo in pasta.glob('*.pdf'):
            arquivo.unlink()
        for pdf in uploaded_pdfs:
            with open(pasta / pdf.name, 'wb') as f:
                f.write(pdf.read())

    fonte_selecionada = st.sidebar.selectbox(
        "Selecione a fonte de dados:",
        ["Nenhuma", "Dados ANS", "Dados Tableau", "Fontes Externas", "Sinistralidade", "Contas Médicas"]
    )

    fonte_arquivos = {
        "Dados ANS": "Dados_ANS.pdf",
        "Dados Tableau": "Dados_Tableau.pdf",
        "Fontes Externas": "Fontes_Externas.pdf",
        "Contas Médicas": "Contas_Medicas.pdf"
    }

    if 'df_grafico' not in st.session_state:
        st.session_state['df_grafico'] = None

    if fonte_selecionada in fonte_arquivos:
        for arquivo in pasta.glob('*.pdf'):
            arquivo.unlink()

        caminho_origem = os.path.join("fontes_preexistentes", fonte_arquivos[fonte_selecionada])
        caminho_destino = pasta / fonte_arquivos[fonte_selecionada]

        if not os.path.isfile(caminho_origem):
            st.sidebar.error(f"Arquivo {fonte_arquivos[fonte_selecionada]} não encontrado.")
        else:
            with open(caminho_origem, 'rb') as src, open(caminho_destino, 'wb') as dst:
                dst.write(src.read())

    label_botao = '🔄 Pergunte a IA' if 'chain' not in st.session_state else '🔄 Pergunte a IA'
    if st.sidebar.button(label_botao, use_container_width=True):
        if len(list(pasta.glob('*.pdf'))) == 0 and st.session_state.get('df_grafico') is None:
            st.sidebar.error('Adicione arquivos PDF ou selecione uma fonte de dados para inicializar o chatbot.')
        else:
            st.sidebar.success('Inicializando a IA...')
            cria_chain_conversa()

def chat_window():
    st.markdown("<h1 style='text-align: center;'>🩺 Go<span style='color:#009863;'>Talk</span></h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Bem vindo Adriano!</h3>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid #ccc;' />", unsafe_allow_html=True)

    if 'chain' not in st.session_state and st.session_state.get('df_grafico') is None:
        st.warning("📂 Por favor, faça o upload dos PDFs ou selecione uma fonte de dados na barra lateral para começar.")
        st.stop()

    container = st.container()
    nova_mensagem = st.chat_input("💬 Escreva sua pergunta aqui...")

    if nova_mensagem:
        with container:
            st.markdown(f"**Você:** {nova_mensagem}")

        respostas_fixas = get_config("respostas_fixas")
        resposta = respostas_fixas.get(nova_mensagem.strip(), None)
        resposta_placeholder = st.empty()  # Espaço para exibição gradual da resposta

        if resposta:
            exibir_resposta_digitando(resposta_placeholder, resposta)
        else:
            if 'chain' in st.session_state:
                with st.spinner("GoTalk está pensando..."):
                    resposta_placeholder.text_area("GoTalk:", "⏳ Processando resposta...", height=500)
                    time.sleep(2)

                    resposta_dict = chain.invoke({'question': nova_mensagem})
                    resposta = resposta_dict.get('answer', "Não foi possível gerar uma resposta.")

                exibir_resposta_digitando(resposta_placeholder, resposta)

            else:
                resposta = "Sou uma Inteligência Artificial especialista em dados. Já temos os gráficos para análise prontos. O que você gostaria de saber sobre esses dados?"
                exibir_resposta_digitando(resposta_placeholder, resposta)

        # 🔊 Geração de áudio
        audio_data = gerar_audio(resposta, idioma='pt')
        st.audio(audio_data, format="audio/mp3")

def main():
    sidebar()
    chat_window()

if __name__ == '__main__':
    main()
