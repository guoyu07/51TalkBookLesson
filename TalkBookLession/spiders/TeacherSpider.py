#_-*- encoding:utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule
from scrapy.http import Request
from scrapy_splash import SplashRequest
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy import Spider

'''
visitid=59EDA956E4D8DD96CA56069F8022E533MNzTAF40NYTWAx2rNMzjYAO0O0Ox; uuid=8ee79dc96865c77976d4929f07730dd9; remember_user=y; CNZZDATA1253020514=901012977-1493781924-http%253A%252F%252Fwww.51talk.com%252F%7C1494308562; price_show_type=4; Hm_lpvt_cd5cd03181b14b3269f31c9cc8fe277f=1494311672; Hm_lvt_cd5cd03181b14b3269f31c9cc8fe277f=1493783003,1494212227,1494307257; NTKF_T2D_CLIENTID=guest3E0EB7A7-E139-EDC1-DFC1-CC682FF9D59A; SpMLdaPx_poid=26; SpMLdaPx_pvid=1494311671555; SpMLdaPx_sid=4430365590; nTalk_CACHE_DATA={uid:kf_9992_ISME9754_uid-0_nickname-,tid:1494309829025757}; __utma=108070726.1864109400.1490844974.1494307257.1494309282.5; __utmb=108070726.10.9.1494310351443; __utmc=108070726; __utmz=108070726.1490844974.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _gscbrs_551672857=1; _gscs_551672857=t94309281mrrlc597|pv:4; _gscu_551672857=90844973bmmhnb20; PHPSESSID=8pg34qihpjmvrlvr9hh4059u04; UM_distinctid=15bcc67db977c0-0893999e8aa9f78-4a1b3104-1fa400-15bcc67db98921; from_url=www.51talk.com; SpMLdaPx_uuid=3511360630

'''

class TeacherSpider(CrawlSpider):
    name = 'TeacherSpider'
    download_delay = 5
    allowed_domains = ['51talk.com']
    start_urls = ['http://www.51talk.com/reserve/index']
    rules = (
        Rule(LinkExtractor(allow="http://www.51talk.com/teacher/info/t\d{1,10}"),callback='parse_item',follow=True,),
    )

    #http://www.51talk.com/teacher/info/t432950510
    # url_pattern = ['http://www.51talk.com/teacher/info/t39644339']
    # url_extractor = LxmlLinkExtractor(allow="http://www.51talk.com/teacher/info/t39644339")
    cookie = {
           'visitid':'59EDA956E4D8DD96CA56069F8022E533MNzTAF40NYTWAx2rNMzjYAO0O0Ox',
            'uuid':'8ee79dc96865c77976d4929f07730dd9',
            'remember_user':'y',
        'CNZZDATA1253020514': '901012977-1493781924-http%253A%252F%252Fwww.51talk.com%252F%7C1494308562',
        'price_show_type': '4',
        'Hm_lpvt_cd5cd03181b14b3269f31c9cc8fe277f': '1494311672',
        'Hm_lvt_cd5cd03181b14b3269f31c9cc8fe277f': '1493783003,1494212227,1494307257',
        'NTKF_T2D_CLIENTID': 'guest3E0EB7A7-E139-EDC1-DFC1-CC682FF9D59A',
        'SpMLdaPx_poid': '26',
        'SpMLdaPx_pvid': '1494311671555',
        'SpMLdaPx_sid': '4430365590',
        'nTalk_CACHE_DATA':'{uid:kf_9992_ISME9754_uid-0_nickname-,tid:1494309829025757}',
        '__utma': '108070726.1864109400.1490844974.1494307257.1494309282.5',
        '__utmb': '108070726.10.9.1494310351443',
        '__utmc': '108070726',
        '__utmz': '108070726.1490844974.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
        '_gscbrs_551672857': '1',
        '_gscs_551672857': 't94309281mrrlc597|pv:4',
        '_gscu_551672857': '90844973bmmhnb20',
        'PHPSESSID': '8pg34qihpjmvrlvr9hh4059u04',
        'UM_distinctid': '15bcc67db977c0-0893999e8aa9f78-4a1b3104-1fa400-15bcc67db98921',
        'from_url': 'www.51talk.com',
        'SpMLdaPx_uuid': '3511360630',
        'aliyungf_tc':'AQAAADYcVRrnUwgAXlTKb0sABqSD/ARo',
        'servChkFlag':'sso'
    }
    
    def start_requests(self):
        for url in self.start_urls:
            print url
            yield Request(url,callback=self.parse,cookies=self.cookie)
            # yield SplashRequest(url, callback=self.parse, args={'wait': 10},cookies=self.cookie)

    def parse_item(self,response):
        print '----------------'
        print response.text




