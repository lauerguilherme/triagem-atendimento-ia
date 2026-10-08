import json
import time
from groq import Groq

GROQ_API_KEY = "SUA_CHAVE_AQUI"
client = Groq(api_key=GROQ_API_KEY)

mensagens_clientes = [
    {"id": 101, "texto": "O produto chegou amassado e a caixa estava aberta. Quero meu dinheiro de volta!"},
    {"id": 102, "texto": "Muito obrigado pelo atendimento, a entrega foi super rápida e o produto é ótimo."},
    {"id": 103, "texto": "Gostaria de saber qual o horário de funcionamento da loja física de São Paulo?"},
    {"id": 104, "texto": "Não consigo fazer login na minha conta, fica dando erro 500."}
]

def analisar_mensagem(texto):
    prompt_usuario = f"Análise: '{texto}'. Responda no formato estrito: SENTIMENTO | INTENÇÃO."
    
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "Você é um classificador de dados. Responda APENAS no formato: SENTIMENTO | INTENCAO. Exemplo: NEGATIVO | Reembolso"},
            {"role": "user", "content": prompt_usuario}
        ],
        model="openai/gpt-oss-20b",
    )
    return chat_completion.choices[0].message.content.strip()

resultados = []

print("[+] Processando lote e gerando relatório JSON...\n")

for item in mensagens_clientes:
    print(f"[-] Analisando ID {item['id']}...")
    analise = analisar_mensagem(item['texto'])
    
    # Adiciona os dados processados na nossa lista
    resultados.append({
        "id_cliente": item["id"],
        "mensagem_original": item["texto"],
        "analise_ia": analise
    })
    time.sleep(1)

# Salvando a saída em um arquivo JSON local
nome_arquivo = "relatorio_triagem.json"
with open(nome_arquivo, "w", encoding="utf-8") as f:
    json.dump(resultados, f, indent=4, ensure_ascii=False)

print(f"\n[+] Relatório concluído e salvo em '{nome_arquivo}'!")