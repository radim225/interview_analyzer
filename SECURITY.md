# Security

## Action required: rotate the leaked Azure key

A Microsoft Azure Cognitive Services / Language **subscription key** was committed in `sentiment_test.py` and pushed to this public repository. The hostname `sentimentdemo01.cognitiveservices.azure.com` identifies the resource.

**Revoke and rotate that key immediately** (do not keep using it):

1. Open [Azure Portal](https://portal.azure.com) → the Language / Cognitive Services resource (`sentimentdemo01` or whatever you now use).
2. Go to **Keys and Endpoint**.
3. **Regenerate Key 1 and Key 2** (or delete the resource if it was only a demo).
4. Put the **new** key only in a local `.env` file or your host’s secret store — never in git.

Removing the key from the current tree does **not** unsay it. Public clones, forks, crawlers, and GitHub caches may still have the old value. Rotation is mandatory even after a history rewrite.

## History purge (optional, owner-only)

This repository is small (single owner, no forks at the time of the fix), so rewriting history is *possible* but still disruptive: anyone with a clone must re-clone, and GitHub may retain unreachable objects until support is involved.

A rewritten branch that replaces the leaked value in all commits is published as `cursor/purge-azure-key-history-fc42` for Radim to inspect. **Do not merge that branch** into `main` through a normal PR — a merge keeps the old commits. To replace `main` after rotating the key:

```bash
git fetch origin
git checkout cursor/purge-azure-key-history-fc42
git push --force-with-lease origin cursor/purge-azure-key-history-fc42:main
```

After a force-push, consider asking GitHub Support to purge cached data, and confirm no forks/mirrors remain.

If force-pushing `main` is not acceptable, keep this (additive) fix on `main` and still **rotate the key**.

## Local secrets

- Copy `.env.example` → `.env` and fill placeholders.
- `.env` and `.streamlit/secrets.toml` are gitignored.
- Prefer environment variables `AZURE_COGNITIVE_KEY` / `AZURE_LANGUAGE_KEY` and `AZURE_COGNITIVE_ENDPOINT`.
