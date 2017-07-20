
-- User 用户表
delete from user;
insert into user values (1, 'Test user 1', 0, '2017-07-01', 0, '2017-07-02 09:00:00');


-- crawl job 抓取任务配置表
delete from crawl_job;
insert into crawl_job values (1, 1, '新浪新闻', 1, 1, 0, 0, 1, 0, 0, 0, 'http://roll.news.sina.com.cn/s/channel.php#col=97&spec=&type=&ch=&k=&offset_page=0&offset_num=0&num=60&asc=&page=1', 1, 0);
insert into crawl_job values (2, 1, '天气预报', 1, 1, 0, 0, 1, 0, 0, 0, 'http://www.weather.com.cn/textFC/hunan.shtml', 1, 0);
insert into crawl_job values (3, 1, '新浪图片', 1, 1, 0, 0, 1, 0, 0, 0, 'http://slide.sports.sina.com.cn/', 1, 0);
insert into crawl_job values (4, 1, '新浪股票', 1, 1, 0, 0, 1, 0, 0, 0, 'http://finance.sina.com.cn/realstock/company/sz000651/nc.shtml', 1, 0);

-- crawl_page_config 采集页面定义表
delete from crawl_page_config;
insert into crawl_page_config values (1, 1, 1, '新浪新闻列表', 1, 0, 1, '//div[@class="pagebox"]/span[@class="pagebox_pre"][last()]/a', '//div[@class="pagebox"]', 0, 2, 0, '');
insert into crawl_page_config values (2, 1, 1, '新浪新闻页面', 0, 0, 0, '', '//h1[@id="artibodyTitle"]', 0, 0, 0, 'spider_data.sina_news');

insert into crawl_page_config values (1, 2, 1, '省级天气预报', 0, 0, 0, '', '//div[@class="hanml"]', 0, 0, 0, 'spider_data.weather');

insert into crawl_page_config values (1, 3, 1, '新浪图片列表', 1, 0, 1, '//span[@class="pagination"]/a[@class="next"]', '//span[@class="pagination"]/a[@class="next"]', 0, 2, 0, '');
insert into crawl_page_config values (2, 3, 1, '新浪图片页面', 1, 0, 0, '', '//div[@slide-type="title"]/h2', 0, 0, 0, 'spider_data.sina_image');
insert into crawl_page_config values (1, 4, 1, '新浪股票行情', 1, 0, 1, '', '//h1[@id="stockName"]', 2, 10, 0, 'spider_data.stock_price');


-- page_link 页面链接表
delete from page_link;
insert into page_link values (1, 1, 1, 1, '//div[@id="d_list"]/ul/li/span[@class="c_tit"]/a', '', 2);
insert into page_link values (1, 1, 3, 1, '//div[@node-type="items"]//div[@class="bd"]//a', '', 2);

-- data_store 数据存储表
delete from data_store;
insert into data_store values (1, 1, 0);

-- data_store_param 数据存储参数表
delete from data_store_param;
insert into data_store_param values (1, 1, 'host', 'localhost');
insert into data_store_param values (1, 1, 'port', '3306');
insert into data_store_param values (1, 1, 'user', 'root');
insert into data_store_param values (1, 1, 'passwd', 'root');

-- page_field 页面字段配置表
delete from page_field;

-- 新浪新闻
insert into page_field values (1, 2, 1, 1, 'title', 0, 0, 1);
insert into page_field values (2, 2, 1, 1, 'content', 0, 0, 1);

-- 天气预报
insert into page_field values (1, 1, 2, 1, 'city', 0, 0, 1);
insert into page_field values (2, 1, 2, 1, 'district', 0, 1, 1);
insert into page_field values (3, 1, 2, 1, 'day_weather', 0, 1, 1);
insert into page_field values (4, 1, 2, 1, 'day_wind', 0, 1, 1);
insert into page_field values (5, 1, 2, 1, 'max_temp', 1, 1, 1);
insert into page_field values (6, 1, 2, 1, 'night_weather', 0, 1, 1);
insert into page_field values (7, 1, 2, 1, 'night_wind', 0, 1, 1);
insert into page_field values (8, 1, 2, 1, 'min_temp', 1, 1, 1);

-- 新浪图片
insert into page_field values (1, 2, 3, 1, 'title', 0, 0, 1);
insert into page_field values (2, 2, 3, 1, 'description', 0, 1, 0);
insert into page_field values (3, 2, 3, 1, 'image_url', 0, 1, 0);
insert into page_field values (4, 2, 3, 1, 'image_path', 0, 1, 0);

