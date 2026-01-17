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

SIGNATURE_NAME = "Equipe de Suporte"


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


# CLASSIFICAÇÃO DE EMAIL (FEW-SHOT)

def classify_email_ai(email_text: str) -> str:
    """
    Classifica email como:
    - Produtivo
    - Improdutivo

    Usa FEW-SHOT para evitar viés de sempre classificar como Produtivo.
    """

    messages = [
        {
            "role": "system",
            "content": (
                "Você é um CLASSIFICADOR RÍGIDO de emails corporativos.\n\n"

                "REGRA PRINCIPAL:\n"
                "- SOMENTE classifique como PRODUTIVO se houver um PEDIDO CLARO\n"
                "  ou AÇÃO EXPLÍCITA solicitada.\n\n"

                "SE NÃO HOUVER PEDIDO → IMPRODUTIVO\n"
                "SE HOUVER DÚVIDA → IMPRODUTIVO\n\n"

                "RESPONDA APENAS COM UMA PALAVRA:\n"
                "Produtivo OU Improdutivo"
            )
        },

        {
            "role": "user",
            "content": "Obrigado pelo atendimento, ficou tudo certo agora."
        },
        {
            "role": "assistant",
            "content": "Improdutivo"
        },
        {
            "role": "user",
            "content": "Bom dia, segue o relatório conforme combinado."
        },
        {
            "role": "assistant",
            "content": "Improdutivo"
        },
        {
            "role": "user",
            "content": "Poderiam verificar o erro que está ocorrendo no sistema?"
        },
        {
            "role": "assistant",
            "content": "Produtivo"
        },
        {
            "role": "user",
            "content": "Preciso de ajuda para redefinir minha senha."
        },
        {
            "role": "assistant",
            "content": "Produtivo"
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
    """
    Gera resposta profissional com template fixo.
    A IA NÃO pode inventar nomes ou formatos.
    """

    messages = [
        {
            "role": "system",
            "content": (
                "Você é um assistente corporativo profissional.\n\n"

                "REGRAS ABSOLUTAS:\n"
                "- NÃO invente nomes de pessoas\n"
                "- NÃO assine com nomes próprios\n"
                "- NÃO altere o formato da assinatura\n"
                "- NÃO mencione IA\n"
                "- NÃO use emojis\n\n"

                "FORMATO OBRIGATÓRIO (SIGA EXATAMENTE):\n"
                "Olá,\n\n"
                "[resposta clara, curta e objetiva]\n\n"
                "Atenciosamente,\n"
                f"{SIGNATURE_NAME}"
            )
        },
        {
            "role": "user",
            "content": (
                f"Classificação do email: {classification}\n\n"
                f"Email recebido:\n{email_text}"
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
            f"Atenciosamente,\n{SIGNATURE_NAME}"
        )