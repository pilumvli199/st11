import time
from config import INDICES, FNO_STOCKS
from angel_bot.login.angel_login import angel_login
from angel_bot.data.data_fetch import fetch_instruments, fetch_option_chain
from angel_bot.analysis.option_chain_analysis import analyze_option_chain
from ai.gpt_trade import gpt_trade_decision
from angel_bot.alerts.telegram_bot import send_telegram_alert

def run_bot():
    obj, data = angel_login()
        if not obj or not data:
            print("❌ Login failed, exiting.")
            exit(1)
    
        client_id = data.get("data", {}).get("clientcode")
        jwt_token = data.get("data", {}).get("jwtToken")
        refresh_token = data.get("data", {}).get("refreshToken")
    if not data or not obj:
        print('❌ Login failed, exiting.')
        exit(1)
        client_id = data.get('data', {}).get('clientcode')
    jwt_token = data.get('data', {}).get('jwtToken')
    refresh_token = data.get('data', {}).get('refreshToken')
    if not jwt_token:
        print("❌ Login failed, skipping cycle")
        return

    df = fetch_instruments()
    symbols = INDICES + FNO_STOCKS

    for symbol in symbols:
        try:
            expiry = df[df["symbol"] == symbol]["expiry"].min()
            chain = fetch_option_chain(obj.api_key, client_id, jwt_token, symbol, expiry)

            if chain.empty:
                print(f"⚠️ No option chain for {symbol}")
                continue

            summary = analyze_option_chain(chain)
            print(f"\n📊 {symbol} Analysis:", summary)

            gpt_signal = gpt_trade_decision(symbol, summary)
            print(f"⚡ {symbol} Signal:", gpt_signal)

            # ✅ Send Telegram Alert
            alert_msg = f"⚡ {symbol} Trade Signal\n{gpt_signal}"
            send_telegram_alert(alert_msg)

        except Exception as e:
            print(f"⚠️ Error processing {symbol}: {e}")

if __name__ == "__main__":
    while True:
        run_bot()
        time.sleep(300)