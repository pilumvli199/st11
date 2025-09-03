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
    Auto-picks nearest upcoming expiry for given symbol (e.g., NIFTY, BANKNIFTY).
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

        # Pick nearest valid expiry (>= today)
        try:
            expiry_dates = pd.to_datetime(options["expiry"], errors="coerce").dropna().unique()
            expiry_dates = sorted([e for e in expiry_dates if e >= pd.Timestamp.today()])
            if not expiry_dates:
                print(f"⚠️ No valid upcoming expiries for {symbol}")
                return pd.DataFrame()
            nearest_expiry = expiry_dates[0].strftime("%Y-%m-%d")
        except Exception as e:
            print(f"⚠️ Expiry parsing error: {e}")
            return pd.DataFrame()

        options = options[options["expiry"] == nearest_expiry]

        chain_data = []
        for _, row in options.iterrows():
            try:
                # Handle tradingsymbol / symbol mismatch
                if "tradingsymbol" in row and pd.notna(row["tradingsymbol"]):
                    tsymbol = row["tradingsymbol"]
                else:
                    tsymbol = row["symbol"]

                # ✅ Use NFO for options contracts
                ltp_resp = obj.ltpData("NFO", tsymbol, row["token"])
                if "data" in ltp_resp and ltp_resp["data"] is not None:
                    ltp = ltp_resp["data"].get("ltp", None)
                else:
                    ltp = None

                chain_data.append({
                    "tradingsymbol": tsymbol,
                    "strike": row["strike"],
                    "expiry": row["expiry"],
                    "option_type": row["optiontype"],
                    "ltp": ltp,
                    "token": row["token"]
                })
            except Exception as e:
                print(f"⚠️ LTP fetch failed for {row.get('symbol', 'UNKNOWN')}: {e}")

        return pd.DataFrame(chain_data)

    except Exception as e:
        print(f"⚠️ Option chain fetch error: {e}")
        return pd.DataFrame()

    
