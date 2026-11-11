"""The New York Fed: the federal funds target range, the effective federal funds rate and SOFR,
from its Markets Data API (documented for programs, no key). It publishes each business day:
SOFR at about 8:00 a.m. ET and the effective rate at about 9:00 a.m., read just after those, and
every four hours besides."""
from __future__ import annotations

from datetime import date, datetime, time

from liminal_libs.sources.archive import ET
from liminal_libs.sources.publisher import Feed, Policy, Read

from .agency import Agency
from .apis import NYFED_API


def parse_nyfed(data: dict) -> dict | None:
    """The New York Fed's newest reference rate: {series, day, value, lo, hi} (lo/hi: the
    federal funds target range, on EFFR only)."""
    rows = data.get("refRates") or []
    if not rows:
        return None
    r = rows[0]
    return {"series": r.get("type"), "day": r.get("effectiveDate"), "value": r.get("percentRate"),
            "lo": r.get("targetRateFrom"), "hi": r.get("targetRateTo")}


def parse(answer, feed) -> Read:
    """Its Markets Data API's answer: the newest rate (none without its day)."""
    rate = parse_nyfed(answer.json())
    return Read(rates=[rate] if rate and rate["day"] else [])


class NewYorkFed(Agency):
    """The New York Fed: its reference rates from its Markets Data API (each feed parsed by
    `parse`), read just after it publishes them on a business day (`moments`)."""

    name = "nyfed"
    title = "New York Fed"
    order = 210
    about = "the federal funds target range, the effective federal funds rate and SOFR"
    apis = (NYFED_API,)  # what it attaches to (apis.py)
    feeds = (
        Feed("nyfed-effr", "New York Fed", "Effective federal funds rate and target range",
             "https://markets.newyorkfed.org/api/rates/unsecured/effr/last/1.json", "nyfed", every_minutes=240,
             parse=parse),
        Feed("nyfed-sofr", "New York Fed", "SOFR",
             "https://markets.newyorkfed.org/api/rates/secured/sofr/last/1.json", "nyfed", every_minutes=240,
             parse=parse),
    )
    policy = Policy(hosts=("markets.newyorkfed.org",), min_minutes=30, per_day=40,
                    terms="the Markets Data API, documented for programs; no key",
                    terms_url="https://markets.newyorkfed.org/static/docs/markets-api.html")

    def moments(self, day: date) -> tuple[datetime, ...]:
        if day.weekday() >= 5:
            return ()
        return tuple(datetime.combine(day, t, tzinfo=ET) for t in (time(8, 5), time(9, 5)))


PUBLISHER = NewYorkFed()
