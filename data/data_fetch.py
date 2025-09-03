import requests
import pandas as pd

ANGEL_INSTRUMENTS_URL = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"


def fetch_instruments():
    try:
        res = requests.get(ANGEL_INSTRUMENTS_URL, timeout=15)
        res.raise_for_status()
        data = res.json()
        return pd.DataFrame(data)
    except Exception as e:
        print(f"⚠️ Instruments fetch error: {e}")
        return pd.DataFrame()


def fetch_option_chain(obj, symbol, expiry=None):
    """
    Build option chain manually using instruments master + LTP API.
    If expiry is None, it will automatically pick the nearest expiry.
    """
    try:
        instruments = fetch_instruments()
        if instruments.empty:
            print("⚠️ Instruments not available")
            return pd.DataFrame()

        # Choose nearest expiry if not provided
        if expiry is None:
            expiries = instruments[instruments["name"] == symbol]["expiry"].unique()
            if len(expiries) == 0:
                print(f"⚠️ No expiries found for {symbol}")
                return pd.DataFrame()
            expiry = sorted(expiries)[0]  # pick earliest expiry

        # Filter options
        options = instruments[
            (instruments["name"] == symbol) &
            (instruments["expiry"] == expiry) &
            (instruments["instrumenttype"].isin(["OPTIDX", "OPTSTK"]))
        ].copy()

        if options.empty:
            print(f"⚠️ No options found for {symbol} {expiry}")
            return pd.DataFrame()

        chain_data = []
        for _, row in options.iterrows():
            try:
                ltp_resp = obj.ltpData("NSE", row["symbol"], row["token"])
                if "data" in ltp_resp:
                    ltp = ltp_resp["data"].get("ltp", None)
                else:
                    ltp = None

                chain_data.append({
                    "symbol": row["symbol"],
                    "strike": row["strike"],
                    "expiry": row["expiry"],
                    "option_type": row["optiontype"],
                    "ltp": ltp,
                    "token": row["token"]
                })
            except Exception as e:
                print(f"⚠️ LTP fetch failed for {row['symbol']}: {e}")

        return pd.DataFrame(chain_data)

    except Exception as e:
        print(f"⚠️ Option chain fetch error: {e}")
        return pd.DataFrame()

