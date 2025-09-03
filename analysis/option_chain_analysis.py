import pandas as pd

def analyze_option_chain(option_chain: pd.DataFrame, symbol: str):
    """
    Analyze option chain for bullish/bearish bias and return clean dict for Telegram alerts.
    """
    try:
        if option_chain.empty:
            print(f"⚠️ Option chain empty for {symbol}")
            return None

        # ✅ Ensure numeric
        option_chain["strikePrice"] = pd.to_numeric(option_chain["strikePrice"], errors="coerce")
        option_chain = option_chain.dropna(subset=["strikePrice"])

        calls = option_chain[option_chain["option_type"] == "CE"]
        puts = option_chain[option_chain["option_type"] == "PE"]

        if calls.empty or puts.empty:
            print(f"⚠️ Not enough CE/PE data for {symbol}")
            return None

        # Basic support = lowest strike (PE side), resistance = highest strike (CE side)
        support = float(puts["strikePrice"].min())
        resistance = float(calls["strikePrice"].max())

        # Total OI
        total_ce_oi = int(calls["openInterest"].sum())
        total_pe_oi = int(puts["openInterest"].sum())

        # Put/Call Ratio
        pcr = round(total_pe_oi / total_ce_oi, 2) if total_ce_oi > 0 else None

        signal = {
            "symbol": symbol,
            "support": int(support),
            "resistance": int(resistance),
            "total_CE_OI": total_ce_oi,
            "total_PE_OI": total_pe_oi,
            "PCR": pcr,
        }

        print(f"📊 {symbol} Option Chain Signal: {signal}")
        return signal

    except Exception as e:
        print(f"⚠️ Error analyzing {symbol}: {e}")
        return None
