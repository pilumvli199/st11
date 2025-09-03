import pandas as pd

def analyze_option_chain(option_chain: pd.DataFrame, symbol: str):
    """
    Analyze option chain for bullish/bearish bias based on CE vs PE.
    """
    try:
        if option_chain.empty:
            print(f"⚠️ Option chain empty for {symbol}")
            return None

        # ✅ Ensure strikePrice is numeric
        option_chain["strikePrice"] = pd.to_numeric(option_chain["strikePrice"], errors="coerce")
        option_chain = option_chain.dropna(subset=["strikePrice"])

        # Split CE & PE
        calls = option_chain[option_chain["option_type"] == "CE"]
        puts = option_chain[option_chain["option_type"] == "PE"]

        # Total OI
        total_ce_oi = calls["openInterest"].sum()
        total_pe_oi = puts["openInterest"].sum()

        # Total LTP
        avg_ce_ltp = calls["ltp"].mean()
        avg_pe_ltp = puts["ltp"].mean()

        print(f"\n📊 {symbol} Option Chain Analysis")
        print(f"Total CE OI: {total_ce_oi}, Avg CE LTP: {avg_ce_ltp}")
        print(f"Total PE OI: {total_pe_oi}, Avg PE LTP: {avg_pe_ltp}")

        # Simple bias logic
        if total_ce_oi > total_pe_oi:
            print(f"⚡ {symbol} Bias: Bearish (Calls > Puts)")
            return "Bearish"
        elif total_pe_oi > total_ce_oi:
            print(f"⚡ {symbol} Bias: Bullish (Puts > Calls)")
            return "Bullish"
        else:
            print(f"⚡ {symbol} Bias: Neutral")
            return "Neutral"

    except Exception as e:
        print(f"⚠️ Error analyzing {symbol}: {e}")
        return None
