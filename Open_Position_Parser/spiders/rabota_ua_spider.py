# -*- coding: utf-8 -*-
import scrapy
from Open_Position_Parser.items import OpenPostion
from re import sub

RABOTA_UA_BASE = 'https://rabota.ua'
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



# parse_functions = {RABOTA_UA_BASE:rabota_ua_parse}
class PositionSpider(scrapy.Spider):
    name = "position"
    def __init__(self,start_url,base_url,*args,**kwargs):
        # Now job search only for Kyiv 
        super(PositionSpider, self).__init__(*args,**kwargs)
        # Removing all unnecessary symbols
        self.start_urls = [start_url]
        self.base_url = base_url

    def start_request(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url,callback=self.rabota_ua_parse)

    def parse(self,response):
        # Result is list of OpenPosition items
        result = []
        openings = response.css('table.f-vacancylist-tablewrap tr')
        for open_position in openings:
            position_info = OpenPostion()
            position_info['name'] = clear_text(open_position.css('h3 a::text').extract_first())
            position_info['href'] = RABOTA_UA_BASE + open_position.css('h3 a::attr(href)').extract_first()
            position_info['company_name'] = clear_text(open_position.css('p.f-vacancylist-companyname a::text').extract_first())
            position_info['description'] = clear_text(open_position.css('p.f-vacancylist-shortdescr::text').extract_first())
            result.append(position_info)
        return result


            


