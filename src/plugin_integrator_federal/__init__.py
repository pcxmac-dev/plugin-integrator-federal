"""Federal: the US federal agencies and regulators whose actions and releases move or govern
companies and stocks, one plugin (the user, 2026-10-30: "merge everything in to a Federal plugin,
from news feeds to edgar access, to everything that matters"; state agencies go in a plugin of
their own).

Each agency is a part of it (PublisherPlugin.part_of; plugin API 2.0, the class contract: Agency,
agency.py, is the PublisherPlugin subclass they share, each agency a subclass of it in a module here),
with its own scrape checks: its hosts, floor, daily cap, robots.txt, holds, pause and limits recheck,
and its own state kept by its name (gov/gov.db, the kills), as when each was a plugin of its own:
- the Federal Reserve (fed.py, FederalReserve): press releases, speeches and testimony; the FOMC's
  calendar and release moments;
- the New York Fed (nyfed.py, NewYorkFed): the federal funds target range, the effective rate and SOFR;
- the SEC (sec.py, SEC): press releases and trading suspensions (waiting for GOV_CONTACT);
- the Bureau of Labor Statistics (bls.py, BLS): the employment situation, CPI, PPI and job openings;
- the Federal Register (fedreg.py, FederalRegister): rules and notices of the SEC (FINRA's and the
  exchanges' rule filings), the CFTC, the Fed and the Treasury;
- the CFTC (cftc.py, CommodityFuturesTradingCommission): its Commitments of Traders, a dataset
  (PublisherPlugin.datasets).

The plugin's own publisher (FEDERAL, a Federal) reads nothing: pausing it pauses every agency in it
(publications: Reader.kill), and the Plugins view lists it once with its agencies. Its design, and
what is to be added (EDGAR's company data, the Treasury, the banks' regulators, the economic
calendars, the sector regulators, Congress): docs/ARCHITECTURE.md in liminal, "The Federal plugin".

A Liminal plugin released on its own, registered under the entry point group `liminal.providers` as
`federal` (a module of publishers: PUBLISHERS, the instances). It relies on plugin API 2.0 and nothing
of the app outside the contract; its version is this distribution's (release.py), so each class's is
left empty."""
from __future__ import annotations

from liminal_libs.sources.publisher import Policy, PublisherPlugin

from .agency import Agency  # noqa: F401  (the agencies' base, the package's to import)
from .bls import PUBLISHER as BLS
from .cftc import PUBLISHER as CFTC
from .fed import PUBLISHER as FED
from .fedreg import PUBLISHER as FEDREG
from .nyfed import PUBLISHER as NYFED
from .release import API, VERSION
from .sec import PUBLISHER as SEC


class Federal(PublisherPlugin):
    """The plugin: the publisher its agencies are parts of (their `part_of`). No feeds, no hooks: it
    reads nothing itself; pausing it pauses every agency in it, and the Plugins view lists it once
    with them."""

    version = VERSION  # the plugin's release, and the contract it needs (its agencies' part_of)
    api = API
    name = "federal"
    title = "Federal"
    order = 195
    about = ("US federal agencies and regulators: the Fed, the New York Fed, the SEC, BLS, the Federal Register "
             "and the CFTC; official feeds and documented APIs only")
    feeds = ()
    policy = Policy(terms="each agency's own: official feeds and documented APIs, never a page")


FEDERAL = Federal()

PUBLISHERS = (FEDERAL, FED, NYFED, SEC, BLS, FEDREG, CFTC)
