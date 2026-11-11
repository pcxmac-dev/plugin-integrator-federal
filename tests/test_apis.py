"""What the agencies attach to (plugin API 2.2, apis.py): each agency declares its own card (the plugin, which reads
nothing itself, all six), each card is sound, names the feeds, the API paths and the files its agency really reads (the
feeds' and the dataset's own addresses) among the rest of what the agency publishes, and every address on it is the
agency's own. The page check (each address asked once) runs only with LIMINAL_VENDOR_PAGES=1, the weekly CI run's;
nothing is sent otherwise. The user, 2026-11-11: "each plugin should reflect the the API its attached to, and present
links that provide documentation"."""
from __future__ import annotations

import os
import re
from datetime import date
from urllib.parse import urlsplit

import pytest

from liminal_libs.sources.apis import dead_links, problems, urls

import plugin_integrator_federal as federal
from plugin_integrator_federal import apis as cards

TODAY = date(2026, 11, 11)
HOSTS = {  # each agency's own hosts: every address on its card is one of them
    "fed": {"www.federalreserve.gov"},
    "nyfed": {"markets.newyorkfed.org", "www.newyorkfed.org"},
    "sec": {"www.sec.gov"},
    "bls": {"www.bls.gov", "data.bls.gov"},
    "fedreg": {"www.federalregister.gov"},
    "cftc": {"www.cftc.gov", "publicreporting.cftc.gov", "dev.socrata.com"},  # its data API's page is Socrata's
}


def by_name():
    return {p.name: p for p in federal.PUBLISHERS}


def read_by(p) -> set[str]:
    """The addresses an agency really reads: its feeds' (without the query) and its datasets' files'."""
    out = {f.url.split("?")[0] for f in p.feeds}
    out |= {url for d in p.datasets for url, _ in d.files(TODAY)}
    return out


def matches(call: str, base: str, url: str) -> bool:
    """Whether a call on a card ("GET /path", a {year} in it standing for any year) is a request for `url`."""
    pattern = re.escape(base + call.removeprefix("GET ")).replace(r"\{year\}", r"\d{4}")
    return re.fullmatch(pattern, url) is not None


def test_each_agency_declares_its_own_card_and_the_plugin_all_six():
    assert problems(cards.APIS, today=TODAY) == []
    pubs = by_name()
    assert {n: p.apis for n, p in pubs.items() if n != "federal"} == {n: (a,) for n, a in cards.AGENCY_APIS.items()}
    assert pubs["federal"].apis == cards.APIS and len(cards.APIS) == 6
    assert all(a.verified == "2026-11-11" and a.docs for a in cards.APIS)
    assert all(p.api_facts() == {} for p in pubs.values())  # they learn nothing while they run: the reader reads
    assert pubs["sec"].interface()["apis"] == ["SEC RSS feeds and EDGAR"]


@pytest.mark.parametrize("name", sorted(cards.AGENCY_APIS))
def test_each_card_names_what_its_agency_really_reads(name):
    """Each call an agency makes is a request for one of its feeds' or its dataset's addresses, and each of those
    addresses is a call on its card; the agency's other feeds, endpoints and files follow, not used."""
    p, api = by_name()[name], cards.AGENCY_APIS[name]
    read = read_by(p)
    used = [c.name for c in api.used]
    assert read and all(c.startswith("GET ") for c in used)
    assert all(any(matches(c, api.base, url) for c in used) for url in read), sorted(read)  # every request is named
    assert all(any(matches(c, api.base, url) for url in read) for c in used), used  # and nothing else is used
    areas = {a.name for a in api.areas}
    assert all(c.area in areas for c in api.calls)  # every call is in a part of the agency's API
    assert api.covered and len(api.areas) > len(api.covered) and len(api.calls) > len(api.used)
    assert not any(c.writes or c.costs for c in api.calls)  # each reads; nothing changes or is billed


@pytest.mark.parametrize("name", sorted(cards.AGENCY_APIS))
def test_every_address_is_the_agencys_own(name):
    assert {urlsplit(u).hostname for u in urls((cards.AGENCY_APIS[name],))} <= HOSTS[name]


def test_the_cards_say_the_limits_their_agencies_publish():
    assert "10 requests a second" in cards.SEC_API.limits and "User-Agent" in cards.SEC_API.auth
    assert "500 queries a day" in cards.BLS_API.limits and "25 queries a day" in cards.BLS_API.limits
    assert cards.FEDREG_API.auth.startswith("none") and cards.NYFED_API.auth.startswith("none")
    assert all(a.costs == "" for a in cards.APIS)  # every agency publishes for programs at no cost


@pytest.mark.skipif(not os.environ.get("LIMINAL_VENDOR_PAGES"),
                    reason="LIMINAL_VENDOR_PAGES=1 asks each address on the cards (the weekly CI run)")
def test_every_address_on_the_cards_answers():
    assert dead_links(cards.APIS) == []
