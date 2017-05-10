#_-*- encoding:utf-8 -*-
import os
from lxml import etree
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule
from scrapy.http import Request
from scrapy.http import FormRequest
import requests

class TeacherSpider(CrawlSpider):
    name = 'TeacherSpider'
    download_delay = 5
    allowed_domains = ['51talk.com']
    # start_urls = ['http://www.51talk.com/reserve/index']
    # http://www.51talk.com/reserve/index?type=ph&Date=20170511&selectTime=13&course=fiveone&pageID=2&useSearch=y#goto
    # http://www.51talk.com/reserve/index?type=ph&Date=20170511&selectTime=13&course=fiveone&useSearch=y

    rules = (
        Rule(LinkExtractor(allow=('http://www.51talk.com/teacher/info/t\d{7,10}')),process_request='request_teacher',callback='parse_teacher_lesson',follow=False,),
    )
    need_book_lessons = [
                        # '20170512_44',
                         # '20170516_44','20170516_45',
                         # '20170517_44','20170517_45',
                         # '20170518_44','20170518_45',
                         # '20170519_44','20170519_45',
                         # '20170520_45',
                         # '20170521_44','20170521_45',
                         # '20170522_44','20170522_45',
                         '20170523_44','20170523_45'
                         ]
    #http://www.51talk.com/teacher/info/t432950510
    # url_pattern = ['http://www.51talk.com/teacher/info/t39644339']
    # url_extractor = LxmlLinkExtractor(allow="http://www.51talk.com/teacher/info/t39644339")
    cookie = 'user_tk_checkFg=1; visitid=3EF32499DE51ADD48AA439A3A13F9BFBMNzTAF40NYTWAx2rNMzjYAO0O0Ox; servChkFlag=sso; uuid=8ee79dc96865c77976d4929f07730dd9; remember_user=y; CNZZDATA1253020514=901012977-1493781924-http%253A%252F%252Fwww.51talk.com%252F%7C1494308562; price_show_type=4; aliyungf_tc=AQAAAF4X60IGcwAAXlTKb6KZmwQyG6Lu; NTKF_T2D_CLIENTID=guest3E0EB7A7-E139-EDC1-DFC1-CC682FF9D59A; nTalk_CACHE_DATA={uid:kf_9992_ISME9754_uid-0_nickname-,tid:1494322864235111}; Hm_lpvt_cd5cd03181b14b3269f31c9cc8fe277f=1494324405; Hm_lvt_cd5cd03181b14b3269f31c9cc8fe277f=1493783003,1494212227,1494307257; SpMLdaPx_poid=134; SpMLdaPx_pvid=1494324404823; SpMLdaPx_sid=4001506188; __utma=108070726.1864109400.1490844974.1494313076.1494318321.7; __utmc=108070726; __utmz=108070726.1490844974.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _gscbrs_551672857=1; _gscu_551672857=90844973bmmhnb20; servChkFlag=sso; user_usg=MCwCFFDy7d62oK16Z3imCy%2FhoG%2FNqvhiAhQ%2BkoZscl5ORI4vWfq4gBOngzsxFw%3D%3D; user_ust=I%2B0RRTZJXlqyb0QnGhWSOLl%2BkLWHoqN326R%2FBvKGpSDbnj0CZPtenUISk4W%2F0iym91Ci9dweYOxUwLjyO9aZZToRTQ8kyJFnVOS0MOc%3D; www_ugroup=4; PHPSESSID=8pg34qihpjmvrlvr9hh4059u04; global=5e07df5e-f0de-43dd-9a36-2920831cde62; UM_distinctid=15bcc67db977c0-0893999e8aa9f78-4a1b3104-1fa400-15bcc67db98921; from_url=www.51talk.com; SpMLdaPx_uuid=3511360630'


    def get_request_url(self):
        urls = []
        for lesson in self.need_book_lessons:
            for i in range(1,2):
                url = u'http://www.51talk.com/reserve/index?type=ph&Date={0}&selectTime={1}&course=fiveone&pageID={2}&useSearch=y'.format(lesson.split('_')[0],lesson.split('_')[1],i)
                print url
                # yield url
                urls.append(url)
        return urls

    def get_cookies(self,cookie):
        cookie_list = cookie.split(';')
        cookie_dic = {}
        for cookie_key_value in cookie_list:
            a_cookie = cookie_key_value.split('=')
            cookie_dic[a_cookie[0]] = a_cookie[1]
        return cookie_dic
    # http://stackoverflow.com/questions/32623285/how-to-send-cookie-with-scrapy-crawlspider-requests
    def start_requests(self):
        cookie_text = self.get_cookies(self.cookie)
        # urls = self.get_request_url();
        for url in self.get_request_url():
            yield Request(url,cookies=cookie_text)

    def request_teacher(self, request):
        cookie_text = self.get_cookies(self.cookie)
        tagged = request.replace(cookies=cookie_text)
        return tagged
        # return Request(request.url,callback=self.parse_teacher_lesson,cookies=cookie_text)

    def parse_teacher_lesson(self,response):
        favor_state = response.xpath('//div[@class="favor f-fr"]/p/text()').extract_first(default="N/A")
        teacher_id = response.url.split('?')[0].split('/')[-1]
        favor_count = favor_state.replace(u'人收藏','')
        if int(favor_count) > 10:
            print favor_count,
        else:
            return
        book_able = response.xpath("//div[@class='teacher']//li/input[@type='checkbox']/@id").extract()
        for lesson in book_able:
            if lesson in self.need_book_lessons:
                self.book_lesson_for_id(teacher_id,lesson)

    def book_lesson_for_id(self,teacher_id,lesson_id):
        print teacher_id,lesson_id

        '''
        os.abort(）
        停止爬取
        https://groups.google.com/forum/m/#!msg/python-cn/3wcbVkOANdE/hS1CpP4bVuQJ
        这里之所以用Requests,是因为Requests能够马上处理请求，
        如果是yield FormRequest,则该Request会被加到Scarpy队列里，
        一直等到该Request 之前的请求(通过Rule规则提取的请求)都处理完毕，才会处理该请求，
        
        请求体
        appoint_type=multi&t_id=t4893630&date_time=20170510_47%2C20170510_48&showCustom=0&reduceCount=2&
        is_price_course=&intelligent=2&ec_course_max=14&is_course_new=new&defaultTool=&is_selection_teacher=&
        is_from_ea_recommend=&show_freetalk=1&has_freetalk_course=n&course_thr=8926%2C8927&cla_en=new&
        tool=51TalkAC&lm_self_introduction=2&lm_recovery=2&Desc=
        '''
        payload = {
            'appoint_type': 'multi',
            't_id': teacher_id,
            'date_time': lesson_id,
            'showCustom': '0',
            'reduceCount': '0',
            'defaultTool': '',
            'is_selection_teacher': '',
            'is_from_ea_recommend': '',
            'course_thr': '8926',
            'intelligent': '2',
            'ec_course_max': '100',
            'is_course_new': 'new',
            'show_freetalk': '1',
            'has_freetalk_course': 'n',
            'cla_en': 'new',
            'tool': '51TalkAC',
            'lm_self_introduction': '2',
            'lm_recovery': '2',
        }
        session = requests.session()
        session.headers.update({"Cookie": self.cookie})
        r = session.post("http://www.51talk.com/reserve/doReserve", data=payload)
        # print r.content
        if "from_url=http%3A%2F%2Fwww.51talk.com%2Freserve%2Fsuccess%2F" in r.content:
            print u'功预约课程！'+ lesson_id
            self.need_book_lessons.remove(lesson_id)
        else:
            html = etree.HTML(r.content)
            title = html.xpath('//div[@class="hd"]/h4/text()')[0]
            tips = html.xpath('//div[@class="bd"]/p/text()')[0]
            print title + ":" + tips;
            if u"该时间您已经预约了课程" in tips:
                self.need_book_lessons.remove(lesson_id)
        if  len(self.need_book_lessons) == 0:
            print '退出爬虫'
            os.abort()








