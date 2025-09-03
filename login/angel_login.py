from SmartApi.smartConnect import SmartConnect
import pyotp
import os

def angel_login():
    api_key = os.getenv("ANGEL_API_KEY")
    client_id = os.getenv("ANGEL_CLIENT_ID")
    password_or_pin = os.getenv("ANGEL_PIN_OR_PWD")
    totp_secret = os.getenv("ANGEL_TOTP_SECRET")

    if not api_key or not client_id or not password_or_pin or not totp_secret:
        print("⚠️ Missing login environment variables.")
        return None, None

    smartApi = SmartConnect(api_key=api_key)
    totp = pyotp.TOTP(totp_secret).now()

    try:
        data = smartApi.generateSession(client_id, password_or_pin, totp)
        print("✅ Login success")
        return smartApi, data
    except Exception as e:
        print(f"⚠️ Login Error: {e}")
        return None, None
