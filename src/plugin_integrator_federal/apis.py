"""What the plugin's agencies attach to (plugin API 2.2, liminal_libs.sources.apis), each as the agency's own pages
describe it (read 2026-11-11): the Federal Reserve Board's RSS feeds, the New York Fed's Markets Data API, the SEC's RSS
feeds and EDGAR, BLS's RSS feeds and Public Data API, the Federal Register API and the CFTC's Commitments of Traders
files. Each agency (a part of the plugin) declares its own card; the plugin, which reads nothing itself, declares all
six (APIS). The parts each agency reads come first, then the rest of what it publishes for programs. The user,
2026-11-11: "each plugin should reflect the the API its attached to, and present links that provide documentation ...
it should also expose more of what the API is about".

Every agency here publishes for programs at no cost and with no key (the SEC asks for a contact in the User-Agent);
the limits each card gives are the agency's where it publishes them, and the plugin's own scrape checks (its policy)
besides."""
from __future__ import annotations

from liminal_libs.sources.apis import Api, Area, Call, Link

VERIFIED = "2026-11-11"  # the day these facts were read from the agencies' pages

# -- the Federal Reserve Board ------------------------------------------------------------------------------------------

FRB = "https://www.federalreserve.gov"
FRB_FEEDS = FRB + "/feeds/feeds.htm"
FRB_FOMC = FRB + "/monetarypolicy/fomccalendars.htm"
FRB_DDP = FRB + "/datadownload/"

FED_API = Api(
    name="Federal Reserve Board RSS feeds",
    maker="Board of Governors of the Federal Reserve System",
    about=("The Board's RSS 2.0 feeds for programs: its press releases (all of them, or by monetary policy, banking and "
           "consumer regulation, enforcement, orders on banking applications and other announcements), speeches and "
           "testimony (all, or each governor's), research papers, data releases (H.15, H.4.1, H.8, G.17, Z.1 ...) and "
           "other notices, each feed the newest items with links to the Board's pages. The FOMC's meeting calendar and "
           "the Data Download Program (the releases' series as files) are beside them."),
    kind="feed",
    base=FRB,
    version="RSS 2.0",
    auth="none: public feeds",
    limits=("none published; the plugin keeps its own: at most 120 requests a day, never one feed more often than once "
            "a minute (press releases every 30 minutes, speeches hourly, and at the FOMC's 2:00 p.m. ET releases)"),
    costs="",
    links=(
        Link("RSS feeds", FRB_FEEDS, "docs"),
        Link("FOMC meeting calendars", FRB_FOMC, "reference"),
        Link("Calendar", FRB + "/newsevents/calendar.htm", "reference"),
        Link("Data Download Program", FRB_DDP, "tool"),
        Link("Data Download Program: things you should know", FRB_DDP + "help/default.htm", "guide"),
        Link("Data", FRB + "/data.htm", "reference"),
    ),
    areas=(
        Area("Press releases", "every press release, or one kind: monetary policy, banking and consumer regulation, "
                               "enforcement actions, orders on banking applications, other announcements", FRB_FEEDS,
             covered="all press releases (fed-press), every 30 minutes and at the FOMC's release moments"),
        Area("Speeches and testimony", "all speeches and testimony, or each governor's", FRB_FEEDS,
             covered="all speeches and testimony (fed-speeches), hourly"),
        Area("FOMC meetings", "the decision days (with or without projections) and the minutes three weeks after",
             FRB_FOMC, covered="the decision days written in from the calendars (read 2026-10-28): the release moments "
                               "(2:00 p.m. ET) and the calendar of decisions and minutes"),
        Area("Research", "working papers, the Finance and Economics Discussion Series, International Finance "
                         "Discussion Papers, FEDS Notes", FRB_FEEDS),
        Area("Data releases", "a feed for each statistical release: H.15 selected interest rates, H.4.1 reserve "
                              "balances, H.8 bank assets, H.10 exchange rates, G.17 industrial production, G.19 consumer "
                              "credit, Z.1 financial accounts, policy rates ...", FRB_FEEDS),
        Area("Data Download Program", "each release's series as CSV, Excel or XML files, chosen by series and dates",
             FRB_DDP),
        Area("Other notices", "board meetings, reporting forms, supervision and regulation letters, credit and "
                              "liquidity programs, the Inspector General", FRB_FEEDS),
    ),
    calls=(
        Call("GET /feeds/press_all.xml", "all press releases", "Press releases",
             used="the fed-press feed", docs=FRB_FEEDS),
        Call("GET /feeds/speeches_and_testimony.xml", "all speeches and testimony", "Speeches and testimony",
             used="the fed-speeches feed", docs=FRB_FEEDS),
        Call("GET /feeds/press_monetary.xml", "monetary policy press releases only", "Press releases", docs=FRB_FEEDS),
        Call("GET /feeds/press_bcreg.xml", "banking and consumer regulatory policy", "Press releases", docs=FRB_FEEDS),
        Call("GET /feeds/press_enforcement.xml", "enforcement actions", "Press releases", docs=FRB_FEEDS),
        Call("GET /feeds/speeches.xml", "all speeches", "Speeches and testimony", docs=FRB_FEEDS),
        Call("GET /feeds/testimony.xml", "all testimony", "Speeches and testimony", docs=FRB_FEEDS),
        Call("GET /feeds/h15.xml", "the H.15 selected interest rates release", "Data releases", docs=FRB_FEEDS),
        Call("GET /feeds/h41.xml", "the H.4.1 factors affecting reserve balances", "Data releases", docs=FRB_FEEDS),
        Call("GET /feeds/prates.xml", "policy rates", "Data releases", docs=FRB_FEEDS),
        Call("GET /datadownload/Choose.aspx?rel=H15", "the H.15 series to download", "Data Download Program",
             docs=FRB_DDP),
    ),
    verified=VERIFIED,
)

