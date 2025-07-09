import os
import asyncio
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
USER_CHAT_ID = os.getenv("CHAT_ID")  # Chat ID do Telegram onde os alertas serão enviados

# IDs dos tokens na CoinGecko
TOKENS = {
    "TICS": "tics",
    "BDAG": "based-dag",
    "DTX": "dt-x",
    "RCOF": "rco-finance"
}

# Armazena os preços e volumes anteriores
previous_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot $TICS ativo! Monitorando tokens: $TICS, $BDAG, $DTX, $RCOF.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📡 Monitoramento a cada 30 minutos. Tokens: " + ", ".join(TOKENS.keys()))

async def fetch_token_data(token_id):
    url = f"https://api.coingecko.com/api/v3/coins/{token_id}"
    try:
        res = requests.get(url)
        data = res.json()
        price = data['market_data']['current_price']['usd']
        volume = data['market_data']['total_volume']['usd']
        return price, volume
    except Exception as e:
        print(f"Erro ao buscar dados para {token_id}: {e}")
        return None, None

async def check_prices(app):
    global previous_data
    while True:
        for symbol, token_id in TOKENS.items():
            price, volume = await fetch_token_data(token_id)
            if price is None:
                continue

            prev_price, prev_vol = previous_data.get(symbol, (price, volume))
            price_change = (price - prev_price) / prev_price * 100
            vol_change = (volume - prev_vol) / prev_vol * 100

            alert = ""
            if abs(price_change) >= 3:
                alert += f"💰 {symbol} preço mudou {price_change:.2f}% (${prev_price:.4f} → ${price:.4f})\n"
            if abs(vol_change) >= 10:
                alert += f"📊 {symbol} volume mudou {vol_change:.1f}% (${prev_vol:,.0f} → ${volume:,.0f})\n"
            if volume < 1000:
                alert += f"⚠️ Baixa liquidez detectada em {symbol} (volume < $1k)\n"

            if alert:
                try:
                    await app.bot.send_message(chat_id=USER_CHAT_ID, text=alert)
                except Exception as e:
                    print(f"Erro ao enviar alerta: {e}")

            previous_data[symbol] = (price, volume)

        await asyncio.sleep(1800)  # Espera 30 minutos

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))

    # Inicia o loop de monitoramento
    app.job_queue.run_once(lambda ctx: asyncio.create_task(check_prices(app)), 1)
    app.run_polling()

if __name__ == '__main__':
    main()import os
import asyncio
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
USER_CHAT_ID = os.getenv("CHAT_ID")  # Chat ID do Telegram onde os alertas serão enviados

# IDs dos tokens na CoinGecko
TOKENS = {
    "TICS": "tics",
    "BDAG": "based-dag",
    "DTX": "dt-x",
    "RCOF": "rco-finance"
}

# Armazena os preços e volumes anteriores
previous_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot $TICS ativo! Monitorando tokens: $TICS, $BDAG, $DTX, $RCOF.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📡 Monitoramento a cada 30 minutos. Tokens: " + ", ".join(TOKENS.keys()))

async def fetch_token_data(token_id):
    url = f"https://api.coingecko.com/api/v3/coins/{token_id}"
    try:
        res = requests.get(url)
        data = res.json()
        price = data['market_data']['current_price']['usd']
        volume = data['market_data']['total_volume']['usd']
        return price, volume
    except Exception as e:
        print(f"Erro ao buscar dados para {token_id}: {e}")
        return None, None

async def check_prices(app):
    global previous_data
    while True:
        for symbol, token_id in TOKENS.items():
            price, volume = await fetch_token_data(token_id)
            if price is None:
                continue

            prev_price, prev_vol = previous_data.get(symbol, (price, volume))
            price_change = (price - prev_price) / prev_price * 100
            vol_change = (volume - prev_vol) / prev_vol * 100

            alert = ""
            if abs(price_change) >= 3:
                alert += f"💰 {symbol} preço mudou {price_change:.2f}% (${prev_price:.4f} → ${price:.4f})\n"
            if abs(vol_change) >= 10:
                alert += f"📊 {symbol} volume mudou {vol_change:.1f}% (${prev_vol:,.0f} → ${volume:,.0f})\n"
            if volume < 1000:
                alert += f"⚠️ Baixa liquidez detectada em {symbol} (volume < $1k)\n"

            if alert:
                try:
                    await app.bot.send_message(chat_id=USER_CHAT_ID, text=alert)
                except Exception as e:
                    print(f"Erro ao enviar alerta: {e}")

            previous_data[symbol] = (price, volume)

        await asyncio.sleep(1800)  # Espera 30 minutos

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))

    # Inicia o loop de monitoramento
    app.job_queue.run_once(lambda ctx: asyncio.create_task(check_prices(app)), 1)
    app.run_polling()

if __name__ == '__main__':
    main()
