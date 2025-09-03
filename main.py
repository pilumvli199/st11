from login.angel_login import angel_login
from data.data_fetch import fetch_instruments, fetch_option_chain
from analysis.option_chain_analysis import analyze_option_chain
from alerts.telegram_bot import send_telegram_alert
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

    # Example watchlist (subset of NIFTY50)
    watchlist = instruments_df[instruments_df["symbol"].isin([
        "TITAN", "ASIANPAINT", "JSWSTEEL", "NTPC", "POWERGRID"
    ])]

   # Watchlist for indices
watchlist = ["NIFTY", "SENSEX"]

for symbol in watchlist:
    try:
        # Fetch LTP data directly
        ltp_resp = obj.ltpData("NSE", symbol, "26000")  # token बद्दल instruments master मध्ये बघावे लागेल
        print(f"📊 {symbol} LTP: {ltp_resp}")
        send_telegram_alert(f"📊 {symbol}: {ltp_resp}")

    except Exception as e:
        print(f"⚠️ Error processing {symbol}: {e}")



if __name__ == "__main__":
    # Run once at start
    run_bot()

    # Schedule every 5 minutes
    schedule.every(5).minutes.do(run_bot)

    while True:
        schedule.run_pending()
        time.sleep(1)

