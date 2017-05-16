#_-*- encoding:utf-8 -*-
import os
from lxml import etree
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule
from scrapy.http import Request
import requests

class TeacherSpider(CrawlSpider):
    name = 'TeacherSpider'
    download_delay = 5
    allowed_domains = ['51talk.com']
    allowed_page = 10   #允许每个上课时间所爬取得最大页数
    min_faver_count = 1000 #最少的收藏数
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
                         # '20170520_44','20170520_45',
                         # '20170521_44','20170521_45',
                         # '20170522_44','20170522_45',
                         # '20170523_44','20170523_45',
                         '20170524_44','20170524_45'
    ]
    #http://www.51talk.com/teacher/info/t432950510
    # url_pattern = ['http://www.51talk.com/teacher/info/t39644339']
    # url_extractor = LxmlLinkExtractor(allow="http://www.51talk.com/teacher/info/t39644339")
    cookie = ''

    #添加参数
    #http://blog.csdn.net/q_an1314/article/details/50748700
    def __init__(self,cookie=None, *args, **kwargs):
        super(TeacherSpider, self).__init__(*args, **kwargs)
        extern_cookie = '; aliyungf_tc=AQAAADYcVRrnUwgAXlTKb0sABqSD/ARo; servChkFlag=sso'
        self.cookie = (self.get_cookie_from_file(cookie) + extern_cookie).replace('\n', '')
        print(self.cookie)

    def get_cookie_from_file(self,cookie_file):
        f = open(cookie_file, 'r')
        cookie = f.readline()
        f.close()
        return cookie

    def get_request_url(self):
        urls = []
        for lesson in self.need_book_lessons:
            for i in range(1,self.allowed_page + 1):
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

    def parse(self, response):
        auto_login_text = response.xpath('/html/head/title/text()').extract_first(default='N/A')
        if auto_login_text == u'自动登录中':
            print 'cookie无效，退出程序'
            os.abort()
        return super(TeacherSpider,self).parse(response)

    def request_teacher(self, request):
        cookie_text = self.get_cookies(self.cookie)
        tagged = request.replace(cookies=cookie_text)
        return tagged
        # return Request(request.url,callback=self.parse_teacher_lesson,cookies=cookie_text)

    def parse_teacher_lesson(self,response):
        favor_state = response.xpath('//div[@class="favor f-fr"]/p/text()').extract_first(default="N/A")
        teacher_id = response.url.split('?')[0].split('/')[-1]
        favor_count = favor_state.replace(u'人收藏','')
        if int(favor_count) >= self.min_faver_count:
            print u'teacher_id为{}的老师有{}'.format(teacher_id,favor_state)
        else:
            return
        book_able = response.xpath("//div[@class='teacher']//li/input[@type='checkbox']/@id").extract()
        for lesson in book_able:
            if lesson in self.need_book_lessons:
                self.book_lesson_for_id(teacher_id,lesson)

    def book_lesson_for_id(self,teacher_id,lesson_id):
        print u'开始预约teacher_id为{}日期为{}的课程'.format(teacher_id,lesson_id)
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