# -- the New York Fed ---------------------------------------------------------------------------------------------------

NYFED = "https://markets.newyorkfed.org"
NYFED_DOCS = NYFED + "/static/docs/markets-api.html"
RATES = "Reference Rates"

NYFED_API = Api(
    name="New York Fed Markets Data API",
    maker="Federal Reserve Bank of New York",
    about=("The New York Fed's REST API for the markets data it publishes: the reference rates (EFFR, OBFR, SOFR, BGCR, "
           "TGCR, the SOFR averages and index), its open market operations (repo and reverse repo, Treasury and agency "
           "MBS operations, securities lending, central bank liquidity swaps), the System Open Market Account's "
           "holdings, primary dealer statistics and guide sheets. Each path ends in its format (json, xml, csv, xlsx); "
           "a beta copy of each service is under /beta."),
    kind="rest",
    base=NYFED,
    version="1.0 (its OpenAPI 3.0 document, last updated June 12, 2026)",
    auth="none: no key",
    limits=("none published (an invalid path or parameter answers 400 with the reasons); the plugin keeps its own: at "
            "most 40 requests a day, 30 minutes apart at least (each rate every four hours and just after 8:00 and "
            "9:00 a.m. ET)"),
    costs="",
    links=(
        Link("Markets Data APIs", NYFED_DOCS, "reference"),
        Link("OpenAPI document", NYFED + "/static/docs/markets-api.yml", "spec"),
        Link("Terms of use", "https://www.newyorkfed.org/privacy/termsofuse", "terms"),
    ),
    areas=(
        Area(RATES, "the secured (SOFR, BGCR, TGCR, the SOFR averages and index) and unsecured (EFFR, OBFR) rates",
             NYFED_DOCS, covered="the effective federal funds rate with the target range, and SOFR: the newest of each"),
        Area("Repo and Reverse Repo Operations", "repo, reverse repo and propositions", NYFED_DOCS),
        Area("Treasury Securities Operations", "outright purchases and sales, and the prices paid", NYFED_DOCS),
        Area("Agency Mortgage-Backed Securities Operations", "outrights, dollar rolls and coupon swaps", NYFED_DOCS),
        Area("Securities Lending Operations", "securities lending and extensions", NYFED_DOCS),
        Area("Central Bank Liquidity Swaps Operations", "U.S. dollar and non-U.S. dollar swaps", NYFED_DOCS),
        Area("System Open Market Account Holdings", "the SOMA's Treasury and agency holdings by date", NYFED_DOCS),
        Area("Primary Dealer Statistics", "the primary dealer survey's series", NYFED_DOCS),
        Area("Primary Dealer Statistics Market Share", "quarterly and year-to-date market shares", NYFED_DOCS),
        Area("Guide Sheets", "the FR 2004SI, FR 2004WI and FR 2004F series", NYFED_DOCS),
    ),
    calls=(
        Call("GET /api/rates/unsecured/effr/last/1.json", "the newest effective federal funds rate", RATES,
             used="the nyfed-effr feed: the rate, its day and the target range", docs=NYFED_DOCS),
        Call("GET /api/rates/secured/sofr/last/1.json", "the newest SOFR", RATES,
             used="the nyfed-sofr feed: the rate and its day", docs=NYFED_DOCS),
        Call("GET /api/rates/all/latest.{format}", "every reference rate's newest value", RATES, docs=NYFED_DOCS),
        Call("GET /api/rates/secured/{ratetype}/search.{format}", "a secured rate between two dates", RATES,
             docs=NYFED_DOCS),
        Call("GET /api/rates/unsecured/{ratetype}/search.{format}", "an unsecured rate between two dates", RATES,
             docs=NYFED_DOCS),
        Call("GET /api/rp/results/search.{format}", "repo and reverse repo results between two dates",
             "Repo and Reverse Repo Operations", docs=NYFED_DOCS),
        Call("GET /api/tsy/{operation}/results/{include}/latest.{format}", "the latest Treasury operations' results",
             "Treasury Securities Operations", docs=NYFED_DOCS),
        Call("GET /api/soma/summary.{format}", "the SOMA holdings' summary by date",
             "System Open Market Account Holdings", docs=NYFED_DOCS),
        Call("GET /api/pd/get/all/timeseries.csv", "every primary dealer statistics series",
             "Primary Dealer Statistics", docs=NYFED_DOCS),
    ),
    verified=VERIFIED,
)

