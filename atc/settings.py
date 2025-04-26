# Scrapy settings for atc project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

# Custom output settings
from datetime import datetime as dt
from datetime import timezone
from pathlib import Path
OUTPUT_DIRECTORY = Path(
    f"./output/{dt.now(timezone.utc).strftime('%Y_%m_%d_T%H_%M_%S')}"
)
OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)

# Crawl responsibly by identifying yourself (and your website) on the user-agent
BOT_NAME = USER_AGENT = "ATC_Bot"

SPIDER_MODULES = ["atc.spiders"]
NEWSPIDER_MODULE = "atc.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32
DOWNLOAD_DELAY = 0.1
RANDOMIZE_DOWNLOAD_DELAY = True

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0'
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware': None,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': None,
    'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': None,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.ajaxcrawl.AjaxCrawlMiddleware': None,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
    'scrapy.extensions.logstats.LogStats': None,
    'scrapy.extensions.telnet.TelnetConsole': None,
    'scrapy.extensions.memusage.MemoryUsage': None,
    'scrapy.extensions.memdebug.MemoryDebugger': None,
    'scrapy.extensions.statsmailer.Statsmailer': None,
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {}

# Logging
LOG_ENABLED = True
# LOG_FILE = None
# LOG_FILE_APPEND = False
LOG_FORMAT = '%(levelname)s: %(message)s'
LOG_LEVEL = 'INFO'

# Redirects
REDIRECT_ENABLED = True
REDIRECT_MAX_TIMES = 5

# Metarefreshing
METAREFRESH_ENABLED = False

# These settings tell the engine how often it should retry failed request
# Scrapy will only retry the failed requests which return the response codes defined in RETRY_HTTP_CODES
RETRY_ENABLED = True
RETRY_TIMES = 2
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 400, 408, 429]

# CloseSpider Extension
CLOSESPIDER_TIMEOUT = 3 * 60 * 60  # 3 hours
CLOSESPIDER_TIMEOUT_NO_ITEM = 30 * 60  # 30 min
CLOSESPIDER_ERRORCOUNT = 5

# Configure feeds
# See https://docs.scrapy.org/en/latest/topics/feed-exports.html#feeds
FEEDS = {
    (OUTPUT_DIRECTORY / 'atc.csv').as_posix(): {
        'format': 'csv',
        'overwrite': True,
        'item_export_kwargs': {
            'include_headers_line': True,
            'join_multivalued': '; ',
        }
    }
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 0.1
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 1
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 12 * 60 * 60
# HTTPCACHE_DIR = 'HttpCache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
