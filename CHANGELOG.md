# Changelog

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