# -- the SEC ------------------------------------------------------------------------------------------------------------

SEC = "https://www.sec.gov"
SEC_DEV = SEC + "/about/developer-resources"
SEC_RSS = SEC + "/about/rss-feeds"
SEC_EDGAR = SEC + "/search-filings/edgar-application-programming-interfaces"
SEC_ACCESS = SEC + "/search-filings/edgar-search-assistance/accessing-edgar-data"
XBRL = "EDGAR XBRL APIs"

SEC_API = Api(
    name="SEC RSS feeds and EDGAR",
    maker="U.S. Securities and Exchange Commission",
    about=("The SEC's RSS feeds of its own news (press releases, speeches and statements, testimony, litigation "
           "releases, administrative proceedings, trading suspensions), and EDGAR, its filings system: the latest "
           "filings as an Atom feed, the data.sec.gov JSON APIs (a company's submissions, its XBRL facts and concepts, "
           "frames of one fact across companies), full-text search and the bulk archives. Every automated reader must "
           "identify itself in the User-Agent and keep to the fair access rate."),
    kind="feed",
    base=SEC,
    version="RSS 2.0",
    auth=("none, but the fair access policy: a User-Agent naming you and an email (GOV_CONTACT: nothing is sent until "
          "it is set); data.sec.gov needs no key"),
    limits=("at most 10 requests a second, however many machines (fair access); automated tools outside the policy are "
            "managed or blocked. The plugin reads each feed hourly: at most 60 requests a day, 15 minutes apart"),
    costs="",
    links=(
        Link("Developer resources", SEC_DEV, "docs"),
        Link("RSS feeds", SEC_RSS, "reference"),
        Link("EDGAR application programming interfaces", SEC_EDGAR, "reference"),
        Link("Accessing EDGAR data (fair access)", SEC_ACCESS, "limits"),
        Link("Webmaster frequently asked questions", SEC + "/about/webmaster-frequently-asked-questions", "guide"),
        Link("EDGAR full-text search", SEC + "/edgar/search/", "tool"),
    ),
    areas=(
        Area("Press releases", "the SEC's press releases", SEC_RSS,
             covered="sec-press, hourly, once GOV_CONTACT is set"),
        Area("Trading suspensions", "the SEC's trading suspensions", SEC_RSS,
             covered="sec-suspensions, hourly, once GOV_CONTACT is set"),
        Area("Speeches, statements and testimony", "the Commission's speeches and statements, and its testimony",
             SEC_RSS),
        Area("Litigation releases and administrative proceedings", "the SEC's enforcement actions in court and in its "
                                                                   "own proceedings", SEC_RSS),
        Area("EDGAR latest filings", "the newest filings of every form, or of one (10-K ...), as an Atom feed", SEC_RSS),
        Area("EDGAR submissions API", "a company's filing history and its names, tickers and exchanges (data.sec.gov)",
             SEC_EDGAR),
        Area(XBRL, "a company's facts, one concept of a company, one fact across companies for a period (data.sec.gov)",
             SEC_EDGAR),
        Area("EDGAR full-text search", "every filing's text, searched", SEC + "/edgar/search/"),
        Area("Bulk data", "the daily and full indexes, the daily feed archives, companyfacts.zip and submissions.zip "
                          "(recompiled nightly)", SEC_ACCESS),
    ),
    calls=(
        Call("GET /news/pressreleases.rss", "the press releases", "Press releases", used="the sec-press feed",
             docs=SEC_RSS),
        Call("GET /enforcement-litigation/trading-suspensions/rss", "the trading suspensions", "Trading suspensions",
             used="the sec-suspensions feed", docs=SEC_RSS),
        Call("GET /news/speeches-statements.rss", "speeches and statements", "Speeches, statements and testimony",
             docs=SEC_RSS),
        Call("GET /news/testimony.rss", "testimony", "Speeches, statements and testimony", docs=SEC_RSS),
        Call("GET /enforcement-litigation/litigation-releases/rss", "litigation releases",
             "Litigation releases and administrative proceedings", docs=SEC_RSS),
        Call("GET /enforcement-litigation/administrative-proceedings/rss", "administrative proceedings",
             "Litigation releases and administrative proceedings", docs=SEC_RSS),
        Call("GET /cgi-bin/browse-edgar?action=getcurrent&output=atom", "the latest filings (type=10-k for one form)",
             "EDGAR latest filings", docs=SEC_RSS),
        Call("GET data.sec.gov/submissions/CIK##########.json", "a company's submissions", "EDGAR submissions API",
             docs=SEC_EDGAR),
        Call("GET data.sec.gov/api/xbrl/companyfacts/CIK##########.json", "every XBRL fact of a company", XBRL,
             docs=SEC_EDGAR),
        Call("GET data.sec.gov/api/xbrl/companyconcept/CIK##########/us-gaap/{concept}.json",
             "one concept's facts for a company", XBRL, docs=SEC_EDGAR),
        Call("GET data.sec.gov/api/xbrl/frames/us-gaap/{concept}/USD/{period}.json",
             "one fact for every company in a period (CY2019, CY2019Q1, CY2019Q1I)", XBRL, docs=SEC_EDGAR),
        Call("GET /Archives/edgar/daily-index/xbrl/companyfacts.zip", "every company's facts in one file", "Bulk data",
             docs=SEC_EDGAR),
    ),
    verified=VERIFIED,
)

