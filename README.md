# 📄 Extrator de Dados com IA (GPT-4 Vision)

Este projeto é um aplicativo em Python feito com **Streamlit**, que permite aos usuários enviar **imagens de documentos** e extrair automaticamente os dados contidos nelas com o modelo **GPT-4 com visão** da OpenAI. Os dados extraídos são salvos em **planilhas Excel** (.xlsx), com histórico, filtros e autenticação.

---

## 🚀 Funcionalidades

- 📤 Upload de imagem de documentos (.jpg, .png, .jpeg)
- 🤖 Extração inteligente com **GPT-4 Vision API**
- 📁 Geração automática de arquivos Excel
- 🏷️ Atribuição de **tags personalizadas**
- 🕘 Tela de **histórico com filtros** por data, nome e tags
- 🔐 **Login com usuário e senha** (armazenados via `.env`)
- 🔒 Proteção de dados e credenciais sensíveis com `.gitignore`

---

## 📦 Estrutura do Projeto

```plaintext
extrator-folha/
├── app.py                  # Código principal do aplicativo Streamlit
├── .env                    # Suas variáveis secretas (NÃO subir no GitHub)
├── requirements.txt        # Dependências do projeto
├── imagens/                # Imagens salvas (automático)
├── planilhas/              # Planilhas geradas (automático)
├── metadados.json          # Histórico de uploads e análises
└── .gitignore              # Arquivos ignorados no controle de versão
```

---

## ⚙️ Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/extrator-folha.git
cd extrator-folha
```

### 2. Crie o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure suas credenciais

Crie um arquivo `.env` com:

```env
OPENAI_API_KEY=sk-sua-chave-aqui
APP_USERNAME=admin
APP_PASSWORD=senha123
```

---

## ▶️ Como rodar

```bash
streamlit run app.py
```

---

## 🔒 Segurança

- O app exige **login e senha** antes do uso.
- Todas as imagens, planilhas e metadados são salvos localmente.
- Nenhuma informação é compartilhada externamente além da imagem enviada para análise pela OpenAI.

---

## 📚 Tecnologias utilizadas

- [Streamlit](https://streamlit.io/)
- [OpenAI GPT-4 Vision](https://platform.openai.com/docs/guides/vision)
- [Pandas](https://pandas.pydata.org/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [MSAL (para futura integração com OneDrive)](https://pypi.org/project/msal/)

---

## ✨ Próximos passos

- 🔄 Upload automático para OneDrive
- 👥 Controle de múltiplos usuários
- 🗃 Exportar histórico em PDF/CSV
- 📥 Importação de arquivos PDF com múltiplas páginas

---

## 📄 Licença

MIT © Louissilver
