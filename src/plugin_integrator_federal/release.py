"""The Federal plugin's release and the plugin contract it needs (sources/registry.py: PLUGIN_API
2.2, the class contract with what each part attaches to (apis.py): the plugin and each agency in it a PublisherPlugin subclass (agency.py:
Agency), parts of one plugin (part_of), a publisher's keys (the SEC's GOV_CONTACT), the datasets its
parts declare (the CFTC's Commitments of Traders) and each feed's parser and item kind (Feed.parse,
item_kind)): one for the plugin and each agency in it; the version is the package's."""
VERSION = ""  # the distribution's (pyproject.toml): the app shows it for the plugin and each agency
API = "2.2"
