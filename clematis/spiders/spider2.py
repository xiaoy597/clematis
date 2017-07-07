# -*- coding: utf-8 -*-
import time
import logging
import logging.config

import scrapy
from scrapy import signals
from scrapy.exceptions import DontCloseSpider

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from hbase import Hbase
from hbase.ttypes import ColumnDescriptor, Mutation


class Spider2(scrapy.Spider):
    name = 'spider2'
    allowed_domains = []
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' + \
                 'Chrome/58.0.3029.110 Safari/537.36'

    def start_requests(self):
        self.logger.info("Processing start request")

        urls = self.params['start_page_list']

        for url in urls:
            if filter(lambda page: page['page_id'] == self.params['start_page_id'],
                      [page for page in self.params['page_list']])[0]['page_type'] == 'static':
                yield scrapy.Request(url=url, callback=self.parse_static_page,
                                     meta={'my_page_id': self.params['start_page_id']})
            else:
                yield scrapy.Request(url=url, callback=self.parse_dynamic_page,
                                     meta={"my_page_type": "dynamic", 'my_page_id': self.params['start_page_id']},
                                     dont_filter=True)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls(*args, **kwargs)
        spider._set_crawler(crawler)

        spider.crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)
        spider.crawler.signals.connect(spider.spider_close, signal=signals.spider_closed)

        logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

        spider.params = crawler.settings.getdict(spider.name.upper() + '_SPIDER_PARAMS')

        spider.logger.debug(spider.params)

        spider.logger.debug("%s is configured.", cls.__name__)

        return spider

    def __init__(self, **kwargs):
        super(Spider2, self).__init__(**kwargs)
        self.logger.debug("%s is initiated.", self.__class__.__name__)

        self.browser = None
        self.default_window = None
        self.page_num = 0
        self.request_queue = []
        self.params = None
        self.hbase_client = None
        self.page_dump_params = None
        self.page_serials = {}
        self.start_time = time.time()

    def spider_idle(self):
        self.logger.info("Spider idle signal caught.")

        stats_info = "Stats for last scrapping >>>"
        for k, v in self.crawler.stats.__dict__['_stats'].iteritems():
            stats_info += '\n' + k + ": " + str(v)

        stats_info += "\nStats for last scrapping <<<"

        self.logger.info(stats_info)

        if len(self.request_queue) > 0:
            count = 16 - len(self.browser.window_handles)
            while count > 0 and len(self.request_queue) > 0:
                req = self.request_queue.pop(0)
                self.logger.debug("Dequeuing %s", req.url)
                self.crawler.engine.crawl(req, spider=self)
                count -= 1
            raise DontCloseSpider

    def spider_close(self):
        self.logger.info("Spider close signal caught.")
        if self.browser is not None:
            self.browser.quit()

    def parse_static_page(self, response):

        crawl_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        meta = response.request.meta
        if meta is None or 'my_page_id' not in meta:
            raise Exception('Meta is missing for request ' + response.request.url)

        page_def = filter(lambda x: x['page_id'] == meta['my_page_id'], self.params['page_list'])[0]

        self.logger.debug("Parsing page " + page_def['page_name'])

        content = self.get_page_content(response, page_def)

        self.logger.debug("Page content: %s", str(content))

        new_requests = self.get_page_link(response, page_def)

        if page_def['save_page_source']:
            self.dump_page_source(page_def['page_id'], crawl_time, response.request.url, response.text)

        if page_def['data_format'] == 'table':
            rows = self.content_to_rows(content)

            self.logger.debug("Page content as rows: %s", str(rows))

            for row in rows:
                row['_collect_time'] = crawl_time
                row['_data_store'] = page_def['data_store']
                yield row

        for req in new_requests:
            yield req

    def parse_dynamic_page(self, response):

        crawl_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        meta = response.request.meta
        if meta is None or 'my_page_id' not in meta:
            raise Exception('Meta is missing for request ' + response.request.url)

        page_def = filter(lambda x: x['page_id'] == meta['my_page_id'], self.params['page_list'])[0]

        self.logger.debug("Parsing page " + page_def['page_name'])

        self.browser.switch_to.window(response.headers["handle"])

        time.sleep(2)

        try:
            WebDriverWait(self.browser, 30).until(
                EC.presence_of_element_located((By.XPATH, page_def['load_indicator'])))
        except TimeoutException as e:
            self.logger.exception("Time out for getting content from page %s", response.url)
            self.browser.close()
            yield scrapy.Request(url=response.request.url, callback=self.parse_dynamic_page,
                                 meta={"my_page_type": "dynamic", 'my_page_id': meta['my_page_id']},
                                 dont_filter=True)
            return

        new_requests = self.get_page_link(response, page_def)

        content = self.get_page_content(response, page_def,)

        if page_def['save_page_source']:
            self.dump_page_source(page_def['page_id'], crawl_time, response.request.url, self.browser.page_source)

        self.browser.close()

        if page_def['data_format'] == 'table':
            rows = self.content_to_rows(content)

            self.logger.debug("Page content as rows: %s", str(rows))

            for row in rows:
                row['_collect_time'] = crawl_time
                row['_data_store'] = page_def['data_store']
                yield row

        for req in new_requests:
            yield req

    def get_page_link(self, response, page_def):

        links = []
        request_list = []
        page_type = page_def['page_type']

        if page_type == 'static':
            for link in page_def['page_link_list']:
                try:
                    for link_element in response.xpath(link['link_locate_pattern']):
                        self.logger.debug('Find link: %s[%s]', link_element.get_attribute("href"), link_element.text)
                        links.append((link_element.get_attribute("href"), link['next_page_id']))
                except (NoSuchElementException, StaleElementReferenceException) as e:
                    self.logger.exception('No element is found from path %s', link['link_locate_pattern'])
        else:
            for link in page_def['page_link_list']:
                try:
                    for link_element in self.browser.find_elements_by_xpath(link['link_locate_pattern']):
                        self.logger.debug('Find link: %s[%s]', link_element.get_attribute("href"), link_element.text)
                        links.append((link_element.get_attribute("href"), link['next_page_id']))
                except (NoSuchElementException, StaleElementReferenceException) as e:
                    self.logger.exception('No element is found from path %s', link['link_locate_pattern'])

        # if self.page_num < 1:
        #     next_page = self.browser.find_element_by_xpath(
        #         '//div[@class="pagebox"]/span[@class="pagebox_pre"][last()]/a')
        #     next_page.click()
        #     yield scrapy.Request(self.browser.current_url, callback=self.parse_page_1, dont_filter=True,
        #                          meta={"my_page_type": "update", "my_window": self.browser.current_window_handle})

        if page_type == 'static':
            count = 32
        else:
            count = 16 - len(self.browser.window_handles)

        for link, next_page_id in links:
            next_page_def = filter(lambda x: x['page_id'] == next_page_id, self.params['page_list'])[0]
            if next_page_def['page_type'] == 'static':
                req = scrapy.Request(link, callback=self.parse_static_page,
                                     meta={"my_page_id": next_page_id}, dont_filter=True)
            else:
                req = scrapy.Request(link, callback=self.parse_dynamic_page,
                                     meta={"my_page_id": next_page_id, "my_page_type": 'dynamic'}, dont_filter=True)
            if count < 0:
                self.logger.debug("Enqueuing %s", str(link))
                self.request_queue.append(req)
            else:
                self.logger.debug("Requesting %s", str(link))
                request_list.append(req)
            count -= 1

        return request_list

    def get_page_content(self, response, page_def, current_field_list=None,
                         xpath_var_dict={}, level=1):
        content = []

        if current_field_list is None:
            current_field_list = filter(lambda x: x['parent_field_id'] == 0, page_def['page_field_list'])

        if len(current_field_list) == 0:
            return content

        element_index_var = '${FIELD_LEVEL_' + str(level) + '_INDEX}'

        if reduce(lambda x, y: x or y,
                  [element_index_var in field['field_locate_pattern'] for field in current_field_list]):
            list_index = 1
            while True:
                xpath_var_dict[element_index_var] = str(list_index)

                field_list_value = {}
                if not self.get_field_list_value(response, page_def, xpath_var_dict, field_list_value,
                                                 current_field_list, level):
                    break
                else:
                    content.append(field_list_value)

                list_index += 1
        else:
            field_list_value = {}
            self.get_field_list_value(response, page_def,
                                      xpath_var_dict, field_list_value, current_field_list, level)
            content.append(field_list_value)

        return content

    def get_field_list_value(self, response, page_def,
                             xpath_var_dict, field_list_value, current_field_list, level):
        value_count = 0
        for current_field in current_field_list:
            # field_list_value[current_field['field_name']] = []

            xpath = current_field['field_locate_pattern']
            for xpath_var in xpath_var_dict.keys():
                xpath = xpath.replace(xpath_var, xpath_var_dict[xpath_var])

            if not self.get_field_value(response, page_def, xpath_var_dict,
                                        field_list_value, current_field, xpath, level):
                self.logger.debug("No value is found for field %s.", current_field['field_name'])
            else:
                value_count += 1

        return value_count != 0

    def get_field_value(self, response, page_def, xpath_var_dict,
                        field_list_value, current_field, xpath, level):
        if page_def['page_type'] == 'static':
            field_value_elements = response.xpath(xpath)
            self.logger.debug("%s evaluated to %s", xpath, str(field_value_elements.extract()))
        else:
            if xpath.endswith('text()'):
                xpath = xpath[0:xpath.rfind('text()')-1]
            field_value_elements = self.browser.find_elements_by_xpath(xpath)
            self.logger.debug("%s evaluated to %s", xpath, str(field_value_elements))

        if field_value_elements is not None and len(field_value_elements) > 0:
            if page_def['page_type'] == 'static':
                field_value = reduce(lambda x, y: x + ' ' + y,
                                     field_value_elements.extract()).replace('\n', '').strip()
            else:
                field_value = reduce(lambda x, y: x + ' ' + y,
                                     [elem.text for elem in field_value_elements]).replace('\n', '').strip()

            field_list_value[current_field['field_name']] = \
                (field_value, self.get_page_content(
                    response,
                    page_def,
                    filter(lambda x: x['parent_field_id'] == current_field['field_id'],
                           page_def['page_field_list']),
                    xpath_var_dict, level + 1)
                 )

            return True
        else:
            return False

    def content_to_rows(self, content):
        my_rows = []
        for field_list in content:
            if len(field_list.keys()) > 1:
                row = {}
                for field_name in field_list.keys():
                    row[field_name] = field_list[field_name][0]
                my_rows.append(row)
            else:
                rows = []
                for field_name in field_list.keys():
                    rows = self.content_to_rows(field_list[field_name][1])
                    for row in rows:
                        row[field_name] = field_list[field_name][0]
                my_rows.extend(rows)
        return my_rows

    def dump_page_source(self, page_id, crawl_time, url, page):

        if self.hbase_client is None:
            self.page_dump_params = self.crawler.settings.getdict('PAGE_DUMP_PARAMS')

            transport = TTransport.TBufferedTransport(
                TSocket.TSocket(self.page_dump_params['host'], self.page_dump_params['port']))
            protocol = TBinaryProtocol.TBinaryProtocol(transport)
            self.hbase_client = Hbase.Client(protocol)
            transport.open()

        if page_id not in self.page_serials:
            self.page_serials[page_id] = 0
        else:
            self.page_serials[page_id] += 1

        row = "%d_%d_%d_%d_%d" % \
              (self.params['user_id'], self.params['job_id'], int(self.start_time), page_id, self.page_serials[page_id])

        columns = {
            'f1:url': url,
            'f1:crawl_time': crawl_time,
            'f2:page': page.encode('utf8'),
        }

        # self.logger.debug("row: %s", row)
        # self.logger.debug("columns: %s", str(columns))

        self.hbase_client.mutateRow(
            self.page_dump_params['table'], row,
            map(lambda (k, v): Mutation(column=k, value=v), columns.items()), None)

        self.logger.debug("Row %s dumped to spider_page, url=%s", row, url)

