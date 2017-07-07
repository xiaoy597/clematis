# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import time
import logging
from scrapy import signals
from scrapy.http import Response
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchWindowException
from scrapy.exceptions import IgnoreRequest


class TestSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class BrowserDownloaderMiddleware(object):
    def __init__(self):
        super(BrowserDownloaderMiddleware, self).__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("Instance created.")

    def process_request(self, request, spider):

        self.logger.debug(request.meta)

        if request.meta is None or "my_page_type" not in request.meta:
            self.logger.debug("Skipped request %s" % request.url)
            return None

        self.logger.debug("Process request %s for spider %s", request.url, spider.name)

        if request.meta['my_page_type'] == 'update':
            return Response(str(request.url), headers={"handle": request.meta['my_window']},
                            request=request)

        if spider.browser is None:
            spider.browser = webdriver.Firefox()
            spider.default_window = spider.browser.current_window_handle

        previous_windows = spider.browser.window_handles

        spider.browser.switch_to.window(spider.default_window)

        count = 0
        while count < 3:
            try:
                self.logger.debug("Opening " + request.url)
                spider.browser.execute_script('''window.open("%s");''' % request.url)
            except NoSuchWindowException as e:
                self.logger.debug("%s is caught, try again ..." % e.__class__.__name__)
                self.logger.debug(e.stacktrace)
                time.sleep(1)
                count += 1
            else:
                self.logger.debug("Waiting for new window to be opened %s ..." % time.ctime(time.time()))
                WebDriverWait(spider.browser, 10).until(EC.new_window_is_opened)
                self.logger.debug("New window may be opened at %s." % time.ctime(time.time()))

                if len(spider.browser.window_handles) > len(previous_windows):
                    break
                else:
                    self.logger.debug("New window is not found, keep on waiting ...")
                    time.sleep(1)
                    count += 1

        if count == 3:
            self.logger.warning("Browser failed to open new window for %s, reschedule the request." % request.url)
            spider.link_queue.append(request)
            return IgnoreRequest

        current_windows = spider.browser.window_handles

        # print "old windows = " + str(previous_windows)
        # print "new windows = " + str(current_windows)

        for w in current_windows:
            if w not in previous_windows:
                spider.browser.switch_to.window(w)
                break

        new_window = spider.browser.current_window_handle

        self.logger.debug("%s opened in window %s" % (request.url, new_window))

        return Response(str(spider.browser.current_url), headers={"handle": new_window},
                        request=request)
