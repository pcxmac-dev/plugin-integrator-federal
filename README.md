# plugin-integrator-federal

The US federal agencies and regulators for [Liminal](https://github.com/pcxmac-dev/liminal-charts): one
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
`liminal.providers` and lists it on the Plugins view and in `liminal-charts plugins`
as `package: plugin-integrator-federal`, with this package's version.

## Install

Into the app's environment, from the app's folder:

```powershell
.venv\Scripts\python.exe -m pip install "plugin-integrator-federal @ git+https://github.com/pcxmac-dev/plugin-integrator-federal@v0.3.0"
```

or with the app's plugins (`pip install -e ".[plugins]"` in liminal-charts). The app loads it on its next
start. Set `GOV_CONTACT` with the app's `tools/set-key.ps1` or on the Plugins view (a user
environment variable, never written to a file).

## Its APIs

Each agency is its own API, and each agency's card (`apis.py`, plugin API 2.2) says on its page what it is, its pages,
what the plugin reads of it and what else the agency publishes for programs, as read on 2026-11-11. None takes a key
or costs anything; the limits are the agency's where it publishes them, and the plugin's scrape checks besides.

- The Fed: the Board's [RSS feeds](https://www.federalreserve.gov/feeds/feeds.htm) (`press_all.xml`,
  `speeches_and_testimony.xml`), with the [FOMC calendars](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm)
  the decision days are written from, and the [Data Download Program](https://www.federalreserve.gov/datadownload/)
  beside them.
- The New York Fed: the [Markets Data API](https://markets.newyorkfed.org/static/docs/markets-api.html)
  ([OpenAPI](https://markets.newyorkfed.org/static/docs/markets-api.yml)): `/api/rates/unsecured/effr/last/1.json` and
  `/api/rates/secured/sofr/last/1.json`, among its reference rates, operations, SOMA holdings and dealer statistics.
- The SEC: its [RSS feeds](https://www.sec.gov/about/rss-feeds) (press releases, trading suspensions) and
  [EDGAR's APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces), under its
  [fair access policy](https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data): at most 10
  requests a second, with a User-Agent naming you (`GOV_CONTACT`).
- BLS: its [RSS feeds](https://www.bls.gov/feed/) (the employment situation, CPI, PPI, JOLTS) and the
  [Public Data API](https://www.bls.gov/developers/) (25 queries a day without a key, 500 with one).
- The Federal Register: its [API](https://www.federalregister.gov/developers/documentation/api/v1) (`/documents.json`,
  among documents, public inspection, agencies, images and suggested searches; no key).
- The CFTC: the [Commitments of Traders](https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm)
  [history files](https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm) (Legacy,
  futures only), beside its other reports and the COT Public Reporting Environment.

The plugin itself reads nothing: its own `apis` are the six cards.

## Compatibility

It is written for plugin API 2.2, the class contract of liminal-libs 1.49.0 (`API` in `release.py`): the
plugin is `Federal` and each agency a subclass of the package's `Agency`, a `PublisherPlugin` (parts of
one plugin, a publisher's keys, the datasets its parts declare, each feed's own parser, what each
attaches to; the Fed's release moments and calendar its methods). An app offering 2.2 or a later 2.x
loads it; an app of another major, or an older 2.x, leaves it out and says why on the Plugins view.

## Develop

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install "liminal-libs @ git+https://github.com/pcxmac-dev/liminal-libs@release/0.2.0"
.venv\Scripts\python.exe -m pip install -e ".[dev]"
.venv\Scripts\python.exe -m pytest -q
```

Tests never send requests and never read your keys.
