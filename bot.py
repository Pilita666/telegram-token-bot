import os
import time
import requests
from telegram import Bot

# Configurações via variáveis de ambiente (no Render: Settings > Environment)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
INTERVALO = 1800  # 30 minutos (em segundos)

bot = Bot(token=BOT_TOKEN)

# Alvos para monitorar
TOKEN_NAME = "TICS"
API_URL = "https://api.dexscreener.com/latest/dex/pairs"  # Exemplo com Dexscreener

def buscar_dados_token():
    try:
        response = requests.get(f"{API_URL}?q={TOKEN_NAME}")
        data = response.json()

        if 'pairs' not in data or len(data['pairs']) == 0:
            return "❗Token não encontrado."

        pair = data['pairs'][0]  # Primeiro resultado relevante
        preco = pair.get("priceUsd", "N/A")
        volume = pair.get("volume", "N/A")
        liquidez = pair.get("liquidity", {}).get("usd", "N/A")
        exchange = pair.get("dexId", "N/A")
        token_url = pair.get("url", "N/A")

        msg = (
            f"📊 *Monitoramento do Token {TOKEN_NAME}*\n\n"
            f"💰 *Preço:* ${preco}\n"
            f"📈 *Volume 24h:* ${volume}\n"
            f"💧 *Liquidez:* ${liquidez}\n"
            f"🏛️ *Exchange:* {exchange}\n"
            f"🔗 [Ver no DexScreener]({token_url})"
        )
        return msg

    except Exception as e:
        return f"Erro ao buscar dados: {str(e)}"

def enviar_alerta():
    texto = buscar_dados_token()
    bot.send_message(chat_id=CHAT_ID, text=texto, parse_mode='Markdown')

def main():
    while True:
        enviar_alerta()
        time.sleep(INTERVALO)

if __name__ == "__main__":
    main()
