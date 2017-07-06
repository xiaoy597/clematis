# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import logging


class MySQLPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        mysql_pipeline = cls()

        mysql_pipeline.params = crawler.settings.getdict('MYSQL_PIPELINE_PARAMS')

        mysql_pipeline.logger.debug(mysql_pipeline.params)

        return mysql_pipeline

    def __init__(self):
        super(MySQLPipeline, self).__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("Instance created.")

        self.cxn = None
        self.cursor = None
        self.params = None

    def get_col_value(self, item, col_def):
        if col_def[1] == 'string':
            return item[col_def[0]].encode('utf8')
        else:
            return item[col_def[0]]

    def process_item(self, item, spider):

        if '_data_store' not in dict(item).keys() or not item['_data_store'].startswith('mysql:'):
            return item

        for k, v in dict(item).iteritems():
            self.logger.debug("%s: %s", k, v)

        if self.cxn is None:
            self.cxn = MySQLdb.connect(host=self.params['host'], port=self.params['port'],
                                       user=self.params['user'], passwd=self.params['passwd'])
            self.cxn.autocommit(True)
            self.cursor = self.cxn.cursor()

        sql_params = {
            'db': item['_data_store'].replace('mysql:', '').split('.')[0],
            'table_name': item['_data_store'].replace('mysql:', '').split('.')[1],
        }

        sql_params['table'] = filter(lambda t: t['table_name'] == sql_params['table_name'],
                                     self.params['table_list'])[0]
        sql_params['column_name_list'] = ','.join([col[0] for col in sql_params['table']['column_list']])

        sql = 'insert into %(db)s.%(table_name)s(collect_time, %(column_name_list)s)' % sql_params + ' values (%s' + \
              ', %s' * len(sql_params['table']['column_list']) + ')'

        col_val_list = [item['_collect_time'].encode('utf8')]
        col_val_list.extend([self.get_col_value(item, col) for col in sql_params['table']['column_list']])

        param = tuple(col_val_list)

        self.cursor.execute(sql, param)

        return item