# -- BLS ----------------------------------------------------------------------------------------------------------------

BLS = "https://www.bls.gov"
BLS_FEEDS = BLS + "/feed/"
BLS_DEV = BLS + "/developers/"
BLS_SIGNATURES = BLS + "/developers/api_signature_v2.htm"
BLS_FAQ = BLS + "/developers/api_faqs.htm"
JOBS = "Employment and unemployment releases"
PRICES = "Inflation and prices releases"
SERIES = "Public Data API: time series"

BLS_API = Api(
    name="BLS RSS feeds and Public Data API",
    maker="U.S. Bureau of Labor Statistics",
    about=("BLS publishes an RSS feed for each of its news releases (the employment situation, CPI, PPI, job openings "
           "and 45 others) and latest-numbers feeds of its principal indicators. Its Public Data API gives the "
           "time series behind them as JSON or Excel: version 2.0 with a registration key (more data, more often, "
           "with calculations, annual averages and series descriptions), version 1.0 without one."),
    kind="feed",
    base=BLS,
    version="RSS 2.0 (the release feeds)",
    auth="none for the feeds; the Public Data API's version 2.0 takes a registration key (registrationkey), 1.0 none",
    limits=("the Public Data API: 25 queries a day, 25 series and 10 years a query without a key; 500 queries a day, "
            "50 series and 20 years a query with one; 50 requests per 10 seconds either way. The plugin reads each "
            "feed every two hours and just after the 8:30 a.m. ET releases (JOLTS 10:00): at most 100 requests a day"),
    costs="",
    links=(
        Link("RSS feeds", BLS_FEEDS, "docs"),
        Link("Public Data API", BLS_DEV, "docs"),
        Link("API signatures, version 2.0", BLS_SIGNATURES, "reference"),
        Link("API frequently asked questions", BLS_FAQ, "limits"),
        Link("API terms of service", BLS + "/developers/termsOfService.htm", "terms"),
        Link("API registration", "https://data.bls.gov/registrationEngine/", "console"),
        Link("API release notes", BLS + "/bls/api_features.htm", "changelog"),
    ),
    areas=(
        Area(JOBS, "the employment situation, job openings and labor turnover, state and metro employment, earnings "
                   "and some twenty others", BLS_FEEDS,
             covered="the employment situation (bls-empsit) and job openings and labor turnover (bls-jolts)"),
        Area(PRICES, "CPI, PPI, import and export prices, consumer expenditures", BLS_FEEDS,
             covered="CPI (bls-cpi) and PPI (bls-ppi)"),
        Area("Pay and benefits releases", "the employment cost index, employer costs, benefits, work stoppages",
             BLS_FEEDS),
        Area("Productivity releases", "productivity and costs, by sector and industry", BLS_FEEDS),
        Area("Workplace injuries releases", "fatal and nonfatal workplace injuries", BLS_FEEDS),
        Area("Latest numbers feeds", "the principal federal economic indicators' newest values, by program", BLS_FEEDS),
        Area(SERIES, "one or more series' data, with optional years, catalog, calculations and annual averages",
             BLS_SIGNATURES),
        Area("Public Data API: surveys and popular series", "the surveys and each one's most popular series",
             BLS_SIGNATURES),
    ),
    calls=(
        Call("GET /feed/empsit.rss", "the employment situation", JOBS, used="the bls-empsit feed", docs=BLS_FEEDS),
        Call("GET /feed/cpi.rss", "the consumer price index", PRICES, used="the bls-cpi feed", docs=BLS_FEEDS),
        Call("GET /feed/ppi.rss", "the producer price index", PRICES, used="the bls-ppi feed", docs=BLS_FEEDS),
        Call("GET /feed/jolts.rss", "job openings and labor turnover", JOBS, used="the bls-jolts feed", docs=BLS_FEEDS),
        Call("GET /feed/eci.rss", "the employment cost index", "Pay and benefits releases", docs=BLS_FEEDS),
        Call("GET /feed/prod2.rss", "productivity and costs", "Productivity releases", docs=BLS_FEEDS),
        Call("GET /feed/ximpim.rss", "U.S. import and export price indexes", PRICES, docs=BLS_FEEDS),
        Call("GET /feed/bls_latest.rss", "the principal federal economic indicators", "Latest numbers feeds",
             docs=BLS_FEEDS),
        Call("GET api.bls.gov/publicAPI/v2/timeseries/data/<series_id>", "one series' data", SERIES,
             docs=BLS_SIGNATURES),
        Call("POST api.bls.gov/publicAPI/v2/timeseries/data/", "several series' data, with optional parameters", SERIES,
             docs=BLS_SIGNATURES),
        Call("GET api.bls.gov/publicAPI/v2/timeseries/popular", "the most popular series",
             "Public Data API: surveys and popular series", docs=BLS_SIGNATURES),
        Call("GET api.bls.gov/publicAPI/v2/surveys", "every survey", "Public Data API: surveys and popular series",
             docs=BLS_SIGNATURES),
    ),
    verified=VERIFIED,
)

