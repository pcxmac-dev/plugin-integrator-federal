# Changelog

## 1.4.1 (2026-11-02)

The plugin imports the library as `liminal_lib` and depends on liminal-lib (the app, renamed liminal-app, is no longer needed to run the tests; the user, 2026-11-02: "lets rename the app to liminal-app").

## 1.4.0 (2026-11-01)

- Released as its own package, `liminal-plugin-federal`, registered under the entry point group
  `liminal.providers` (a module of publishers: the plugin's record and its six agencies); its
  version is the distribution's, for the plugin and each agency.
- Plugin API 1.7; the agencies' release moments take New York time from the contract
  (`liminal.sources.archive.ET`).

## 1.3.0 (2026-10-31)

- Built into the app (then massive-collate): each feed's own parser and item kind (plugin API 1.7).

## 1.2.0 and before

- Built into the app (then massive-collate): the agencies merged into one plugin (parts, API 1.2),
  the SEC's GOV_CONTACT and the CFTC's dataset (API 1.4); see the app's history.
