
#-*- encoding: utf-8 -*-

import urllib2
import urllib
import re

#定义糗事百科类
class QSBK:
    
    #初始化方法，定义一些变量
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}
        #存放段子的变量，每一个元素是每一页的段子
        self.stories = []
        self.currentStoryIndex = 0
        #存放程序是否继续运行的变量
        self.enable = False

    #传入某一页的索引得页面代码
    def getPage(self, pageIndex):
        try:
            url = 'http://www.qiushibaike.com/text/page/' + str(pageIndex)
            #构建请求的request
            request = urllib2.Request(url, headers=self.headers)
            #利用urlopen获取页面代码
            response = urllib2.urlopen(request)
            #将页面转化为UTF-8编码
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print('连接糗事百科失败，错误原因', e.reason)
                return None

    #传入某一页的代码，返回段子列表
    def gegPageItems(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if pageCode is None:
            return None

        pattern = re.compile('<div class="author clearfix">.*?<a.*?<h2>(.*?)</h2>.*?' + 
            '<a.*?<div.*?<span>(.*?)</span>', re.S)
        items = re.findall(pattern, pageCode)
        #用来存储煤业的段子
        pageStories = []
        replaceBR = re.compile('<br/>')
        for item in items:
            text = re.sub(replaceBR, '\n', item[1])
            pageStories.append([item[0], text])
        return pageStories

    #加载并获取页面的内容，加入到列表中
    def loadPage(self):
        #如果当前未看的页数少于两页，则加载新的一页
        if self.enable == True:
            if len(self.stories) < 2:
                #获取新的一页
                pageStories = self.gegPageItems(self.pageIndex)
                if pageStories is not None:
                    self.stories.append(pageStories)
                    #获取完之后页码索引加1，表示下一次读取下一页
                    self.pageIndex += 1
    
    #调用该方法，每次敲击回车打印输出一条段子
    def getOneStory(self, pageStories):
        #遍历一页的段子
        for story in pageStories:
            #等待用户输入
            input = raw_input()
            #每当输入回车一次，判断一下是否要加载新页面
            self.loadPage()
            #如果输入Q则退出程序
            if input == 'Q' or input == 'q':
                self.enable = False
                return
            self.currentStoryIndex += 1
            print(u'第%d条\t发布人:%s' % (self.currentStoryIndex, story[0]))
            print(u'内容:%s' % story[1])

    #开始方法
    def start(self):
        print(u'正在读取糗事百科，按回车查看新段子，Q退出')
        #使变量为True，程序可以正常运行
        self.enable = True
        #先加载一页内容
        self.loadPage()
        #局部变量，控制当前督导了第几页
        while self.enable:
            if len(self.stories) > 0:
                #从全局list中获取一页段子
                pageStories = self.stories[0]
                #将全局list中第一个元素删除，因为已经取出
                del self.stories[0]
                #输出该页的段子
                self.getOneStory(pageStories)


if __name__ == '__main__':
    spider = QSBK()
    spider.start()