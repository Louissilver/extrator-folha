import streamlit as st
import openai
import base64
import pandas as pd
import json
import re
from dotenv import load_dotenv
import os
from datetime import datetime

# ========== CONFIGURAÇÕES INICIAIS ==========
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Autenticação simples por sessão
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False


def autenticar():
    st.title("🔐 Login necessário")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if usuario == os.getenv("APP_USERNAME") and senha == os.getenv("APP_PASSWORD"):
            st.session_state.autenticado = True
            st.success("✅ Login realizado com sucesso!")
            st.rerun()
        else:
            st.error("❌ Credenciais inválidas")


if not st.session_state.autenticado:
    autenticar()
    st.stop()

# ========== CONFIGURAÇÃO DO APP ==========
st.set_page_config(page_title="📄 Extrator de Folha", layout="wide")
st.title("📄 Extrair dados de uma folha e salvar no Excel")

# Pastas e arquivos
os.makedirs("imagens", exist_ok=True)
os.makedirs("planilhas", exist_ok=True)
METADADOS_PATH = "metadados.json"
if not os.path.exists(METADADOS_PATH):
    with open(METADADOS_PATH, "w") as f:
        json.dump([], f)


# Funções auxiliares
def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.read()).decode("utf-8")


def salvar_metadado(entry):
    with open(METADADOS_PATH, "r") as f:
        data = json.load(f)
    data.append(entry)
    with open(METADADOS_PATH, "w") as f:
        json.dump(data, f, indent=2)


# Navegação
aba = st.sidebar.radio(
    "📂 Escolha uma seção", ["📤 Enviar nova imagem", "🕘 Histórico"]
)

# ========== ABA 1 ==========
if aba == "📤 Enviar nova imagem":
    uploaded_file = st.file_uploader(
        "Envie uma imagem da folha 📸", type=["jpg", "jpeg", "png"]
    )

    tags = st.multiselect(
        "🏷️ Selecione uma ou mais tags para este envio",
        [
            "auto de infração",
            "recibo",
            "nota fiscal",
            "documento geral",
            "formulário",
            "documento técnico",
        ],
    )

    if uploaded_file:
        st.image(uploaded_file, caption="Imagem enviada", width=400)

        if st.button("🔍 Analisar e Gerar Excel"):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_imagem = f"imagens/folha_{timestamp}.jpg"
            with open(nome_imagem, "wb") as f:
                f.write(uploaded_file.getbuffer())

            base64_image = encode_image(open(nome_imagem, "rb"))

            with st.spinner("Enviando para análise com GPT-4 Vision..."):
                response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "Extraia os dados desta imagem como tabela e retorne em formato JSON.",
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}"
                                    },
                                },
                            ],
                        }
                    ],
                    max_tokens=1500,
                )

            resposta = response.choices[0].message.content
            st.markdown("### 📋 Resposta do GPT")
            st.code(resposta)

            resposta_limpa = (
                re.sub(r"```(?:json)?\n?", "", resposta).replace("```", "").strip()
            )
            try:
                dados = json.loads(resposta_limpa)
                df = (
                    pd.json_normalize(dados)
                    if isinstance(dados, dict)
                    else pd.DataFrame(dados)
                )

                nome_excel = f"planilhas/dados_{timestamp}.xlsx"
                df.to_excel(nome_excel, index=False)
                st.success("✅ Planilha criada com sucesso!")

                with open(nome_excel, "rb") as f:
                    st.download_button(
                        "📥 Baixar Excel", f, file_name=os.path.basename(nome_excel)
                    )

                salvar_metadado(
                    {
                        "timestamp": timestamp,
                        "nome_excel": os.path.basename(nome_excel),
                        "nome_imagem": os.path.basename(nome_imagem),
                        "tags": tags,
                        "data": datetime.now().strftime("%Y-%m-%d"),
                    }
                )

            except Exception as e:
                st.error("Erro ao interpretar JSON retornado pela IA.")
                st.code(resposta)
                st.exception(e)

# ========== ABA 2 ==========
elif aba == "🕘 Histórico":
    st.subheader("📜 Histórico de envios")

    filtro_nome = st.text_input("🔍 Filtrar por nome de arquivo (parcial)")
    filtro_data = st.date_input("📅 Filtrar por data específica (opcional)", value=None)
    filtro_tags = st.multiselect(
        "🏷️ Filtrar por tags",
        [
            "auto de infração",
            "recibo",
            "nota fiscal",
            "documento geral",
            "formulário",
            "documento técnico",
        ],
    )

    with open(METADADOS_PATH, "r") as f:
        historico = json.load(f)

    resultados = []
    for item in historico:
        cond_nome = filtro_nome.lower() in item["nome_excel"].lower()
        cond_data = not filtro_data or item["data"] == filtro_data.strftime("%Y-%m-%d")
        cond_tags = not filtro_tags or any(tag in item["tags"] for tag in filtro_tags)

        if cond_nome and cond_data and cond_tags:
            resultados.append(item)

    if resultados:
        for item in sorted(resultados, key=lambda x: x["timestamp"], reverse=True):
            with st.expander(f"🗂 {item['nome_excel']} ({item['data']})"):
                st.markdown(f"**Tags:** {', '.join(item['tags'])}")
                st.image(f"imagens/{item['nome_imagem']}", width=250)
                with open(f"planilhas/{item['nome_excel']}", "rb") as f:
                    st.download_button(
                        "📥 Baixar Excel", f, file_name=item["nome_excel"]
                    )
    else:
        st.info("Nenhum resultado encontrado com os filtros aplicados.")
