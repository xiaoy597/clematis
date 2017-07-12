# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import logging


class ExporterPipeline(object):

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
            'mysql': {'exporter': self.export_to_mysql, 'vars': {}, 'params': {}},
            'hbase': {'exporter': self.export_to_hbase, 'vars': {}, 'params': {}},
        }

    def get_col_value(self, item, col_def):
        if col_def[1] == 'string':
            return item[col_def[0]].encode('utf8')
        else:
            return item[col_def[0]]

    def process_item(self, item, spider):

        if '_data_store' not in dict(item).keys():
            return item

        data_store = item['_data_store'].split(':')[0]

        new_item = self.exporters[data_store]['exporter'](item, spider)

        return new_item

    def export_to_mysql(self, item, spider):

        if len(self.exporters['mysql']['params']) == 0:
            self.exporters['mysql']['params'] = self.crawler.settings.getdict('MYSQL_PIPELINE_PARAMS')

        for k, v in dict(item).iteritems():
            self.logger.debug("%s: %s", k, v)

        exporter_vars = self.exporters['mysql']['vars']
        exporter_params = self.exporters['mysql']['params']
        if 'cxn' not in exporter_vars:
            exporter_vars['cxn'] = MySQLdb.connect(host=exporter_params['host'], port=exporter_params['port'],
                                       user=exporter_params['user'], passwd=exporter_params['passwd'])
            exporter_vars['cxn'].autocommit(True)
            exporter_vars['cursor'] = exporter_vars['cxn'].cursor()

        sql_params = {
            'db': item['_data_store'].replace('mysql:', '').split('.')[0],
            'table_name': item['_data_store'].replace('mysql:', '').split('.')[1],
        }

        sql_params['table'] = filter(lambda t: t['table_name'] == sql_params['table_name'],
                                     exporter_params['table_list'])[0]
        sql_params['column_name_list'] = ','.join([col[0] for col in sql_params['table']['column_list']])

        sql = 'insert into %(db)s.%(table_name)s(collect_time, %(column_name_list)s)' % sql_params + ' values (%s' + \
              ', %s' * len(sql_params['table']['column_list']) + ')'

        col_val_list = [item['_collect_time'].encode('utf8')]
        col_val_list.extend([self.get_col_value(item, col) for col in sql_params['table']['column_list']])

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
            print "Moving %s to %s" % \
                  (self.image_root + os.path.sep + image['path'], target_path)
            try:
                shutil.move(self.image_root + os.path.sep + image['path'], target_path)
            except Exception as e:
                self.logger.exception("Failed to move image file to %s", target_path)

        item['image_path'] = target_path + os.path.sep + item['images'][0]['path'][5:]

        return item
