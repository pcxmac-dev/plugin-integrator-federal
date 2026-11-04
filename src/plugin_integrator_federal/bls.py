"""The Bureau of Labor Statistics: the market-moving releases (the employment situation, CPI,
PPI, job openings), from its RSS feeds. Its releases come at 8:30 a.m. ET (JOLTS at 10:00), read
just after on weekdays, and every two hours besides."""
from __future__ import annotations

from datetime import date, datetime, time

from liminal_libs.sources.archive import ET
from liminal_libs.sources.publisher import Feed, Policy

from .agency import Agency


class BLS(Agency):
    """BLS: its data releases, read just after their 8:30 a.m. (JOLTS 10:00) release on a weekday
    (`moments`)."""

    name = "bls"
    title = "Bureau of Labor Statistics"
    order = 230
    about = "the employment situation, CPI, PPI and job openings, at their 8:30 a.m. releases"
    feeds = (
        Feed("bls-empsit", "BLS", "Employment Situation", "https://www.bls.gov/feed/empsit.rss", every_minutes=120,
             item_kind="data release"),
        Feed("bls-cpi", "BLS", "Consumer Price Index", "https://www.bls.gov/feed/cpi.rss", every_minutes=120,
             item_kind="data release"),
        Feed("bls-ppi", "BLS", "Producer Price Index", "https://www.bls.gov/feed/ppi.rss", every_minutes=120,
             item_kind="data release"),
        Feed("bls-jolts", "BLS", "Job openings and labor turnover", "https://www.bls.gov/feed/jolts.rss",
             every_minutes=120, item_kind="data release"),
    )
    policy = Policy(hosts=("www.bls.gov",), min_minutes=2, per_day=100,
                    terms=f"RSS feeds BLS offers for programs; {Agency.PUBLIC_DOMAIN}",
                    terms_url="https://www.bls.gov/feed/")

    def moments(self, day: date) -> tuple[datetime, ...]:
        if day.weekday() >= 5:
            return ()
        return tuple(datetime.combine(day, t, tzinfo=ET) for t in (time(8, 30, 20), time(8, 33), time(10, 0, 20)))


PUBLISHER = BLS()
