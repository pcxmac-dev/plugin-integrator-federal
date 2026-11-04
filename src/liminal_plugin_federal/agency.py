"""What the federal agencies share: each is a part of the Federal plugin (part_of: listed in it and
stopped while it is paused, its own scrape checks, state and pause still its own), an official
publisher on the plugin's release and contract (release.py). An agency is a subclass in a module of
its own (fed.py, nyfed.py, sec.py, bls.py, fedreg.py, cftc.py), declaring its name, feeds, scrape
checks, keys and datasets as class attributes and its release moments and calendar as methods where
it has them; the package module keeps their instances (PUBLISHERS)."""
from __future__ import annotations

from liminal_lib.sources.publisher import PublisherPlugin

from .release import API, VERSION


class Agency(PublisherPlugin):
    """A federal agency: a publisher part of the Federal plugin. A subclass sets `name`, `title`,
    `order`, `about`, `feeds` and `policy` (and `keys`, `datasets` where it has them), and overrides
    `moments` (its reads at its release moments) and `calendar` (its scheduled releases, for the
    views) where it publishes at set times; the contract's defaults otherwise (none)."""

    version = VERSION  # the Federal plugin's release and contract (release.py), the same for every agency
    api = API
    part_of = "federal"
    kind = "official"
    # what the agencies' own feeds and files are, in their policies' terms: a U.S. government work
    PUBLIC_DOMAIN = "public domain (a U.S. government work)"
