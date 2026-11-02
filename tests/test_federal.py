"""The Federal plugin, run against the app installed beside it: its parsers (the CFTC's report, the
Federal Register's documents, the New York Fed's rates), the agencies' release moments, and the app
loading the plugin and its six agencies from this package with its own version."""
from __future__ import annotations

from datetime import date, datetime, time
from importlib.metadata import version

from liminal.sources import publishers, registry
from liminal.sources.archive import ET
from liminal.sources.dataset import at, ms

import liminal_plugin_federal as federal
from liminal_plugin_federal import bls, cftc, fed, fedreg, nyfed, sec

AGENCIES = ["fed", "nyfed", "sec", "bls", "fedreg", "cftc"]
COT_HEADER = ("Market and Exchange Names,As of Date in Form YYMMDD,As of Date in Form YYYY-MM-DD,"
              "CFTC Contract Market Code,Open Interest (All),Noncommercial Positions-Long (All),"
              "Noncommercial Positions-Short (All),Noncommercial Positions-Spreading (All),"
              "Commercial Positions-Long (All),Commercial Positions-Short (All),"
              "Nonreportable Positions-Long (All),Nonreportable Positions-Short (All)\n")
FEDREG = {"results": [
    {"title": "Self-Regulatory Organizations; Financial Industry Regulatory Authority, Inc.; Order Granting Approval To "
              "Amend FINRA Rule 4210 (Margin Requirements) To Replace the Day Trading Margin Provisions",
     "type": "Notice", "publication_date": "2026-04-17", "html_url": "https://www.federalregister.gov/d/2026-1",
     "document_number": "2026-1", "agencies": [{"slug": "securities-and-exchange-commission"}]},
    {"title": "Self-Regulatory Organizations; New York Stock Exchange LLC; Notice of Filing (Clearly Erroneous Executions)",
     "type": "Notice", "publication_date": "2026-10-23", "html_url": "https://www.federalregister.gov/d/2026-2",
     "document_number": "2026-2", "agencies": [{"slug": "securities-and-exchange-commission"}]},
    {"title": "Position Limits for Derivatives", "type": "Proposed Rule", "publication_date": "2026-10-22",
     "html_url": "https://www.federalregister.gov/d/2026-3", "document_number": "2026-3",
     "agencies": [{"slug": "commodity-futures-trading-commission"}]},
]}


def _cot(day: str) -> str:
    return COT_HEADER + (f'"WHEAT-SRW - CHICAGO BOARD OF TRADE",{day[2:].replace("-", "")},{day},001602,'
                         "400000,100000,90000,20000,150000,200000,30000,20000\n")


def test_cot_series_per_market_and_field_and_the_files_close_once_a_years_last_report_is_out():
    parsed = cftc.parse_cot("annual.txt", _cot("2026-03-03").encode())
    assert parsed.series["001602:open_interest"] == ("WHEAT-SRW - CHICAGO BOARD OF TRADE: open interest", "contracts", "week")
    assert ("001602:commercial_short", parsed.values[0][1], 200000.0) in parsed.values
    assert len(parsed.values) == 8
    files = dict(cftc.cot_files(date(2026, 12, 31)))
    assert files[cftc.CFTC + "deacot1986_2016.zip"] is True and files[cftc.CFTC + "deacot2026.zip"] is False
    assert dict(cftc.cot_files(date(2027, 1, 5)))[cftc.CFTC + "deacot2026.zip"] is False  # its last Tuesday may not be out
    assert dict(cftc.cot_files(date(2027, 1, 15)))[cftc.CFTC + "deacot2026.zip"] is True
    tue = ms(date(2026, 10, 20))  # a report as of Tuesday is released that Friday at 15:30 ET
    assert datetime.fromtimestamp(cftc.cot_published(tue) / 1000, ET) == datetime(2026, 10, 23, 15, 30, tzinfo=ET)
    assert cftc.cot_published(at(date(2026, 10, 23))) == at(date(2026, 10, 23), 15, 30)  # a Friday's: that day


