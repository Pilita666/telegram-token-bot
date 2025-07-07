import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from pycoingecko import CoinGeckoAPI
import datetime

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID"))
CHECK_INTERVAL = 3600

cg = CoinGeckoAPI()
TOKENS = {
    'TICS': 'qubetics',
    'BDAG': 'blockdag',
    'DTX': 'databroker-dao'
}
last_prices = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot ativo! Monitorando: $TICS, BDAG e DTX a cada 1 hora.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "\n".join([f"{k}: ${v:.5f}" for k, v in last_prices.items()])
    await update.message.reply_text(f"📊 Preços atuais\n🕒 {now}\n\n{status or 'Aguardando dados...'}")

async def check_prices(app):
    global last_prices
    try:
        data = cg.get_price(ids=",".join(TOKENS.values()), vs_currencies='usd', include_24hr_change='true')
        alerts = []
        for symbol, cg_id in TOKENS.items():
            if cg_id not in data:
                continue
            new = data[cg_id]['usd']
            change_24h = data[cg_id]['usd_24h_change']
            old = last_prices.get(symbol, new)
            diff = ((new - old) / old) * 100 if old else 0
            last_prices[symbol] = new

            if abs(diff) >= 5:
                arrow = "🔺" if diff > 0 else "🔻"
                alerts.append(f"{arrow} ${symbol}: {diff:.2f}% em 1h (${old:.5f} → ${new:.5f})")
            if abs(change_24h) >= 10:
                emoji = "📈" if change_24h > 0 else "📉"
                alerts.append(f"{emoji} ${symbol}: {change_24h:.2f}% nas 24h (agora ${new:.5f})")

        if alerts:
            msg = "🚨 *ALERTA DE VARIAÇÃO:*\n\n" + "\n".join(alerts)
            await app.bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode="Markdown")
    except Exception as e:
        print("Erro ao consultar preços:", e)

def main():
    app = ApplicationBuilder().token(TOKEN).post_init(lambda app: app.job_queue.start()).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.job_queue.run_repeating(lambda *_: asyncio.create_task(check_prices(app)), interval=CHECK_INTERVAL, first=5)
    print("🤖 Bot rodando...")
    app.run_polling()

if __name__ == '__main__':
    main()
