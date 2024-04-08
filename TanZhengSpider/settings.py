# Scrapy settings for TanZhengSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "TanZhengSpider"

SPIDER_MODULES = ["TanZhengSpider.spiders"]
NEWSPIDER_MODULE = "TanZhengSpider.spiders"
MONGODB_HOST = "spider.fiang.fun"
MONGODB_PORT = 27017
MONGODB_USER = 'admin'
MONGODB_PSW = 'fiang123'
MONGODB_AUTHSOURCE = 'admin'
MONGODB_DB = 'tanzheng-spider'

REDIS_HOST="www.fiang.fun"
REDIS_PORT=6379
REDIS_PSW='fiang123'
REDIS_DB=2

LOG_LEVEL = 'INFO'
COOKIES_ENABLED = False
# Obey robots.txt rules
ROBOTSTXT_OBEY = False
# 悠悠有品账号配置
UUYP_USERNAME='19122486487'
UUYP_PASSWORD='wo195271'
# buff cookie配置
BUFF_COOKIES={
'Device-Id': '6f4da32e-350c-4ea9-b7f4-412544f9435f',
            'Timezone': 'China Standard Time',
            'Locale': 'zh_CN',
            'System-Type': 'Android',
            'Rom-Id': 'V417IR',
            'User-Agent': 'Android/761/2.51.1.202111221546/6a7220a170b1a6df/32/vivo/V2218A/V2218A/6f4da32e-350c-4ea9-b7f4-412544f9435f',
            'Product': 'V2218A',
            'App-Version': '761',
            'Screen-Size': '7.65',
            'Timestamp': '1706146155.261',
            'Locale-Supported': 'zh-Hans',
            'Build-Fingerprint': 'OnePlus/OnePlus8Pro/OnePlus8Pro:12/V417IR/2401122222:user/release-keys',
            'Network': 'WIFI/',
            'Manufacturer': 'vivo',
            'Timezone-Offset': '28800000',
            'System-Version': '32',
            'Screen-Density': '240.00',
            'Channel': 'Official',
            'Device-Id-Weak': '6a7220a170b1a6df',
            'Timezone-Offset-DST': '28800000',
            'Brand': 'vivo',
            'Rom': 'V417IR release-keys',
            'Seed': 'ac53d15ed2a73b19647d7d983e776471',
            'Model': 'V2218A',
            'Sign': 'Hello, world!',
            'App-Version-Code': '2.51.1.202111221546',
            'Resolution': '900x1600',
            'DeviceName': 'V2218A',
            'Host': 'buff.163.com',
            # Requests sorts cookies= alphabetically
            'Cookie': 'session=1-aE_-SAWUsvDfWikbowHgvDw4cJS4RfIPXs2JPr0EYfg12041475705',
        }
# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "TanZhengSpider (+http://www.yourdomain.com)"



# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 20
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en",
    'user-agent:': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/103.0.5060.134',

}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "TanZhengSpider.middlewares.TanzhengspiderSpiderMiddleware": 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    "TanZhengSpider.middlewares.TanzhengspiderDownloaderMiddleware": 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    "TanZhengSpider.pipelines.TanzhengspiderPipeline": 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
