# Agent Hello World

A small GitHub Actions automation repo that uses Python scripts plus GitHub Issues as an audit trail and notification layer.

Current flows in this repository:

- **Bitcoin price alert** using CoinGecko
- **Paper-only crypto execution** from committed research signals
- **Paper position monitoring** against live DexScreener data

The pattern is:

**trigger → GitHub Actions → Python decision logic → GitHub issue or comment**

No wallet access, transaction signing, exchange credentials, or extra infrastructure is required.

## Repository layout

- `/home/runner/work/agent-hello-world/agent-hello-world/agent.py`: fetches the current Bitcoin price and decides whether an alert should fire
- `/home/runner/work/agent-hello-world/agent-hello-world/paper_executor.py`: converts a committed signal into a deterministic paper execution record
- `/home/runner/work/agent-hello-world/agent-hello-world/position_monitor.py`: evaluates a saved paper position against live pair data
- `/home/runner/work/agent-hello-world/agent-hello-world/.github/workflows/bitcoin-monitor.yml`: runs the Bitcoin alert workflow
- `/home/runner/work/agent-hello-world/agent-hello-world/.github/workflows/paper-execution.yml`: runs the paper execution workflow
- `/home/runner/work/agent-hello-world/agent-hello-world/.github/workflows/paper-position-monitor.yml`: runs the paper position monitor workflow
- `/home/runner/work/agent-hello-world/agent-hello-world/signals/`: committed signal inputs
- `/home/runner/work/agent-hello-world/agent-hello-world/positions/`: frozen paper positions
- `/home/runner/work/agent-hello-world/agent-hello-world/observations/`: research observations and follow-up notes

## Bitcoin alert

The Bitcoin workflow runs every six hours, can be started manually, and also runs on pushes that change the alert logic. It checks CoinGecko and opens a single GitHub issue titled **Bitcoin price alert** when the threshold is met.

### Try it from your iPhone

1. Open this repository in the GitHub app or Safari.
2. Open **Actions** → **Bitcoin price monitor**.
3. Tap **Run workflow**.
4. Leave **Force a test alert** set to `true`, then tap **Run workflow**.
5. Open **Issues** to see the alert issue.

### Configure the threshold

The default threshold is **$150,000**. To change it:

1. Open **Settings** → **Secrets and variables** → **Actions** → **Variables**.
2. Add a repository variable named `BTC_ALERT_ABOVE_USD`.
3. Set it to the target price, such as `125000`.

The scheduled run uses that threshold and will not create duplicates while an open issue titled **Bitcoin price alert** already exists.

## Paper execution

The paper execution workflow reads a committed JSON signal, applies deterministic sizing and slippage rules, and opens a GitHub issue containing the frozen execution record.

- It is **simulation only**
- It never sends a transaction
- It never accesses a wallet
- It preserves the execution record for later monitoring

Run **Actions** → **Crypto paper execution** and provide a committed file from `/home/runner/work/agent-hello-world/agent-hello-world/signals/`, or let pushes to that directory trigger the workflow automatically.

## Paper position monitor

The paper position monitor reads a saved position from `/home/runner/work/agent-hello-world/agent-hello-world/positions/`, fetches the live pair from DexScreener, and comments on the associated issue when:

- the position state changes
- or the daily heartbeat has not been posted yet

Possible states include `HOLD`, `SCALE_READY`, `TP1`, `TP2`, `STOP`, `STRUCTURAL_FAIL`, and `LIQUIDITY_WARNING`.

## Notes

- GitHub Issues and comments are used as the visible log of alerts, simulated trades, and monitoring updates.
- Workflow output names are part of the contract between the Python scripts and the workflow files.
- The repo currently mixes a simple public demo with a more opinionated paper-trading research flow, so the README focuses on explaining both clearly rather than pretending it is only one thing.