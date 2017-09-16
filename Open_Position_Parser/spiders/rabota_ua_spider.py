# -*- coding: utf-8 -*-
import scrapy
from Open_Position_Parser.items import OpenPostion
from re import sub

RABOTA_UA_BASE = 'https://rabota.ua'
WORK_UA_BASE = 'https://www.work.ua'
REGION_ID = 1
# start_url = 'https://rabota.ua/jobsearch/vacancy_list?regionId=%s&keyWords=%s' % (REGION_ID, position_name)
# position_name = clear_text(position_name,'+')
def check_keywords_entry(text,keywords):
    occurancies = 0
    for word in keywords:
        pass

def clear_text(text,sub_symbol=' '):
    text.encode('utf-8')
    return sub('[^a-zA-Zа-яА-Яії+#]+', sub_symbol, text.strip())

rabota_ua_selectors = {
                        "openings": 'table.f-vacancylist-tablewrap tr',
                        "name": 'h3 a::text',
                        "href": 'h3 a::attr(href)',
                        "company_name": 'p.f-vacancylist-companyname a::text',
                        "description": 'p.f-vacancylist-shortdescr::text',
                        "href_base": 'https://rabota.ua'
                        
                        }
dou_ua_selectors = {
                        "openings": 'li.l-vacancy',
                        "name": 'a::text',
                        "href": 'a::attr(href)',
                        "company_name": 'a.company::text',
                        "description": 'div.sh-info::text',
                        "href_base": ''
                    }
work_ua_selectors = {
                        "openings": 'div.job-link',
                        "name": 'h2 a::text',
                        "href": 'h2 a::attr(href)',
                        "company_name": 'div span::text',
                        "description": 'p::text',
                        "href_base": 'https://www.work.ua'
                    }

selectors = {
    'rabota': rabota_ua_selectors,
    'dou': dou_ua_selectors,
    'work': work_ua_selectors
}


class PositionSpider(scrapy.Spider):
    name = "position"
    def __init__(self,start_url,selectors_type,*args,**kwargs):
        # Now job search only for Kyiv 
        super(PositionSpider, self).__init__(*args,**kwargs)
        # Removing all unnecessary symbols
        self.start_urls = [start_url]
        self.selectors_type = selectors_type
        try:
            self.selectors = selectors[selectors_type]
        except KeyError:
            raise scrapy.exceptions.CloseSpider(reason='Such website is not yet supported')

    def start_request(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url,callback=self.rabota_ua_parse)

    def parse(self,response):
        selectors = self.selectors
        result = []
        openings = response.css(selectors['openings'])
        for open_position in openings:
            position_info = OpenPostion()
            position_info['name'] = clear_text(open_position.css(selectors['name']).extract_first())
            position_info['href'] = selectors['href_base'] + open_position.css(selectors['href']).extract_first()
            position_info['company_name'] = clear_text(open_position.css(selectors['company_name']).extract_first())
            position_info['description'] = clear_text(open_position.css(selectors['description']).extract_first())
            result.append(position_info)
        return result

# scrapy crawl position -a selectors_type="rabota" -a start_url="https://rabota.ua/jobsearch/vacancy_list?regionId=1&keyWords=Junior+Python" -o result_test4.json
# scrapy crawl position -a selectors_type="dou" -a start_url="https://jobs.dou.ua/vacancies/?search=junior+python" -o result_test2.json
# scrapy crawl position -a selectors_type="work" -a start_url="https://www.work.ua/jobs-kyiv-junior+python/" -o result_test2.json