
-- User 用户表
delete from user;
insert into user values (1, 'Test user 1', 0, '2017-07-01', 0, '2017-07-02 09:00:00');


-- crawl job 抓取任务配置表
delete from crawl_job;
insert into crawl_job values (1, 1, '新浪新闻', 1, 1, 0, 0, 1, 0, 0, 0, 'http://roll.news.sina.com.cn/s/channel.php#col=97&spec=&type=&ch=&k=&offset_page=0&offset_num=0&num=60&asc=&page=1', 1, 0);
insert into crawl_job values (2, 1, '天气预报', 1, 1, 0, 0, 1, 0, 0, 0, 'http://www.weather.com.cn/textFC/hunan.shtml', 1, 0);

-- crawl_page_config 采集页面定义表
delete from crawl_page_config;
insert into crawl_page_config values (1, 2, 1, '省级天气预报', 0, 0, 0, '', '//div[@class="hanml"]', 0, 0, 0, 'spider_data.weather');
insert into crawl_page_config values (1, 1, 1, '新浪新闻列表', 1, 0, 1, '//div[@class="pagebox"]/span[@class="pagebox_pre"][last()]/a', '//div[@class="pagebox"]', 0, 2, 0, '');
insert into crawl_page_config values (2, 1, 1, '新浪新闻页面', 0, 0, 0, '', '//h1[@id="artibodyTitle"]', 0, 0, 0, 'spider_data.sina_news');


-- page_link 页面链接表
delete from page_link;
insert into page_link values (1, 1, 1, 1, '//div[@id="d_list"]/ul/li/span[@class="c_tit"]/a', '', 2);

-- data_store 数据存储表
delete from data_store;
insert into data_store values (1, 1, 0);
insert into data_store values (2, 1, 0);

-- data_store_param 数据存储参数表
delete from data_store_param;
insert into data_store_param values (1, 1, 'host', 'localhost');
insert into data_store_param values (1, 1, 'port', '3306');
insert into data_store_param values (1, 1, 'user', 'root');
insert into data_store_param values (1, 1, 'passwd', 'root');

-- page_field 页面字段配置表
delete from page_field;
insert into page_field values (1, 1, 2, 1, 'city', 0, 0, 1);
insert into page_field values (2, 1, 2, 1, 'district', 0, 1, 1);
insert into page_field values (3, 1, 2, 1, 'day_weather', 0, 1, 1);
insert into page_field values (4, 1, 2, 1, 'day_wind', 0, 1, 1);
insert into page_field values (5, 1, 2, 1, 'max_temp', 1, 1, 1);
insert into page_field values (6, 1, 2, 1, 'night_weather', 0, 1, 1);
insert into page_field values (7, 1, 2, 1, 'night_wind', 0, 1, 1);
insert into page_field values (8, 1, 2, 1, 'min_temp', 1, 1, 1);

insert into page_field values (1, 2, 1, 1, 'title', 0, 0, 1);
insert into page_field values (2, 2, 1, 1, 'content', 0, 0, 1);

-- page_field_locate 页面字段位置表
delete from page_field_locate;
insert into page_field_locate values (1, '//div[@class="hanml"]/div[@class="conMidtab"][1]/div[@class="conMidtab3"][${FIELD_LEVEL_1_INDEX}]/table/tr[1]/td[@class="rowsPan"]', 'self-text');
insert into page_field_locate values (2, '//div[@class="hanml"]/div[@class="conMidtab"][1]/div[@class="conMidtab3"][${FIELD_LEVEL_1_INDEX}]/table/tr[${FIELD_LEVEL_2_INDEX}]/td[not(@class="rowsPan")][1]', 'text');
insert into page_field_locate values (3, '//div[@class="hanml"]/div[@class="conMidtab"][1]/div[@class="conMidtab3"][${FIELD_LEVEL_1_INDEX}]/table/tr[${FIELD_LEVEL_2_INDEX}]/td[not(@class="rowsPan")][2]', 'text');
insert into page_field_locate values (4, '//div[@class="hanml"]/div[@class="conMidtab"][1]/div[@class="conMidtab3"][${FIELD_LEVEL_1_INDEX}]/table/tr[${FIELD_LEVEL_2_INDEX}]/td[not(@class="rowsPan")][3]', 'text');
insert into page_field_locate values (5, '//div[@class="hanml"]/div[@class="conMidtab"][1]/div[@class="conMidtab3"][${FIELD_LEVEL_1_INDEX}]/table/tr[${FIELD_LEVEL_2_INDEX}]/td[not(@class="rowsPan")][4]', 'text');
insert into page_field_locate values (6, '//div[@class="hanml"]/div[@class="conMidtab"][1]/div[@class="conMidtab3"][${FIELD_LEVEL_1_INDEX}]/table/tr[${FIELD_LEVEL_2_INDEX}]/td[not(@class="rowsPan")][5]', 'text');
insert into page_field_locate values (7, '//div[@class="hanml"]/div[@class="conMidtab"][1]/div[@class="conMidtab3"][${FIELD_LEVEL_1_INDEX}]/table/tr[${FIELD_LEVEL_2_INDEX}]/td[not(@class="rowsPan")][6]', 'text');
insert into page_field_locate values (8, '//div[@class="hanml"]/div[@class="conMidtab"][1]/div[@class="conMidtab3"][${FIELD_LEVEL_1_INDEX}]/table/tr[${FIELD_LEVEL_2_INDEX}]/td[not(@class="rowsPan")][7]', 'text');

insert into page_field_locate values (101, '//h1[@id="artibodyTitle"]', 'self-text');
insert into page_field_locate values (102, '//div[@id="artibody"]//p', 'text');

-- page_field_locate_relation 页面字段与位置关系表
delete from page_field_locate_relation;
insert into page_field_locate_relation values (1, 1, 2, 1, 1);
insert into page_field_locate_relation values (2, 1, 2, 1, 2);
insert into page_field_locate_relation values (3, 1, 2, 1, 3);
insert into page_field_locate_relation values (4, 1, 2, 1, 4);
insert into page_field_locate_relation values (5, 1, 2, 1, 5);
insert into page_field_locate_relation values (6, 1, 2, 1, 6);
insert into page_field_locate_relation values (7, 1, 2, 1, 7);
insert into page_field_locate_relation values (8, 1, 2, 1, 8);

insert into page_field_locate_relation values (1, 2, 1, 1, 101);
insert into page_field_locate_relation values (2, 2, 1, 1, 102);

-- job_schedule 任务调度表
delete from job_schedule;
insert into job_schedule values (0, 0);

-- job_schedule_param 任务调度参数表
delete from job_schedule_param;
insert into job_schedule_param values (0, 'time', '');

