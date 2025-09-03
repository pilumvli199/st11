def analyze_option_chain(option_chain_df):
    if option_chain_df.empty:
        return {"error": "No option chain data"}

    ce = option_chain_df[option_chain_df["option_type"] == "CE"]
    pe = option_chain_df[option_chain_df["option_type"] == "PE"]

    ce_resistance = ce.loc[ce["openInterest"].idxmax()] if not ce.empty else None
    pe_support = pe.loc[pe["openInterest"].idxmax()] if not pe.empty else None

    total_ce_oi = ce["openInterest"].sum() if not ce.empty else 0
    total_pe_oi = pe["openInterest"].sum() if not pe.empty else 0
    pcr = round(total_pe_oi / total_ce_oi, 2) if total_ce_oi > 0 else None

    avg_iv_ce = round(ce["impliedVolatility"].mean(), 2) if "impliedVolatility" in ce else None
    avg_iv_pe = round(pe["impliedVolatility"].mean(), 2) if "impliedVolatility" in pe else None

    atm_strike = option_chain_df.iloc[(option_chain_df["strikePrice"] - option_chain_df["strikePrice"].median()).abs().argsort()[:1]]
    greeks = {}
    if not atm_strike.empty:
        row = atm_strike.iloc[0]
        greeks = {
            "delta": row.get("delta", None),
            "gamma": row.get("gamma", None),
            "theta": row.get("theta", None),
            "vega": row.get("vega", None),
        }

    return {
        "support": pe_support["strikePrice"] if pe_support is not None else None,
        "resistance": ce_resistance["strikePrice"] if ce_resistance is not None else None,
        "pcr": pcr,
        "avg_iv_ce": avg_iv_ce,
        "avg_iv_pe": avg_iv_pe,
        "greeks": greeks,
    }
