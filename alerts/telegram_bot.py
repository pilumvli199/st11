import requests
import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram_alert(message: str):
    """
    Send plain text alert to Telegram
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ Telegram credentials missing in .env")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        if r.status_code != 200:
            print(f"⚠️ Telegram Error: {r.text}")
        else:
            print("📩 Telegram Alert Sent")
    except Exception as e:
        print(f"⚠️ Telegram Exception: {e}")


def send_option_chain_signal(signal: dict):
    """
    Format option chain analysis result into clean Telegram message
    """
    if not signal:
        return

    msg = (
        f"📊 *{signal['symbol']} Option Chain Signal*\n\n"
        f"🟢 Support: `{signal['support']}`\n"
        f"🔴 Resistance: `{signal['resistance']}`\n"
        f"📈 Total CE OI: `{signal['total_CE_OI']}`\n"
        f"📉 Total PE OI: `{signal['total_PE_OI']}`\n"
        f"⚖️ PCR: `{signal['PCR']}`\n"
    )

    send_telegram_alert(msg)
