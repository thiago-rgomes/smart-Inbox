import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise RuntimeError(
        "HF_TOKEN não encontrado. "
        "Configure no .env ou nas variáveis de ambiente."
    )

API_URL = "https://router.huggingface.co/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json",
}

MODEL = "meta-llama/Llama-3.1-8B-Instruct:novita"


def hf_chat(messages, temperature=0.2, max_tokens=300):
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    response = requests.post(
        API_URL,
        headers=HEADERS,
        json=payload,
        timeout=60
    )
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]


def classify_email_ai(email_text: str) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "Você é um classificador RÍGIDO de emails corporativos.\n\n"

                "REGRA PRINCIPAL:\n"
                "- SOMENTE classifique como PRODUTIVO se houver um PEDIDO CLARO,\n"
                "  AÇÃO EXPLÍCITA ou SOLICITAÇÃO DIRETA.\n\n"

                "PRODUTIVO (somente se existir pedido explícito):\n"
                "- Solicitação de suporte\n"
                "- Pergunta direta\n"
                "- Pedido de status\n"
                "- Relato de problema\n"
                "- Solicitação de documento ou informação\n\n"

                "IMPRODUTIVO (NÃO há pedido):\n"
                "- Agradecimentos\n"
                "- Felicitações\n"
                "- Confirmações simples (\"ok\", \"recebido\")\n"
                "- Elogios\n"
                "- Mensagens informativas SEM pedido\n\n"

                "REGRA CRÍTICA:\n"
                "- Se NÃO houver pedido explícito → IMPRODUTIVO\n"
                "- Se houver dúvida → IMPRODUTIVO\n\n"

                "RESPONDA APENAS COM UMA PALAVRA:\n"
                "Produtivo OU Improdutivo"
            )
        },
        {
            "role": "user",
            "content": email_text
        }
    ]

    try:
        result = hf_chat(messages, temperature=0)
        result = result.strip().lower()

        if result == "produtivo":
            return "Produtivo"

        if result == "improdutivo":
            return "Improdutivo"

        return "Indefinido"

    except Exception as error:
        print("Erro na classificação IA:", error)
        return "Indefinido"


def generate_response_ai(email_text: str, classification: str) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "Você é um assistente corporativo profissional. "
                "Responda de forma educada, clara e objetiva."
            )
        },
        {
            "role": "user",
            "content": (
                f"Classificação: {classification}\n\n"
                f"Email:\n{email_text}\n\n"
                "Resposta:"
            )
        }
    ]

    try:
        return hf_chat(
            messages,
            temperature=0.6,
            max_tokens=200
        )

    except Exception as error:
        print("Erro na geração IA:", error)
        return (
            "Olá,\n\n"
            "Recebemos sua mensagem e ela será analisada pela equipe.\n\n"
            "Atenciosamente."
        )