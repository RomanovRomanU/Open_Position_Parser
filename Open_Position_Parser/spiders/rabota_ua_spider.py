import scrapy
from re import sub

def clear_text(text,sub_symbol):
    return sub('[^a-zA-Zа-яА-Я]+', sub_symbol, text.strip())

class PositionSpider(scrapy.Spider):
    name = "position"
    # Now job search only for Kyiv
    REGION_ID = 1

    def __init__(self,position_name,*args,**kwargs):
        super(PositionSpider, self).__init__(*args,**kwargs)
        # Removing all unnecessary symbols
        position_name = clear_text(position_name,'+')
        start_url = '''
                    https://rabota.ua/jobsearch/vacancy_list?regionId=%s&keyWords=%s
                    ''' % (REGION_ID, position_name)
        self.start_urls = [start_url]

    def start_request(self):
        for url in self.urls:
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self,response):
        '''
        Simple test for Junior Python position

        @url https://rabota.ua/jobsearch/vacancy_list?regionId=1&keyWords=Junior+Python
        @scrapes Name Url Company Descriptio
        '''
        openings = response.css('table.f-vacancylist-tablewrap tr')
        for open_position in openings:
            name = open_position.css('h3 a::text').extract()
            href = open_position.css('h3 a::attr(href)').extract()
            company_name = open_position.css('p.f-vacancylist-companyname a::text').extract()
            description = open_position.css('p.f-vacancylist-shortdescr::text').extract()