-- 新浪股票行情
insert into page_field values (1, 1, 4, 1, 'stock_name', 0, 0, 1);
insert into page_field values (2, 1, 4, 1, 'stock_id', 0, 0, 1);
insert into page_field values (3, 1, 4, 1, 'stock_time', 0, 0, 1);
insert into page_field values (4, 1, 4, 1, 'stock_price', 1, 0, 1);
insert into page_field values (5, 1, 4, 1, 'stock_open_price', 1, 0, 1);
insert into page_field values (6, 1, 4, 1, 'stock_deal_num', 0, 0, 1);
insert into page_field values (7, 1, 4, 1, 'stock_high_price', 1, 0, 1);
insert into page_field values (8, 1, 4, 1, 'stock_deal_amt', 0, 0, 1);
insert into page_field values (9, 1, 4, 1, 'stock_exch_rate', 0, 0, 1);
insert into page_field values (10, 1, 4, 1, 'stock_low_price', 1, 0, 1);
insert into page_field values (11, 1, 4, 1, 'stock_total_value', 0, 0, 1);
insert into page_field values (12, 1, 4, 1, 'stock_pb', 0, 0, 1);
insert into page_field values (13, 1, 4, 1, 'stock_close_price', 1, 0, 1);
insert into page_field values (14, 1, 4, 1, 'stock_currency_value', 0, 0, 1);
insert into page_field values (15, 1, 4, 1, 'stock_pe', 0, 0, 1);

-- page_field_locate 页面字段位置表
delete from page_field_locate;

insert into page_field_locate values (101, '//h1[@id="artibodyTitle"]', 'self-text');
insert into page_field_locate values (102, '//div[@id="artibody"]//p', 'text');

insert into page_field_locate values (201, '//div[@class="hanml"]/div[@class="conMidtab"][1]/div[@class="conMidtab3"][${FIELD_LEVEL_1_INDEX}]/table/tr[1]/td[@class="rowsPan"]', 'self-text');
insert into page_field_locate values (202, '//div[@class="hanml"]/div[@class="conMidtab"][1]/div[@class="conMidtab3"][${FIELD_LEVEL_1_INDEX}]/table/tr[${FIELD_LEVEL_2_INDEX}]/td[not(@class="rowsPan")][1]', 'text');
insert into page_field_locate values (203, '//div[@class="hanml"]/div[@class="conMidtab"][1]/div[@class="conMidtab3"][${FIELD_LEVEL_1_INDEX}]/table/tr[${FIELD_LEVEL_2_INDEX}]/td[not(@class="rowsPan")][2]', 'text');
insert into page_field_locate values (204, '//div[@class="hanml"]/div[@class="conMidtab"][1]/div[@class="conMidtab3"][${FIELD_LEVEL_1_INDEX}]/table/tr[${FIELD_LEVEL_2_INDEX}]/td[not(@class="rowsPan")][3]', 'text');
insert into page_field_locate values (205, '//div[@class="hanml"]/div[@class="conMidtab"][1]/div[@class="conMidtab3"][${FIELD_LEVEL_1_INDEX}]/table/tr[${FIELD_LEVEL_2_INDEX}]/td[not(@class="rowsPan")][4]', 'text');
insert into page_field_locate values (206, '//div[@class="hanml"]/div[@class="conMidtab"][1]/div[@class="conMidtab3"][${FIELD_LEVEL_1_INDEX}]/table/tr[${FIELD_LEVEL_2_INDEX}]/td[not(@class="rowsPan")][5]', 'text');
insert into page_field_locate values (207, '//div[@class="hanml"]/div[@class="conMidtab"][1]/div[@class="conMidtab3"][${FIELD_LEVEL_1_INDEX}]/table/tr[${FIELD_LEVEL_2_INDEX}]/td[not(@class="rowsPan")][6]', 'text');
insert into page_field_locate values (208, '//div[@class="hanml"]/div[@class="conMidtab"][1]/div[@class="conMidtab3"][${FIELD_LEVEL_1_INDEX}]/table/tr[${FIELD_LEVEL_2_INDEX}]/td[not(@class="rowsPan")][7]', 'text');

insert into page_field_locate values (301, '//div[@slide-type="title"]/h2', 'text');
insert into page_field_locate values (302, '//div[@id="eData"]/dl/dd[5]', 'text');
insert into page_field_locate values (303, '//li[@slide-type="item"]//img', '@src');
insert into page_field_locate values (304, '//li[@slide-type="item"]/div[@slide-type="bigWrap" and @data-src!=""]', '@data-src');


