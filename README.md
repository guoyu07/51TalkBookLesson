# 51TalkBookLesson
通过爬虫自动预约51Talk上的课程

# 使用方法
##### 1、创建Cookie
* 1、在根目录下创建一个名字为cookie的文件
* 2、用浏览器登录51talk,在开发模式下的控制台输入 `document.cookie`按回车，将cooke输出并粘贴到cookie文件，不需要双引号

##### 2、配置
* 1、在[TeacherSpider.py](https://github.com/one-smiling/51TalkBookLesson/blob/master/TalkBookLession/spiders/TeacherSpider.py)文件配置你需要的设置和预约的课程，具体配置如下:

	```
	allowed_page = 1   #允许每个上课时间所爬取得最大页数
	min_faver_count = 10 #外教老师最少的收藏数
	need_book_lessons = ['20170524_44','20170524_45']
	```

	**你可以修改以上参数来预约相应的的老师及课程，其中`need_book_lessons`中的参数`20170524_44 `代表2017年5月24日的21:30的课程，`_`前面的代表日期，后面的代表第几节课，时间从`6`点开始，数字从`13`开始，每半个小时数字加`1`，`6:30`则为`14`，`7：00`为`15`，依次类推，将你需要预约课程的时间添加到`need_book_lessons`中**

##### 3、运行
* 在终端下cd到工程根目录，并输入`scrapy crawl TeacherSpider -a cookie=cookie`开始执行



