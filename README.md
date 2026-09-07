# Agent Hello World

The smallest working version of this pattern:

**iPhone ChatGPT → GitHub repository → GitHub Actions → public API → GitHub notification**

This example checks the current PONS price using DexScreener. It runs every six hours and can also be started manually from an iPhone. When the price is above the configured threshold, it opens one GitHub issue; GitHub then sends the normal issue notification.

## Try it from your iPhone

1. Open this repository in the GitHub app or Safari.
2. Open **Actions** → **PONS price monitor**.
3. Tap **Run workflow**.
4. Leave **Force a test alert** set to `true`, then tap **Run workflow**.
5. Open **Issues** to see the test alert.

No secrets, packages, servers, or Azure subscription are required.

## Configure the real alert

The default threshold is **$1.00**. To change it:

1. Open **Settings** → **Secrets and variables** → **Actions** → **Variables**.
2. Add a repository variable named `PONS_ALERT_ABOVE_USD`.
3. Set it to the price that should trigger an issue, such as `0.75`.

The scheduled run uses that threshold. It will not create duplicates while an open issue titled **PONS price alert** already exists. Close the issue when you want the monitor to be able to alert again.

## What each file does

- `agent.py`: calls DexScreener for the default PONS pair and decides whether the threshold was crossed.
- `.github/workflows/bitcoin-monitor.yml`: supplies the free runtime and creates the GitHub issue.
- `README.md`: iPhone setup and testing instructions.

## Next step: Azure

Once this loop works, the same `agent.py` can move to Azure Functions or Azure Container Apps. GitHub Actions can deploy it, and the GitHub issue can later be replaced or supplemented with email, SMS, Teams, Slack, or a ChatGPT automation.