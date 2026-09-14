# Interview Answer Analyzer

Streamlit app that scores a “Why should we hire you?” answer with Azure AI Language (sentiment + key phrases).

## Security

A Cognitive Services subscription key was previously committed in source. **That key must be rotated/revoked in Azure immediately** — removing it from git does not make the old value private. See [SECURITY.md](SECURITY.md).

## Setup

1. Create a Python virtual environment and install dependencies:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Copy the env template and fill in **your** Azure Language resource values (placeholders only — never commit real keys):

   ```bash
   cp .env.example .env
   ```

   Required variables:

   | Variable | Description |
   | --- | --- |
   | `AZURE_COGNITIVE_KEY` or `AZURE_LANGUAGE_KEY` | Subscription key from Azure Portal → your resource → Keys and Endpoint |
   | `AZURE_COGNITIVE_ENDPOINT` | Endpoint URL, e.g. `https://YOUR-RESOURCE.cognitiveservices.azure.com/` |

3. Run the app:

   ```bash
   streamlit run sentiment_test.py
   ```

`.env` is gitignored. Do not hardcode keys in source, PRs, or screenshots.
