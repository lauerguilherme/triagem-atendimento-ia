import os
import io
import pandas as pd
import streamlit as st
from groq import Groq

# Configuração da página
st.set_page_config(page_title="Triagem Inteligente com IA", page_icon="🤖", layout="wide")

st.title("🤖 Triagem de Atendimento com IA")
st.write("Análise individual ou em lote de mensagens de clientes utilizando Inteligência Artificial.")

# Inicialização do Cliente Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "SUA_CHAVE_AQUI")
client = Groq(api_key=GROQ_API_KEY)

# Função auxiliar para processar uma mensagem com a Groq
def analisar_mensagem(mensagem):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Você é um classificador de atendimento. Responda ESTRITAMENTE no formato: SENTIMENTO: [POSITIVO/NEUTRO/NEGATIVO] | INTENÇÃO: [Resumo em até 5 palavras]."
                },
                {
                    "role": "user",
                    "content": f"Análise: '{mensagem}'"
                }
            ],
            model="openai/gpt-oss-20b",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"ERRO: {e}"

# Criação das Abas na Interface
aba1, aba2 = st.tabs(["💬 Análise Individual", "📁 Análise em Lote (Excel/CSV)"])

# --- ABA 1: ANÁLISE INDIVIDUAL ---
with aba1:
    mensagem_usuario = st.text_area("Mensagem do Cliente:", placeholder="Ex: Comprei ontem e não recebi a nota fiscal...")
    
    if st.button("Analisar Mensagem Individual", type="primary"):
        if not mensagem_usuario.strip():
            st.warning("Por favor, digite uma mensagem.")
        else:
            with st.spinner("A IA está analisando..."):
                resposta = analisar_mensagem(mensagem_usuario)
                st.success("Análise Concluída!")
                st.info(resposta)

# --- ABA 2: ANÁLISE EM LOTE ---
with aba2:
    st.subheader("Carregar Ficheiro de Mensagens")
    st.write("Suba um ficheiro `.csv` ou `.xlsx` contendo uma coluna com as mensagens dos clientes.")
    
    arquivo_enviado = st.file_uploader("Escolha um ficheiro", type=["csv", "xlsx"])
    
    if arquivo_enviado is not None:
        try:
            if arquivo_enviado.name.endswith(".csv"):
                df = pd.read_csv(arquivo_enviado)
            else:
                df = pd.read_excel(arquivo_enviado)
                
            st.write("### Pré-visualização dos dados carregados:")
            st.dataframe(df.head())
            
            colunas = df.columns.tolist()
            coluna_selecionada = st.selectbox("Selecione a coluna que contém as mensagens:", colunas)
            
            if st.button("Processar Ficheiro com IA", type="primary"):
                resultados = []
                progresso = st.progress(0)
                status_texto = st.empty()
                
                total_linhas = len(df)
                
                for idx, mensagem in enumerate(df[coluna_selecionada]):
                    status_texto.text(f"Analisando linha {idx + 1} de {total_linhas}...")
                    
                    if pd.isna(mensagem) or str(mensagem).strip() == "":
                        resultados.append("SENTIMENTO: NEUTRO | INTENÇÃO: Mensagem vazia")
                    else:
                        res = analisar_mensagem(str(mensagem))
                        resultados.append(res)
                    
                    progresso.progress((idx + 1) / total_linhas)
                
                df["Análise da IA"] = resultados
                
                status_texto.text("Processamento concluído com sucesso!")
                st.success("Todas as linhas foram analisadas!")
                
                st.write("### Resultado da Triagem:")
                st.dataframe(df)
                
                buffer_excel = io.BytesIO()
                with pd.ExcelWriter(buffer_excel, engine="openpyxl") as writer:
                    df.to_excel(writer, index=False, sheet_name="Triagem")
                
                st.download_button(
                    label="📥 Baixar Relatório em Excel (.xlsx)",
                    data=buffer_excel.getvalue(),
                    file_name="relatorio_triagem_ia.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                
        except Exception as err:
            st.error(f"Erro ao processar o ficheiro: {err}")