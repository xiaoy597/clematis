# -*- coding: utf-8 -*-

# Scrapy settings for test1 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html


BOT_NAME = 'clematis'

SPIDER_MODULES = ['clematis.spiders']
NEWSPIDER_MODULE = 'clematis.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'test1 (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 12

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'test1.middlewares.Test1SpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'clematis.middlewares.BrowserDownloaderMiddleware': 999,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'clematis.pipelines.MySQLPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
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
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

LOG_ENABLED = False

MYSQL_PIPELINE_PARAMS = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'passwd': 'root',
    'db': 'spider_data',
    'table_list': [
        {
            'table_name': 'weather',
            'column_list': [
                ('city', 'string'),
                ('district', 'string'),
                ('day_weather', 'string'),
                ('day_wind', 'string'),
                ('max_temp', 'number'),
                ('night_weather', 'string'),
                ('night_wind', 'string'),
                ('min_temp', 'number')
            ]
        },
        {
            'table_name': 'sina_news',
            'column_list': [
                ('title', 'string'),
                ('content', 'string'),
            ],
        },
    ]
}

WEATHER_SPIDER_PARAMS = {
    'start_page_list': [
        # 'http://www.weather.com.cn/textFC/beijing.shtml',
        # 'http://www.weather.com.cn/textFC/hunan.shtml',
        # 'http://www.weather.com.cn/textFC/guangdong.shtml',
        'http://roll.news.sina.com.cn/s/channel.php#col=97&spec=&type=&ch=&k=&offset_page=0&offset_num=0&num=60&asc=&page=1',
    ],
    'start_page_id': 10,
    'page_list': [
        {
            'page_id': 1,
            'page_name': u'省级天气预报',
            'page_type': 'static',
            'data_format': 'table',
            'data_store': 'mysql:spider_data.weather',
            'is_multi_page': False,
            'load_indicator': r'//div[@class="hanml"]',
            'page_link_list': [
            ],
            'page_field_list': [
                {
                    'field_id': 1,
                    'field_name': 'city',
                    'field_data_type': 'string',
                    'parent_field_id': 0,
                    'field_level': 1,
                    'field_locate_pattern': r'//div[@class="hanml"]/div[@class="conMidtab"][1]/div[@class="conMidtab3"][${FIELD_LEVEL_1_INDEX}]/table/tr[1]/td[@class="rowsPan"]/text()',
                    'field_extract_pattern': ''
                },
                {
                    'field_id': 2,
                    'field_name': 'district',
                    'field_data_type': 'string',
                    'parent_field_id': 1,
                    'field_level': 2,
                    'field_locate_pattern': r'//div[@class="hanml"]/div[@class="conMidtab"][1]/div[@class="conMidtab3"][${FIELD_LEVEL_1_INDEX}]/table/tr[${FIELD_LEVEL_2_INDEX}]/td[not(@class="rowsPan")][1]//text()',
                    'field_extract_pattern': ''
                },
                {
                    'field_id': 3,
                    'field_name': 'day_weather',
                    'field_data_type': 'string',
                    'parent_field_id': 1,
                    'field_level': 2,
                    'field_locate_pattern': r'//div[@class="hanml"]/div[@class="conMidtab"][1]/div[@class="conMidtab3"][${FIELD_LEVEL_1_INDEX}]/table/tr[${FIELD_LEVEL_2_INDEX}]/td[not(@class="rowsPan")][2]//text()',
                    'field_extract_pattern': ''
                },
                {
                    'field_id': 4,
                    'field_name': 'day_wind',
                    'field_data_type': 'string',
                    'parent_field_id': 1,
                    'field_level': 2,
                    'field_locate_pattern': r'//div[@class="hanml"]/div[@class="conMidtab"][1]/div[@class="conMidtab3"][${FIELD_LEVEL_1_INDEX}]/table/tr[${FIELD_LEVEL_2_INDEX}]/td[not(@class="rowsPan")][3]//text()',
                    'field_extract_pattern': ''
                },
                {
                    'field_id': 5,
                    'field_name': 'max_temp',
                    'field_data_type': 'number',
                    'parent_field_id': 1,
                    'field_level': 2,
                    'field_locate_pattern': r'//div[@class="hanml"]/div[@class="conMidtab"][1]/div[@class="conMidtab3"][${FIELD_LEVEL_1_INDEX}]/table/tr[${FIELD_LEVEL_2_INDEX}]/td[not(@class="rowsPan")][4]//text()',
                    'field_extract_pattern': ''
                },
                {
                    'field_id': 6,
                    'field_name': 'night_weather',
                    'field_data_type': 'string',
                    'parent_field_id': 1,
                    'field_level': 2,
                    'field_locate_pattern': r'//div[@class="hanml"]/div[@class="conMidtab"][1]/div[@class="conMidtab3"][${FIELD_LEVEL_1_INDEX}]/table/tr[${FIELD_LEVEL_2_INDEX}]/td[not(@class="rowsPan")][5]//text()',
                    'field_extract_pattern': ''
                },
                {
                    'field_id': 7,
                    'field_name': 'night_wind',
                    'field_data_type': 'string',
                    'parent_field_id': 1,
                    'field_level': 2,
                    'field_locate_pattern': r'//div[@class="hanml"]/div[@class="conMidtab"][1]/div[@class="conMidtab3"][${FIELD_LEVEL_1_INDEX}]/table/tr[${FIELD_LEVEL_2_INDEX}]/td[not(@class="rowsPan")][6]//text()',
                    'field_extract_pattern': ''
                },
                {
                    'field_id': 8,
                    'field_name': 'min_temp',
                    'field_data_type': 'number',
                    'parent_field_id': 1,
                    'field_level': 2,
                    'field_locate_pattern': r'//div[@class="hanml"]/div[@class="conMidtab"][1]/div[@class="conMidtab3"][${FIELD_LEVEL_1_INDEX}]/table/tr[${FIELD_LEVEL_2_INDEX}]/td[not(@class="rowsPan")][7]//text()',
                    'field_extract_pattern': ''
                },
            ]

        },
        {
            'page_id': 10,
            'page_name': u'新浪新闻滚动列表',
            'page_type': 'dynamic',
            'data_format': 'table',
            'is_multi_page': True,
            'load_indicator': r'//div[@class="pagebox"]',
            'page_link_list': [
                {
                    'link_id': 1,
                    'next_page_id': 11,
                    'link_locate_pattern': r'//div[@id="d_list"]/ul/li/span[@class="c_tit"]/a',
                },
            ],
            'page_field_list': [
            ]
        },
        {
            'page_id': 11,
            'page_name': u'新浪新闻',
            'page_type': 'static',
            'data_format': 'table',
            'data_store': 'mysql:spider_data.sina_news',
            'is_multi_page': False,
            'load_indicator': r'//h1[@id="artibodyTitle"]',
            'page_link_list': [
            ],
            'page_field_list': [
                {
                    'field_id': 1,
                    'field_name': 'title',
                    'field_data_type': 'string',
                    'parent_field_id': 0,
                    'field_level': 1,
                    'field_locate_pattern': r'//h1[@id="artibodyTitle"]/text()',
                    'field_extract_pattern': ''
                },
                {
                    'field_id': 2,
                    'field_name': 'content',
                    'field_data_type': 'string',
                    'parent_field_id': 0,
                    'field_level': 1,
                    'field_locate_pattern': r'//div[@id="artibody"]/p//text()',
                    'field_extract_pattern': ''
                },
            ]
        },

    ],

}