insert into page_field_locate values (401, '//h1[@id="stockName"]', 'self-text');
insert into page_field_locate values (402, '//h1[@id="stockName"]/span', 'text');
insert into page_field_locate values (403, '//*[@id="hqTime"]', 'text');
insert into page_field_locate values (404, '//*[@id="price"]', 'text');
insert into page_field_locate values (405, '//div[@id="hqDetails"]/table/tbody/tr[1]/td[1]', 'text');
insert into page_field_locate values (406, '//div[@id="hqDetails"]/table/tbody/tr[1]/td[2]', 'text');
insert into page_field_locate values (407, '//div[@id="hqDetails"]/table/tbody/tr[2]/td[1]', 'text');
insert into page_field_locate values (408, '//div[@id="hqDetails"]/table/tbody/tr[2]/td[2]', 'text');
insert into page_field_locate values (409, '//div[@id="hqDetails"]/table/tbody/tr[2]/td[3]', 'text');
insert into page_field_locate values (410, '//div[@id="hqDetails"]/table/tbody/tr[3]/td[1]', 'text');
insert into page_field_locate values (411, '//div[@id="hqDetails"]/table/tbody/tr[3]/td[2]', 'text');
insert into page_field_locate values (412, '//div[@id="hqDetails"]/table/tbody/tr[3]/td[3]', 'text');
insert into page_field_locate values (413, '//div[@id="hqDetails"]/table/tbody/tr[4]/td[1]', 'text');
insert into page_field_locate values (414, '//div[@id="hqDetails"]/table/tbody/tr[4]/td[2]', 'text');
insert into page_field_locate values (415, '//div[@id="hqDetails"]/table/tbody/tr[4]/td[3]', 'text');

-- Special field locate used by the fields that don't get value from page.
insert into page_field_locate values (0, '/NULL', 'text');

-- page_field_locate_relation 页面字段与位置关系表
delete from page_field_locate_relation;

insert into page_field_locate_relation values (1, 2, 1, 1, 101);
insert into page_field_locate_relation values (2, 2, 1, 1, 102);

insert into page_field_locate_relation values (1, 1, 2, 1, 201);
insert into page_field_locate_relation values (2, 1, 2, 1, 202);
insert into page_field_locate_relation values (3, 1, 2, 1, 203);
insert into page_field_locate_relation values (4, 1, 2, 1, 204);
insert into page_field_locate_relation values (5, 1, 2, 1, 205);
insert into page_field_locate_relation values (6, 1, 2, 1, 206);
insert into page_field_locate_relation values (7, 1, 2, 1, 207);
insert into page_field_locate_relation values (8, 1, 2, 1, 208);

insert into page_field_locate_relation values (1, 2, 3, 1, 301);
insert into page_field_locate_relation values (2, 2, 3, 1, 302);
insert into page_field_locate_relation values (3, 2, 3, 1, 303);
insert into page_field_locate_relation values (3, 2, 3, 1, 304);
insert into page_field_locate_relation values (4, 2, 3, 1, 0);

insert into page_field_locate_relation values (1, 1, 4, 1, 401);
insert into page_field_locate_relation values (2, 1, 4, 1, 402);
insert into page_field_locate_relation values (3, 1, 4, 1, 403);
insert into page_field_locate_relation values (4, 1, 4, 1, 404);
insert into page_field_locate_relation values (5, 1, 4, 1, 405);
insert into page_field_locate_relation values (6, 1, 4, 1, 406);
insert into page_field_locate_relation values (7, 1, 4, 1, 407);
insert into page_field_locate_relation values (8, 1, 4, 1, 408);
insert into page_field_locate_relation values (9, 1, 4, 1, 409);
insert into page_field_locate_relation values (10, 1, 4, 1, 410);
insert into page_field_locate_relation values (11, 1, 4, 1, 411);
insert into page_field_locate_relation values (12, 1, 4, 1, 412);
insert into page_field_locate_relation values (13, 1, 4, 1, 413);
insert into page_field_locate_relation values (14, 1, 4, 1, 414);
insert into page_field_locate_relation values (15, 1, 4, 1, 415);

-- job_schedule 任务调度表
delete from job_schedule;
insert into job_schedule values (0, 0);

-- job_schedule_param 任务调度参数表
delete from job_schedule_param;
insert into job_schedule_param values (0, 'time', '');

