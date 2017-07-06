# -*- coding: utf-8 -*-
import logging
import logging.config
import scrapy
from scrapy import signals
from selenium import webdriver
from threading import current_thread, Lock
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from scrapy.exceptions import DontCloseSpider
import time

class Spider1Spider(scrapy.Spider):
    name = 'spider1'
    allowed_domains = ['sina.com.cn']
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' + \
                 'Chrome/58.0.3029.110 Safari/537.36'

    def start_requests(self):
        print "Start request in thread %s" % current_thread().name
        urls = [
            'http://roll.news.sina.com.cn/s/channel.php#col=97&spec=&type=&ch=&k=&offset_page=0&offset_num=0&num=60&asc=&page=1'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_page_1,
                                 meta={"my_page_type": "dynamic"}, dont_filter=True)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls(*args, **kwargs)
        spider._set_crawler(crawler)

        spider.crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)
        spider.crawler.signals.connect(spider.spider_close, signal=signals.spider_closed)

        logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

        spider.logger.debug("%s is configured.", cls.__name__)
        return spider

    def __init__(self, **kwargs):
        super(Spider1Spider, self).__init__(**kwargs)
        self.logger.debug("%s is initiated.", self.__class__.__name__)

        self.browser = webdriver.Firefox()
        self.default_window = self.browser.current_window_handle
        self.lock = Lock()
        self.page_num = 0
        self.link_queue = []

    def spider_idle(self):
        self.logger.info("Spider idle signal caught.")

        stats_info = "Stats for last scrapping >>>"
        for k, v in self.crawler.stats.__dict__['_stats'].iteritems():
            stats_info += '\n' + k + ": " + str(v)

        stats_info += "\nStats for last scrapping <<<"

        self.logger.info(stats_info)

        if len(self.link_queue) > 0:
            count = 16 - len(self.browser.window_handles)
            while count > 0 and len(self.link_queue) > 0:
                req = self.link_queue.pop(0)
                self.logger.debug("Dequeuing %s", req.url)
                self.crawler.engine.crawl(req, spider=self)
                count -= 1
            raise DontCloseSpider

    def spider_close(self):
        self.logger.info("Spider close signal caught.")
        self.browser.quit()

    def parse_page_1(self, response):

        self.page_num += 1

        self.browser.switch_to.window(response.headers["handle"])
        time.sleep(2)

        links = []

        while True:
            try:
                for link in self.browser.find_elements_by_xpath(
                        '//div[@id="d_list"]/ul/li/span[@class="c_tit"]/a'):
                    self.logger.debug(link.text + " :[" + link.get_attribute("href") + "]")
                    links.append(link.get_attribute("href"))

            except (NoSuchElementException, StaleElementReferenceException) as e:
                print e
                time.sleep(1)
            else:
                break

        if self.page_num < 1:
            next_page = self.browser.find_element_by_xpath(
                '//div[@class="pagebox"]/span[@class="pagebox_pre"][last()]/a')
            next_page.click()
            yield scrapy.Request(self.browser.current_url, callback=self.parse_page_1, dont_filter=True,
                                 meta={"my_page_type": "update", "my_window": self.browser.current_window_handle})

        count = 16 - len(self.browser.window_handles)
        for link in links:
            req = scrapy.Request(link, callback=self.parse_page_2, meta={"my_page_type": "dynamic"}, dont_filter=True)
            if count < 0:
                self.logger.debug("Enqueuing %s", link)
                self.link_queue.append(req)
            else:
                self.logger.debug("Requesting %s", link)
                yield req
            count -= 1

    def parse_page_2(self, response):

        self.logger.debug("Parsing response for request %s", response.request.url)

        self.browser.switch_to.window(response.headers["handle"])
        time.sleep(2)

        try:
            WebDriverWait(self.browser, 30).until(
                EC.presence_of_element_located((By.XPATH, '//h1[@id="artibodyTitle"]')))
        except TimeoutException as e:
            self.logger.exception("Time out for getting content from page %s, try again.", response.url)
            self.browser.close()
            yield response.request

        page = self.browser.page_source

        try:
            title = self.browser.find_element_by_xpath('//h1[@id="artibodyTitle"]').text
            body = '\n'.join(map(lambda x: x.text,
                                 self.browser.find_elements_by_xpath('//div[@id="artibody"]/p')))
        except NoSuchElementException as e:
            self.logger.exception("Expected element not found!")
            title = ""
            body = ""
        else:
            self.logger.debug("Page " + title + " disposed.")

        self.browser.close()

        yield {
            "title": title,
            "body": body,
            "page": page,
        }
