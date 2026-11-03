# liminal-plugin-federal

The US federal agencies and regulators for [Liminal](https://github.com/pcxmac-dev/liminal-app): one
plugin, each agency a part of it with its own scrape checks (its hosts, floor, daily cap,
robots.txt, holds, pause and limits recheck) and its own state:

- the Federal Reserve (`fed`): press releases, speeches and testimony; the FOMC's calendar and
  release moments;
- the New York Fed (`nyfed`): the federal funds target range, the effective rate and SOFR;
- the SEC (`sec`): press releases and trading suspensions, once you set `GOV_CONTACT` (your name and
  email, sent in the User-Agent to the SEC only, as it asks);
- the Bureau of Labor Statistics (`bls`): the employment situation, CPI, PPI and job openings;
- the Federal Register (`fedreg`): rules and notices of the SEC (FINRA's and the exchanges' rule
  filings), the CFTC, the Fed and the Treasury;
- the CFTC (`cftc`): its Commitments of Traders, a dataset.

Official feeds and documented APIs only, never a page. Pausing the plugin pauses every agency in it.

A Liminal publisher plugin released on its own. The app finds it through the entry point group
`liminal.providers` and lists it on the Plugins view and in `liminal plugins`
as `package: liminal-plugin-federal`, with this package's version.

## Install

Into the app's environment, from the app's folder:

```powershell
.venv\Scripts\python.exe -m pip install "liminal-plugin-federal @ git+https://github.com/pcxmac-dev/liminal-plugin-federal@v1.4.1"
```

or with the app's plugins (`pip install -e ".[plugins]"` in liminal-app). The app loads it on its next
start. Set `GOV_CONTACT` with the app's `tools/set-key.ps1` or on the Plugins view (a user
environment variable, never written to a file).

## Compatibility

It is written for plugin API 1.7 (`API` in `release.py`: parts of one plugin, a publisher's keys,
the datasets its parts declare, each feed's own parser). An app offering 1.7 or a later 1.x loads
it; an app of another major, or one older than 1.7, leaves it out and says why on the Plugins view.

## Develop

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install "liminal-lib @ git+https://github.com/pcxmac-dev/liminal-lib@main"
.venv\Scripts\python.exe -m pip install -e ".[dev]"
.venv\Scripts\python.exe -m pytest -q
```

Tests never send requests and never read your keys.
