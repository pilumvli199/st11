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


def fetch_option_chain(obj, symbol):
    """
    Build option chain manually using instruments master + LTP API.
    Auto-picks nearest expiry for given symbol (e.g., NIFTY, BANKNIFTY).
    """
    try:
        instruments = fetch_instruments()
        if instruments.empty:
            print("⚠️ Instruments not available")
            return pd.DataFrame()

        # Filter only option contracts for given symbol
        options = instruments[
            (instruments["name"].str.upper() == symbol.upper()) &
            (instruments["instrumenttype"].isin(["OPTIDX", "OPTSTK"]))
        ].copy()

        if options.empty:
            print(f"⚠️ No option contracts found for {symbol}")
            return pd.DataFrame()

        # Pick nearest expiry
        expiries = sorted(options["expiry"].unique())
        if not expiries:
            print(f"⚠️ No expiries found for {symbol}")
            return pd.DataFrame()
        expiry = expiries[0]

        options = options[options["expiry"] == expiry]

        chain_data = []
        for _, row in options.iterrows():
            try:
                ltp_resp = obj.ltpData("NSE", row["symbol"], row["token"])
                if "data" in ltp_resp:
                    ltp = ltp_resp["data"].get("ltp", None)
                else:
                    ltp = None

                chain_data.append({
                    "tradingsymbol": row["symbol"],
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
