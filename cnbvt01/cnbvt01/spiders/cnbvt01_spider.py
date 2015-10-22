# -*- coding: utf-8 -*-
import scrapy

from cnbvt01.items import Cnbvt01Item
# for errors
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError
from twisted.web._newclient import ResponseNeverReceived

class Cnbvt01Spider(scrapy.Spider):
    name = "cnbvt01"
    allowed_domains = ["lt.morningstar.com"]
    start_urls = [
        "http://lt.morningstar.com/7ap7omrzjm/fundquickrank/default.aspx",
    ]
    #download_delay = 1    #The amount of time (in secs) that the downloader should wait before downloading consecutive pages from the same website. (default: 0)
    download_timeout = 360    #The amount of time (in secs) that the downloader will wait before timing out. (default: 180)
    download_maxsize = 0    #The maximum response size (in bytes) that downloader will download. If you want to disable it set to 0. (default: 1073741824 (1024MB))
    handle_httpstatus_list = [500, 501, 502, 503, 504, 505, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417]

    def parse(self, response):
        ## --- Log --- ##
        #self.logger.info(' --- [0] Inicio')
        ## --- Log --- ##
        # Send initial form values and start fund parsing per page
        #page_number = 142
        #while page_number >= 1:
        yield scrapy.FormRequest.from_response(
            response,
            formdata={'__EVENTTARGET': 'ctl00$ContentPlaceHolder1$aFundQuickrankControl$AspNetPager', '__EVENTARGUMENT': '1'},
            #formdata={'__EVENTTARGET': 'ctl00$ContentPlaceHolder1$aFundQuickrankControl$ddlPageSize', '__EVENTARGUMENT': '500', 'ctl00_ContentPlaceHolder1_aFundQuickrankControl_ddlPageSize': "500"},
            priority=2,
            callback=self.parse_page_funds,
            #callback=self.parse_funds_list,
            meta={'page_number': '1', 'dont_cache': True},
            #meta={'dont_cache': True},
            dont_filter=True,
            dont_click=True
        )
        #    page_number -= 1


    def parse_funds_list(self, response):
        # Search for next page link, if it exists
        #if not response.meta['page_number']:
        #    page_number = "na"
        #else:
        #    page_number = response.meta['page_number']
        ## --- Log --- ##
        #self.logger.info(' --- [1] Numero de pagina: %s', page_number)
        ## --- Log --- ##
        for funds in response.xpath('//tr[contains(@class, "gridItem")]'):
            item = Cnbvt01Item()
            item['a_emisora'] = funds.xpath('td[@class="msDataText gridFundName Shrink"]/a/text()').extract()
            #item['c_familia'] = ""
            #item['i_benchmark_morningstar'] = ""
            item['j_link_cnbv'] = funds.xpath('td[@class="msDataText gridFundName Shrink"]/a/@href').extract()[0].replace("../", "http://lt.morningstar.com/7ap7omrzjm/")
            item['b_clas_cnbv'] = funds.xpath('td[@class="msDataText gridAmibSectorName"]/text()').extract()
            item['k_link_morningstar'] = item['j_link_cnbv'][0:item['j_link_cnbv'].find('&')].replace("lt.morningstar.com/7ap7omrzjm/", "www.morningstar.com.mx/mx/funds/")
            item['l_link_yahoofinanzas1'] = "https://es-us.finanzas.yahoo.com/q/hp?s=" + item['a_emisora'][0].replace('+', '').replace('.', '').replace(' ', '').replace('-', '').replace('&','%26') + ".MX"
            item['m_link_yahoofinanzas2'] = "https://es-us.finanzas.yahoo.com/q/hp?s=" + item['a_emisora'][0].replace('+', '').replace('.', '').replace(' ', '').replace('&','%26') + ".MX"
            if item['l_link_yahoofinanzas1'] == item['m_link_yahoofinanzas2']:
                item['m_link_yahoofinanzas2'] = ""

            ## --- Log --- ##
            #self.logger.info(' --- [1.1] Fondo: %s, URL_CNBV: %s', item['a_emisora'], item['j_link_cnbv'])
            ## --- Log --- ##
            #yield item
            request = scrapy.Request(item['j_link_cnbv'],
                callback=self.parse_fund_data,
                errback=self.parse_fund_data_err,
                priority=1,
                #dont_filter=True,
                meta={'dont_cache': True, 'handle_httpstatus_all': True}
            )
            request.meta['item'] = item
            ## --- Log --- ##
            #self.logger.info('page_number[%s] request_url %s', page_number, request.url)
            self.logger.info('Fondo[%s] request_url %s', item['a_emisora'], request.url)
            ## --- Log --- ##
            yield request

    def parse_page_funds(self, response):
        # Search for next page link, if it exists
        if not response.meta['page_number']:
            page_number = 1
        else:
            page_number = int(response.meta['page_number'])
        ## --- Log --- ##
        #self.logger.info(' --- [1] Numero de pagina: %d', page_number)
        ## --- Log --- ##
        for funds in response.xpath('//tr[contains(@class, "gridItem")]'):
            item = Cnbvt01Item()
            item['j_link_cnbv'] = funds.xpath('td[@class="msDataText gridFundName Shrink"]/a/@href').extract()[0].replace("../", "http://lt.morningstar.com/7ap7omrzjm/")

            ## --- Log --- ##
            #self.logger.info(' --- [1.1] Fondo: %s', item['a_emisora'])
            ## --- Log --- ##
            #yield item
            request = scrapy.Request(item['j_link_cnbv'],
                callback=self.parse_fund_data,
                errback=self.parse_fund_data_err,
                priority=1,
                #meta={'dont_cache': True, 'handle_httpstatus_all': True}
                meta={'item': item, 'dont_cache': True, 'handle_httpstatus_all': True}
            )
            item['a_emisora'] = funds.xpath('td[@class="msDataText gridFundName Shrink"]/a/text()').extract()
            #item['c_familia'] = ""
            #item['i_benchmark_morningstar'] = ""
            item['b_clas_cnbv'] = funds.xpath('td[@class="msDataText gridAmibSectorName"]/text()').extract()
            item['k_link_morningstar'] = item['j_link_cnbv'][0:item['j_link_cnbv'].find('&')].replace("lt.morningstar.com/7ap7omrzjm/", "www.morningstar.com.mx/mx/funds/")
            item['l_link_yahoofinanzas1'] = "https://es-us.finanzas.yahoo.com/q/hp?s=" + item['a_emisora'][0].replace('+', '').replace('.', '').replace(' ', '').replace('-', '').replace('&','%26') + ".MX"
            item['m_link_yahoofinanzas2'] = "https://es-us.finanzas.yahoo.com/q/hp?s=" + item['a_emisora'][0].replace('+', '').replace('.', '').replace(' ', '').replace('&','%26') + ".MX"
            if item['l_link_yahoofinanzas1'] == item['m_link_yahoofinanzas2']:
                item['m_link_yahoofinanzas2'] = ""

            request.meta['item'] = item
            ## --- Log --- ##
            #self.logger.info('page_number[%s] request_url %s', page_number, request.url)
            self.logger.info('Fondo[%s] request_url %s', item['a_emisora'], request.url)
            ## --- Log --- ##
            yield request

        # Check if this is the last page ("Sig" link must not have an URL to the next page)
        is_not_last = response.xpath('//div[@id="ctl00_ContentPlaceHolder1_aFundQuickrankControl_AspNetPager"]/table/tr/td/a[3]/@href').extract()
        if is_not_last:
            page_number += 1

            yield scrapy.FormRequest.from_response(
                response,
                formdata={'__EVENTTARGET': 'ctl00$ContentPlaceHolder1$aFundQuickrankControl$AspNetPager', '__EVENTARGUMENT': str(page_number)},
                priority=3,
                callback=self.parse_page_funds,
                meta={'page_number': str(page_number), 'dont_cache': True},
                dont_filter=True,
                dont_click=True
            )

    def parse_fund_data(self, response):
        ## --- Log --- ##
        #self.logger.info('response_url {url}'.format(url=response.url))
        self.logger.info('status %d response_url %s', response.status, response.url)
        ## --- Log --- ##
        item = response.meta['item']
        if response.status == 200:
            ## --- Log --- ##
            #self.logger.info(' --- [2] Fondo: %s - Status: %d', item['a_emisora'][0], response.status)
            ## --- Log --- ##
            # Get official fund data from CNBV online catalog
            item['d_adquiriente'] = response.xpath('//div[@id="keyStatsDiv"]/table[contains(@class, "keyStatsTable")]/tbody/tr[8]/td[2]/following-sibling::*/span/text()').extract()
            item['e_cat_cnbv'] = response.xpath('string(//div[@id="keyStatsDiv"]/table[contains(@class, "keyStatsTable")]/tbody/tr[4]/td)').extract()
            item['f_cat_fondos'] = response.xpath('string(//div[@id="keyStatsDiv"]/table[contains(@class, "keyStatsTable")]/tbody/tr[16]/td)').extract()
            item['g_fecha_inicio'] = response.xpath('string(//div[@id="keyStatsDiv"]/table[contains(@class, "keyStatsTable")]/tbody/tr[16]/td[3])').extract()
            item['h_benchmark_fondos'] = response.xpath('//div[@id="benchmarksBodyDiv"]/table/tr[2]/td/text()').extract()[0].replace('\n', '').replace('\t', '').strip()
        else:
            item['d_adquiriente'] = ""
            item['e_cat_cnbv'] = ""
            item['f_cat_fondos'] = ""
            item['g_fecha_inicio'] = ""
            item['h_benchmark_fondos'] = ""
        return item

    def parse_fund_data_err(self, failure):
        ## --- Log --- ##
        self.logger.info(' --- [3] Failure.type: %s, Failure.repr: %s, Failure.repr.value: %s', type(failure), repr(failure), repr(failure.value))
        #self.logger.info(' --- [3] Failure.value: %s, ErrorMesage: %s', failure.value, failure.getErrorMessage())
        ## --- Log --- ##
        # log all errback failures, in case you want to do something special for some errors, you may need the failure's type
        self.logger.error(repr(failure))

        #if isinstance(failure.value, HttpError):
        if failure.check(HttpError):
            # you can get the response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)
        #elif isinstance(failure.value, DNSLookupError):
        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)
        #elif isinstance(failure.value, TimeoutError):
        elif failure.check(TimeoutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
        #elif isinstance(failure.value, ResponseNeverReceived):
        elif failure.check(ResponseNeverReceived):
            request = failure.request
            self.logger.error('ResponseNeverReceived on %s', request.url)
        # Default fund data in case of error access to CNBV online catalog
        #item['d_adquiriente'] = "---"
        #item['e_cat_cnbv'] = "---"
        #item['f_cat_fondos'] = "---"
        #item['g_fecha_inicio'] = "---"
        #item['h_benchmark_fondos'] = "---"

    #def parse_list_funds(self, response):
    #    for funds in response.xpath('//tr[contains(@class, "gridItem")]'):
    #        item = Cnbvt01Item()
    #        item['emisora'] = funds.xpath('td[@class="msDataText gridFundName Shrink"]/a/text()').extract()
    #        item['link_morningstar'] = funds.xpath('td[@class="msDataText gridFundName Shrink"]/a/@href').extract()
    #        item['clas_cnbv'] = funds.xpath('td[@class="msDataText gridAmibSectorName"]/text()').extract()
    #        yield item
