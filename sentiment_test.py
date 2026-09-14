import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

api_key = (os.getenv("AZURE_COGNITIVE_KEY") or os.getenv("AZURE_LANGUAGE_KEY") or "").strip()
endpoint = (os.getenv("AZURE_COGNITIVE_ENDPOINT") or "").strip().rstrip("/")
sentiment_url = f"{endpoint}/text/analytics/v3.0/sentiment"
keyphrase_url = f"{endpoint}/text/analytics/v3.0/keyPhrases"

st.set_page_config(page_title="Interview Answer Analyzer", page_icon="💼")
st.title("💼 Interview Answer Analyzer")
st.write("Paste your answer to: **Why should we hire you?**")

if not api_key or not endpoint:
    missing = []
    if not api_key:
        missing.append("`AZURE_COGNITIVE_KEY` or `AZURE_LANGUAGE_KEY`")
    if not endpoint:
        missing.append("`AZURE_COGNITIVE_ENDPOINT`")
    st.error("Missing required environment variable(s): " + ", ".join(missing))
    st.info("Copy `.env.example` to `.env`, add your Azure Language resource values, then restart the app. See the README.")
    st.stop()

user_input = st.text_area("✍️ Your answer", "")

if st.button("🔍 Analyze"):
    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json"
    }
    documents = {"documents": [{"id": "1", "language": "en", "text": user_input}]}

    # Sentiment analysis
    response = requests.post(sentiment_url, headers=headers, json=documents)
    result = response.json()
    sentiment = result["documents"][0]["sentiment"]
    confidence = result["documents"][0]["confidenceScores"]
    score_pos = confidence["positive"]
    score_neu = confidence["neutral"]
    score_neg = confidence["negative"]

    # Key phrase extraction
    kp_response = requests.post(keyphrase_url, headers=headers, json=documents)
    key_phrases = kp_response.json()["documents"][0]["keyPhrases"]

    # Red flag phrase detection
    red_flags = ["not the best", "not qualified", "no experience", "don't have", "i'm unsure", "not confident"]
    red_flag_hits = [phrase for phrase in red_flags if phrase in user_input.lower()]

    st.subheader("🔎 Azure AI Analysis")
    st.markdown(f"**Sentiment**: `{sentiment.upper()}`")

    st.subheader("📊 Confidence Breakdown")
    st.markdown(f"- **Positive tone:** {score_pos:.2%} confidence")
    st.markdown(f"- **Neutral elements:** {score_neu:.2%}")
    st.markdown(f"- **Negative tone:** {score_neg:.2%}")

    st.write("**Key Phrases Detected:**", ", ".join(key_phrases))

    st.caption("⚠️ Note: Azure may misinterpret phrases like 'not the best candidate' as positive. Context is limited.")

    st.subheader("🧠 Verdict")
    if red_flag_hits:
        st.error("❌ This answer includes self-doubt or negative phrases: " + ", ".join(red_flag_hits) + ". Try to sound more confident.")
    elif score_pos > 0.65 and score_neg < 0.2:
        st.success("✅ This is a strong and confident answer! Great job!")
    elif score_neg > 0.3:
        st.error("❌ This sounds too negative or insecure. Try rephrasing with more positive language.")
    elif score_pos > 0.5 and score_neu < 0.3:
        st.success("✅ Confident tone detected. Could be even stronger with clearer examples.")
    else:
        st.warning("⚠️ You're on the right track, but consider making it more confident or specific.")
