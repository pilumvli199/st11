import requests
import pandas as pd

ANGEL_INSTRUMENTS_URL = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"

def fetch_instruments():
    try:
        res = requests.get(ANGEL_INSTRUMENTS_URL, timeout=15)
        res.raise_for_status()
        return pd.DataFrame(res.json())
    except Exception as e:
        print(f"⚠️ Error fetching instruments: {e}")
        return pd.DataFrame()
