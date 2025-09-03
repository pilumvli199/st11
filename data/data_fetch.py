import requests
import pandas as pd

ANGEL_OPTIONCHAIN_URL = "https://apiconnect.angelbroking.com/rest/secure/angelbroking/market/v1/optionchain"

def fetch_option_chain(api_key, client_id, jwt_token, symbol, expiry):
    headers = {
        "X-PrivateKey": api_key,
        "X-ClientLocalIP": "127.0.0.1",
        "X-ClientPublicIP": "127.0.0.1",
        "X-MACAddress": "00:00:00:00:00:00",
        "X-UserType": "USER",
        "X-SourceID": "WEB",
        "X-ClientID": client_id,
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }

    payload = {"symbol": symbol, "expirydate": expiry}

    try:
        res = requests.post(ANGEL_OPTIONCHAIN_URL, headers=headers, json=payload, timeout=15)
        res.raise_for_status()
        data = res.json()

        ce = data.get("data", {}).get("CE", [])
        pe = data.get("data", {}).get("PE", [])

        ce_df = pd.DataFrame(ce)
        pe_df = pd.DataFrame(pe)

        ce_df["option_type"] = "CE"
        pe_df["option_type"] = "PE"

        return pd.concat([ce_df, pe_df], ignore_index=True)
    except Exception as e:
        print(f"⚠️ Option chain fetch error: {e}")
        return pd.DataFrame()



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
