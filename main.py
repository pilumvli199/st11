from login.angel_login import angel_login
from alerts.telegram_bot import send_telegram_alert
import schedule
import time


def run_bot():
    obj, data = angel_login()
    if not obj or not data:
        print("❌ Login failed, exiting.")
        return

    # Indices watchlist
    watchlist = ["NIFTY", "SENSEX"]

    for symbol in watchlist:
        try:
            # NOTE: Token must match instruments master
            token_map = {
                "NIFTY": "26000",    # NIFTY spot token
                "SENSEX": "1"        # SENSEX token (verify from instruments master)
            }
            token = token_map[symbol]

            # Fetch LTP
            ltp_resp = obj.ltpData("NSE", symbol, token)
            ltp = ltp_resp.get("data", {}).get("ltp")

            msg = f"📊 {symbol} LTP: {ltp}"
            print(msg)
            send_telegram_alert(msg)

        except Exception as e:
            print(f"⚠️ Error processing {symbol}: {e}")


if __name__ == "__main__":
    run_bot()
    schedule.every(5).minutes.do(run_bot)

    while True:
        schedule.run_pending()
        time.sleep(1)

