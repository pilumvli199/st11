from login.angel_login import angel_login
from data.data_fetch import fetch_instruments, fetch_option_chain
from analysis.option_chain_analysis import analyze_option_chain
from alerts.telegram_bot import send_telegram_alert
import schedule
import time


def run_bot():
    obj, data = angel_login()
    if not obj or not data:
        print("❌ Login failed, exiting.")
        return

    # Watchlist indices for option chain scanning
    watchlist = ["NIFTY", "BANKNIFTY"]

    for symbol in watchlist:
        try:
            # ✅ Expiry auto-detect होईल (data_fetch.py मध्ये handle आहे)
            option_chain = fetch_option_chain(obj, symbol)
            if option_chain.empty:
                print(f"⚠️ Option chain empty for {symbol}")
                continue

            # Analyze option chain
            signals = analyze_option_chain(option_chain)
            if signals:
                msg = f"📊 {symbol} Option Chain Signal: {signals}"
                print(msg)
                send_telegram_alert(msg)

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


