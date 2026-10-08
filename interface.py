import streamlit as st
from groq import Groq

# Configuração da página
st.set_page_config(page_title="Triagem Inteligente", page_icon="🤖", layout="centered")

st.title("🤖 Triagem de Atendimento com IA")
st.write("Insira a mensagem do cliente para analisar o sentimento e extrair a intenção automaticamente.")

# Chave da API
GROQ_API_KEY = "SUA_CHAVE_AQUI"
client = Groq(api_key=GROQ_API_KEY)

# Campo de texto para o usuário digitar
mensagem_usuario = st.text_area("Mensagem do Cliente:", placeholder="Ex: Comprei ontem e não recebi a nota fiscal...")

# Botão de execução
if st.button("Analisar Mensagem", type="primary"):
    if mensagem_usuario.strip() == "":
        st.warning("Por favor, digite uma mensagem antes de analisar.")
    else:
        with st.spinner("A IA está analisando a mensagem..."):
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "Você é um classificador de dados. Responda estritamente no formato: SENTIMENTO: [POSITIVO/NEUTRO/NEGATIVO] | INTENÇÃO: [Resumo curto da intenção]."
                        },
                        {
                            "role": "user",
                            "content": f"Análise: '{mensagem_usuario}'"
                        }
                    ],
                    model="openai/gpt-oss-20b",
                )
                
                resposta = chat_completion.choices[0].message.content
                
                st.success("Análise Concluída!")
                st.subheader("Resultado:")
                st.info(resposta)
                
            except Exception as e:
                st.error(f"Erro ao conectar com a IA: {e}")