from angel_bot.login.angel_login import angel_login
from angel_bot.data.data_fetch import fetch_instruments, fetch_option_chain
from angel_bot.analysis.option_chain_analysis import analyze_option_chain
from angel_bot.alerts.telegram_bot import send_telegram_alert
import schedule
import time
import os


def run_bot():
    obj, data = angel_login()
    if not obj or not data:
        print("❌ Login failed, exiting.")
        return

    # Extract tokens and client id
    client_id = data.get("data", {}).get("clientcode")
    jwt_token = data.get("data", {}).get("jwtToken")
    refresh_token = data.get("data", {}).get("refreshToken")

    api_key = os.getenv("ANGEL_API_KEY")

    # Fetch instruments
    instruments_df = fetch_instruments()
    if instruments_df.empty:
        print("⚠️ Instruments fetch failed")
        return

    # Example watchlist (NIFTY50 subset)
    watchlist = instruments_df[instruments_df["symbol"].isin([
        "TITAN", "ASIANPAINT", "JSWSTEEL", "NTPC", "POWERGRID"
    ])]

    for symbol in watchlist["symbol"].unique():
        try:
            option_chain = fetch_option_chain(obj, symbol, "26-SEP-2024")
            if option_chain.empty:
                continue

            signals = analyze_option_chain(option_chain)
            if signals:
                send_telegram_alert(f"📊 {symbol}: {signals}")

        except Exception as e:
            print(f"⚠️ Error processing {symbol}: {e}")


if __name__ == "__main__":
    run_bot()
    schedule.every(5).minutes.do(run_bot)

    while True:
        schedule.run_pending()
        time.sleep(1)

      
