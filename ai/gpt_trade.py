import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def gpt_trade_decision(symbol, analysis_summary):
    prompt = f"""
    Symbol: {symbol}
    Support: {analysis_summary.get('support')}
    Resistance: {analysis_summary.get('resistance')}
    PCR: {analysis_summary.get('pcr')}
    IV CE: {analysis_summary.get('avg_iv_ce')}
    IV PE: {analysis_summary.get('avg_iv_pe')}
    Greeks: {analysis_summary.get('greeks')}

    Task: Based on the above option chain analysis,
    decide whether to BUY, SELL, or HOLD.
    Give confidence %, Entry, Target, StopLoss, and 1-line reason.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ GPT Error: {e}"
