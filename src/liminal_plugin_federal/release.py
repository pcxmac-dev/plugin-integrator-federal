"""The Federal plugin's release and the plugin contract it needs (sources/registry.py: PLUGIN_API
1.7: Publisher.part_of, Publisher.keys (the SEC's GOV_CONTACT), the datasets its parts declare
(the CFTC's Commitments of Traders) and each feed's parser and item kind (Feed.parse, item_kind)):
one for the plugin and each agency in it; the version is the package's."""
VERSION = ""  # the distribution's (pyproject.toml): the app shows it for the plugin and each agency
API = "1.7"
