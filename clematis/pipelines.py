# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import logging
from clematis.const import SPIDER_FIELD_TYPE_STRING


class ExporterPipeline(object):
    data_store_type = ['mysql', 'hbase']

    @classmethod
    def from_crawler(cls, crawler):
        exporter_pipeline = cls()
        exporter_pipeline.crawler = crawler

        # exporter_pipeline.logger.debug(exporter_pipeline.params)

        return exporter_pipeline

    def __init__(self):
        super(ExporterPipeline, self).__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("Instance created.")

        self.crawler = None

        self.exporters = {
            'mysql': {'exporter': self.export_to_mysql, 'vars': {}},
            'hbase': {'exporter': self.export_to_hbase, 'vars': {}},
        }

    def get_field_value(self, item, field):
        if field['field_datatype'] == SPIDER_FIELD_TYPE_STRING:
            return item[field['field_name']].encode('utf8')
        else:
            return item[field['field_name']]

    def process_item(self, item, spider):

        if '_page_id' not in dict(item).keys():
            return item

        data_store = self.data_store_type[spider.params['data_store']['data_store_type']]

        new_item = self.exporters[data_store]['exporter'](item, spider)

        return new_item

    def export_to_mysql(self, item, spider):

        for k, v in dict(item).iteritems():
            self.logger.debug("%s: %s", k, v)

        exporter_vars = self.exporters['mysql']['vars']
        exporter_params = spider.params['data_store']
        if 'cxn' not in exporter_vars:
            exporter_vars['cxn'] = MySQLdb.connect(host=exporter_params['host'], port=int(exporter_params['port']),
                                                   user=exporter_params['user'], passwd=exporter_params['passwd'],
                                                   charset='utf8')
            exporter_vars['cxn'].autocommit(True)
            exporter_vars['cursor'] = exporter_vars['cxn'].cursor()

        page_def = filter(lambda x: x['page_id'] == item['_page_id'], spider.params['pages'])[0]

        sql_params = {
            'db': page_def['data_file'].split('.')[0],
            'table_name': page_def['data_file'].split('.')[1],
            'column_name_list': ','.join([c['field_name'] for c in page_def['fields']]),
        }

        sql = 'insert into %(db)s.%(table_name)s (collect_time, %(column_name_list)s)' % sql_params + ' values (%s' + \
              ', %s' * len(page_def['fields']) + ')'

        col_val_list = [item['_collect_time'].encode('utf8')]
        col_val_list.extend([self.get_field_value(item, field) for field in page_def['fields']])

        param = tuple(col_val_list)

        exporter_vars['cursor'].execute(sql, param)

        return item

    def export_to_hbase(self, item, spider):
        return item


import os
import shutil


class ImagePreProcessPipeline(object):
    def __init__(self):
        super(ImagePreProcessPipeline, self).__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("Instance created.")

        self.image_root = None
        self.crawler = None

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        pipeline.crawler = crawler

        return pipeline

    def process_item(self, item, spider):
        if 'image_url' in item:
            item['image_urls'] = [item['image_url']]
        return item


class ImagePostProcessPipeline(object):
    def __init__(self):
        super(ImagePostProcessPipeline, self).__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("Instance created.")

        self.image_root = None
        self.crawler = None

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        pipeline.crawler = crawler

        # exporter_pipeline.logger.debug(exporter_pipeline.params)
        pipeline.image_root = crawler.settings.get("IMAGES_STORE")

        return pipeline

    def process_item(self, item, spider):

        if 'image_urls' not in item or 'title' not in item:
            return item

        slide_title = item['title'].replace('"', u'“')
        slide_title = slide_title.replace(':', u'：')
        slide_title = slide_title.replace('|', u'——')
        slide_title = slide_title.replace('?', u'？')
        slide_title = slide_title.replace('<', u'《')
        slide_title = slide_title.replace('>', u'》')
        slide_title = slide_title.replace('*', u'×')
        slide_title = slide_title.replace('/', '_')
        slide_title = slide_title.replace('\\', '_')

        target_path = self.image_root + os.path.sep + slide_title
        if not os.path.exists(target_path):
            os.mkdir(target_path)

        for image in item['images']:
            self.logger.debug("Moving %s to %s", self.image_root + os.path.sep + image['path'], target_path)
            try:
                shutil.move(self.image_root + os.path.sep + image['path'], target_path)
            except Exception as e:
                self.logger.exception("Failed to move image file to %s", target_path)

        item['image_path'] = target_path + os.path.sep + item['images'][0]['path'][5:]

        return item
