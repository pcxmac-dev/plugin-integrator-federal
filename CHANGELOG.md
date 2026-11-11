# Changelog

## 0.3.0 (2026-11-11)

Their APIs on their pages (plugin API 2.2, liminal-libs 1.49.0; the user: "each plugin should reflect the the API its
attached to, and present links that provide documentation, the plugin interface should more or less contain what it
already has, BUT, it should also expose more of what the API is about"). Each agency declares its card (apis.py,
`apis`), from the agency's own pages, verified 2026-11-11:
- the Fed: the Board's RSS feeds (press releases and speeches read; the press releases by kind, governors, research,
  data releases and the Data Download Program not), with the FOMC calendars;
- the New York Fed: the Markets Data API (its ten parts from its OpenAPI document: the reference rates read; the
  operations, SOMA holdings, primary dealer statistics and guide sheets not);
- the SEC: its RSS feeds and EDGAR (press releases and trading suspensions read; the other feeds, the latest filings,
  the data.sec.gov submissions and XBRL APIs, full-text search and the bulk files not), with the fair access policy:
  10 requests a second, a User-Agent with a contact;
- BLS: its RSS feeds and the Public Data API (four release feeds read; the others, the latest-numbers feeds and the
  API's series, surveys and popular series not), with the API's limits;
- the Federal Register API (the document search read; the documents, issues, public inspection, agencies, images and
  suggested searches not), with its OpenAPI document;
- the CFTC: the Commitments of Traders files (the Legacy futures-only files read; the combined, Disaggregated, TFF and
  supplemental reports, the current week's and the COT Public Reporting Environment not).

The plugin (`Federal`), which reads nothing itself, declares all six. Nothing any of them reads or does changes; they
learn nothing while they run, so `api_facts()` says nothing. `API` (release.py) is "2.2". Needs liminal-libs>=1.49.0.
A test checks that each card names the feeds, paths and files its agency really reads; `LIMINAL_VENDOR_PAGES=1` asks
each address on them.

## 0.2.0 (2026-11-03)

Renamed `plugin-integrator-federal` (the package `plugin_integrator_federal`; it was `liminal-plugin-federal`) on 2026-11-03: the naming by system (plugins are `plugin-<app>-<name>`), on liminal-libs 1.4.0 (`liminal_libs`, the library renamed with it).

Classes on plugin API 2.0 (liminal-libs 1.3.0; the user: "all the plugins under liminal should basically
follow inheritance/oop paradigm"): `Agency` (agency.py), a `PublisherPlugin` subclass holding what the
agencies share (a part of the plugin, official, the plugin's release and contract, their terms' public-domain
phrase), and each agency a subclass of it in its module: `FederalReserve` (the FOMC's `moments` and `calendar`,
its methods now), `NewYorkFed`, `BLS` and `FederalRegister` (each with its `moments`), `SEC` (its `GOV_CONTACT`
key) and `CommodityFuturesTradingCommission` (its dataset; `cftc.CFTC` stays its history files' URL); the
plugin itself is `Federal`. What each record held are class attributes; the instances stay where they were
(`PUBLISHER` in each module, `PUBLISHERS` in the package, the entry point as before) and the feeds' parsers
stay functions. An agency's release moments are asked of its instance (`fed.PUBLISHER.moments(day)`, no
longer `fed.moments(day)`). Nothing an agency does or says changes. Version 0.2.0: every Liminal distribution
is released at 0.2.0 together, tested against the library's `release/0.2.0` branch until the release.

## 1.4.1 (2026-11-02)

The plugin imports the library as `liminal_libs` and depends on liminal-libs (the app, renamed liminal-charts, is no longer needed to run the tests; the user, 2026-11-02: "lets rename the app to liminal-charts").

## 1.4.0 (2026-11-01)

- Released as its own package, `plugin-integrator-federal`, registered under the entry point group
  `liminal.providers` (a module of publishers: the plugin's record and its six agencies); its
  version is the distribution's, for the plugin and each agency.
- Plugin API 1.7; the agencies' release moments take New York time from the contract
  (`liminal.sources.archive.ET`).

## 1.3.0 (2026-10-31)

- Built into the app (then massive-collate): each feed's own parser and item kind (plugin API 1.7).

## 1.2.0 and before

- Built into the app (then massive-collate): the agencies merged into one plugin (parts, API 1.2),
  the SEC's GOV_CONTACT and the CFTC's dataset (API 1.4); see the app's history.