def test_the_federal_register_tags_finras_and_the_exchanges_filings():
    docs = {d["id"]: d for d in fedreg.parse_fedreg(FEDREG)}
    assert docs["2026-1"]["agency"] == "SEC" and docs["2026-1"]["tags"] == ["FINRA"]
    assert docs["2026-2"]["tags"] == ["SRO"] and docs["2026-3"]["agency"] == "CFTC"
    assert docs["2026-3"]["kind"] == "proposed rule" and docs["2026-3"]["published"] == "2026-10-22T00:00:00+00:00"
    assert fedreg.parse_fedreg({}) == [] and "conditions[agencies][]=securities-and-exchange-commission" in fedreg.FEDREG_URL


def test_the_new_york_feds_rates_are_read_with_the_target_range():
    effr = nyfed.parse_nyfed({"refRates": [{"effectiveDate": "2026-10-22", "type": "EFFR", "percentRate": 3.88,
                                            "targetRateFrom": 3.75, "targetRateTo": 4.00}]})
    assert effr == {"series": "EFFR", "day": "2026-10-22", "value": 3.88, "lo": 3.75, "hi": 4.00}
    sofr = nyfed.parse_nyfed({"refRates": [{"effectiveDate": "2026-10-23", "type": "SOFR", "percentRate": 3.91}]})
    assert sofr["series"] == "SOFR" and sofr["lo"] is None
    assert nyfed.parse_nyfed({"refRates": []}) is None


def test_the_agencies_release_moments():
    assert fed.moments(date(2026, 12, 9))[0] == datetime(2026, 12, 9, 14, 0, 20, tzinfo=ET)  # a decision day
    assert fed.moments(date(2026, 11, 18)) and not fed.moments(date(2026, 11, 19))  # the October minutes, three weeks after
    assert set(fed.FOMC_DECISIONS) >= {date(2026, 10, 28), date(2026, 12, 9), date(2027, 6, 9)}
    upcoming = fed.calendar(date(2026, 12, 1))
    assert upcoming[0]["kind"] == "fomc-decision" and upcoming[0]["projections"] is True
    assert bls.moments(date(2026, 11, 6)) == tuple(datetime.combine(date(2026, 11, 6), t, tzinfo=ET)
                                                   for t in (time(8, 30, 20), time(8, 33), time(10, 0, 20)))
    assert bls.moments(date(2026, 11, 7)) == () and nyfed.moments(date(2026, 11, 8)) == ()  # weekends
    assert nyfed.moments(date(2026, 11, 6)) == (datetime(2026, 11, 6, 8, 5, tzinfo=ET), datetime(2026, 11, 6, 9, 5, tzinfo=ET))
    assert fedreg.moments(date(2026, 11, 6)) == (datetime(2026, 11, 6, 6, 5, tzinfo=ET),)


def test_the_app_loads_the_plugin_and_its_agencies_from_this_package_with_its_own_version():
    registry.reload()
    assert [p.name for p in federal.PUBLISHERS] == ["federal", *AGENCIES]
    pubs = publishers()
    for name in ("federal", *AGENCIES):
        p = pubs.get(name)
        assert p is not None, dict(registry.errors())
        assert p.origin in {"package: liminal-plugin-federal (liminal_plugin_federal)", "plugins/liminal-plugin-federal (liminal_plugin_federal)"}  # its package, or its checkout in the workspace\'s plugin directory
        assert p.version == version("liminal-plugin-federal") and p.api == "1.7"
    assert federal.FEDERAL.version == "" and federal.VERSION == ""
    assert not [why for where, why in registry.errors() if "federal" in where or "federal" in why]
    assert list(pubs)[:7] == ["federal", *AGENCIES]  # the plugin's record first, its agencies after it
    assert all(pubs[n].part_of == "federal" for n in AGENCIES) and pubs["federal"].part_of == ""
    assert registry.publisher_parts("federal") == AGENCIES and registry.publisher_of("sec") == "federal"
    assert [k.name for k in pubs["sec"].keys] == ["GOV_CONTACT"] and not pubs["sec"].keys[0].secret
    assert [k.name for k in registry.plugin_keys("federal")] == ["GOV_CONTACT"]
    assert [f.key for f in pubs["fed"].feeds] == ["fed-press", "fed-speeches"] and pubs["sec"].policy.contact
    assert pubs["cftc"].feeds == () and pubs["cftc"].dataset_names == ("cftc-cot-legacy",)
    assert sec.PUBLISHER.policy.hosts == ("www.sec.gov",)