# -- the Federal Register -----------------------------------------------------------------------------------------------

FEDREG = "https://www.federalregister.gov"
FEDREG_DOCS = FEDREG + "/developers/documentation/api/v1"
FEDREG_AIDS = FEDREG + "/reader-aids/developer-resources"
DOCUMENTS = "Federal Register Documents"
INSPECTION = "Public Inspection Documents"

FEDREG_API = Api(
    name="Federal Register API",
    maker="Office of the Federal Register (National Archives) and the U.S. Government Publishing Office",
    about=("FederalRegister.gov's documented JSON API, with no key: a search of every document published in the "
           "Federal Register since 1994 (rules, proposed rules, notices, presidential documents) by agency, type, date "
           "and words, each document's details, the documents on public inspection before they publish, each issue's "
           "table of contents, the agencies, images and suggested searches. The bulk XML is GPO's, on govinfo.gov."),
    kind="rest",
    base=FEDREG + "/api/v1",
    version="v1",
    auth="none: no key",
    limits=("none published; the plugin keeps its own: at most 30 requests a day, 30 minutes apart at least (every "
            "three hours and just after the 6:00 a.m. ET publication)"),
    costs="",
    links=(
        Link("API documentation", FEDREG_DOCS, "reference"),
        Link("Developer resources", FEDREG_AIDS, "docs"),
        Link("REST API and interactive documentation", FEDREG_AIDS + "/rest-api", "guide"),
        Link("OpenAPI document", FEDREG + "/api/v1/documentation.json", "spec"),
        Link("Bulk data", FEDREG_AIDS + "/bulk-data", "guide"),
        Link("API clients", FEDREG_AIDS + "/ruby-client-gem", "sdk"),
        Link("FederalRegister.gov is open source", FEDREG_AIDS + "/federalregister-gov-is-open-source", "source"),
    ),
    areas=(
        Area(DOCUMENTS, "searches, single and multiple documents, counts by facet, an issue's table of contents",
             FEDREG_DOCS, covered="the newest 100 documents of the SEC, the CFTC, the Fed and the Treasury (title, type, "
                                  "date, link, agencies, number); FINRA's and the exchanges' rule filings tagged"),
        Area(INSPECTION, "documents on public inspection, today's and by number", FEDREG_DOCS),
        Area("Agencies", "every agency's details, or one's", FEDREG_DOCS),
        Area("Images", "an image's variants and their metadata", FEDREG_DOCS),
        Area("Suggested Searches", "the suggested searches, by FederalRegister.gov section", FEDREG_DOCS),
    ),
    calls=(
        Call("GET /documents.json", "search every document published since 1994", DOCUMENTS,
             used="the fedreg feed: the newest 100 of four agencies (conditions[agencies][], fields[])",
             docs=FEDREG_DOCS),
        Call("GET /documents/{document_number}.{format}", "one document", DOCUMENTS, docs=FEDREG_DOCS),
        Call("GET /documents/{document_numbers}.{format}", "several documents", DOCUMENTS, docs=FEDREG_DOCS),
        Call("GET /documents/facets/{facet}", "the matching documents' counts by a facet", DOCUMENTS,
             docs=FEDREG_DOCS),
        Call("GET /issues/{publication_date}.{format}", "an issue's table of contents", DOCUMENTS, docs=FEDREG_DOCS),
        Call("GET /public-inspection-documents/current.{format}", "the documents on public inspection now", INSPECTION,
             docs=FEDREG_DOCS),
        Call("GET /public-inspection-documents.{format}", "search the public inspection documents", INSPECTION,
             docs=FEDREG_DOCS),
        Call("GET /agencies", "every agency's details", "Agencies", docs=FEDREG_DOCS),
        Call("GET /agencies/{slug}", "one agency's details", "Agencies", docs=FEDREG_DOCS),
        Call("GET /images/{identifier}", "an image's variants", "Images", docs=FEDREG_DOCS),
        Call("GET /suggested_searches", "the suggested searches", "Suggested Searches", docs=FEDREG_DOCS),
    ),
    verified=VERIFIED,
)

