import streamlit as st
import requests

# Use your actual key and endpoint
api_key = "REDACTED"
endpoint = "https://sentimentdemo01.cognitiveservices.azure.com/"

# Azure API endpoints
sentiment_url = endpoint + "/text/analytics/v3.0/sentiment"
keyphrase_url = endpoint + "/text/analytics/v3.0/keyPhrases"

st.set_page_config(page_title="Interview Analyzer", page_icon="💼")
st.title("💼 Interview Answer Analyzer")
st.write("Paste your answer to: **Why should we hire you?**")

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

    # Key phrase extraction
    kp_response = requests.post(keyphrase_url, headers=headers, json=documents)
    key_phrases = kp_response.json()["documents"][0]["keyPhrases"]

    # Show detailed output
    st.subheader("🔎 Azure AI Analysis")
    st.markdown(f"**Sentiment**: `{sentiment.upper()}`")
    st.write("**Confidence Scores:**", confidence)
    st.write("**Key Phrases Detected:**", ", ".join(key_phrases))

    # Interpretation logic
    score = confidence["positive"] - confidence["negative"]
    st.subheader("🧠 Verdict")

    if score > 0.6:
        st.success("✅ This is a strong and confident answer! Great job!")
    elif score > 0.3:
        st.warning("⚠️ You're on the right track, but consider making it more confident or specific.")
    else:
        st.error("❌ This comes across as insecure or too negative. Try rephrasing with stronger language.")