# -- the CFTC -----------------------------------------------------------------------------------------------------------

CFTC = "https://www.cftc.gov"
COT = CFTC + "/MarketReports/CommitmentsofTraders/"
COT_FILES = COT + "HistoricalCompressed/index.htm"
COT_PRE_FAQ = "https://publicreporting.cftc.gov/stories/s/inwp-fmhz"
LEGACY = "Legacy reports, futures only"

CFTC_API = Api(
    name="CFTC Commitments of Traders",
    maker="U.S. Commodity Futures Trading Commission",
    about=("The CFTC's weekly Commitments of Traders reports: the open interest and the positions of commercial, "
           "non-commercial and small traders in each futures market (Legacy), the disaggregated and Traders in "
           "Financial Futures breakdowns and the commodity index traders' supplement, each futures only or futures and "
           "options combined. Each Tuesday's positions are released that Friday; the history is text and Excel files, "
           "one a year, and the same reports are a data API in the COT Public Reporting Environment."),
    kind="feed",
    base=CFTC,
    version="the Legacy futures-only text files (comma-delimited, zipped: 1986-2016 in one, then one a year)",
    auth="none: public files",
    limits=("none published; the plugin keeps its own: at most 30 requests a day, an hour apart at least (the dataset "
            "refreshed weekly)"),
    costs="",
    links=(
        Link("Commitments of Traders", COT + "index.htm", "docs"),
        Link("Historical compressed files", COT_FILES, "reference"),
        Link("Explanatory notes", COT + "ExplanatoryNotes/index.htm", "guide"),
        Link("About the COT reports", COT + "AbouttheCOTReports/index.htm", "guide"),
        Link("Release schedule", COT + "ReleaseSchedule/index.htm", "reference"),
        Link("COT Public Reporting Environment", "https://publicreporting.cftc.gov/stories/s/r4w3-av2u", "tool"),
        Link("COT Public Reporting Environment: questions", COT_PRE_FAQ, "guide"),
        Link("Web policy", CFTC + "/WebPolicy/index.htm", "terms"),
    ),
    areas=(
        Area(LEGACY, "open interest and the commercial, non-commercial and small traders' positions, weekly from 1986",
             COT_FILES, covered="cftc-cot-legacy: eight series a market, every week from 1986, each year's file closed "
                                "once its last report is out"),
        Area("Legacy reports, futures and options combined", "the same with options, from 1995", COT_FILES),
        Area("Disaggregated reports", "the positions by kind of trader, futures only or combined: a file a year from "
                                      "2010, 2006-2016 in one", COT_FILES),
        Area("Traders in Financial Futures", "the financial futures' positions by kind of trader: a file a year from "
                                             "2010, 2006-2016 in one", COT_FILES),
        Area("Commodity index traders supplement", "the Commodity Index Trader supplemental report, a file a year",
             COT_FILES),
        Area("Current reports", "this week's reports, long and short format, and comma delimited", COT + "index.htm"),
        Area("COT Public Reporting Environment", "the reports as datasets with a data API (Socrata: Legacy 6dca-aqww "
                                                 "and jun7-fc8e, Disaggregated 72hh-3qpy and kh3c-gbw2, TFF gpe5-46if and "
                                                 "yw9f-hn96, supplemental 4zgm-a668)", COT_PRE_FAQ),
    ),
    calls=(
        Call("GET /files/dea/history/deacot1986_2016.zip", "the Legacy futures-only reports 1986-2016", LEGACY,
             used="cftc-cot-legacy's first file (final)", docs=COT_FILES),
        Call("GET /files/dea/history/deacot{year}.zip", "a year's Legacy futures-only reports, from 2017", LEGACY,
             used="cftc-cot-legacy: one a year, final from January 15 after it", docs=COT_FILES),
        Call("GET /files/dea/history/deahistfo{year}.zip", "a year's Legacy futures-and-options reports",
             "Legacy reports, futures and options combined", docs=COT_FILES),
        Call("GET /files/dea/history/fut_disagg_txt_{year}.zip", "a year's disaggregated futures-only reports",
             "Disaggregated reports", docs=COT_FILES),
        Call("GET /files/dea/history/fut_fin_txt_{year}.zip", "a year's Traders in Financial Futures reports",
             "Traders in Financial Futures", docs=COT_FILES),
        Call("GET /files/dea/history/dea_cit_txt_{year}.zip", "a year's commodity index traders supplement",
             "Commodity index traders supplement", docs=COT_FILES),
        Call("GET /dea/newcot/f_disagg.txt", "this week's disaggregated futures-only report", "Current reports",
             docs=COT + "index.htm"),
        Call("SODA query of dataset 6dca-aqww", "the Legacy futures-only reports through the data API",
             "COT Public Reporting Environment",
             docs="https://dev.socrata.com/foundry/publicreporting.cftc.gov/6dca-aqww"),
    ),
    verified=VERIFIED,
)

AGENCY_APIS = {"fed": FED_API, "nyfed": NYFED_API, "sec": SEC_API, "bls": BLS_API, "fedreg": FEDREG_API,
               "cftc": CFTC_API}
APIS = tuple(AGENCY_APIS.values())  # the plugin's own: it reads nothing itself, its agencies' cards
