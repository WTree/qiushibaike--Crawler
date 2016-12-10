# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 17:16:41 2016

@author: weir
"""

import urllib
import urllib.request
import re



class QSBK:
    
    #初始化方法，定义一些变量
    def __init__(self):
        self.pageIndex=1
        self.user_agent='Mozilla/4.0(compatible;MSIE 5.5;Windows NT)'
        #初始化headers
        self.headers={'User-Agent':self.user_agent}
        #存放段子的变量
        self.stories=[]
        #存放程序是否继续运行的变量
        self.enable=False
    #传入某一页的索引获得页面代码
    def getPage(self,pageIndex):
        try:
            url='http://www.qiushibaike.com/hot/page/'+str(pageIndex)
            request=urllib.request.Request(url,headers=self.headers)
            response=urllib.request.urlopen(request)
            pageCode=response.read().decode('utf-8')
            return pageCode
            
        except urllib.request.URLError as e:
            if hasattr(e,"reason"):
                print("连接失败",e.reason)
                return None
        
    def getPageItems(self,pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print("页面加载失败....")
            return None     
            
        pattern=re.compile('<div class="author clearfix">.*?<h2>(.*?)</h2>.*?"content">(.*?)</div>.*?number">(.*?)</.*?number">(.*?)</.', re.S)
        items=re.findall(pattern,pageCode)
        #存储每页的段子
        pageStories=[]
        #遍历正则表达式匹配的信息
        for item in items:
            
                replaceBR = re.compile('<br/>')
                temp_text1 = re.sub(replaceBR,"\n",item[1])
                #item[0]是一个段子的发布者，item[1]是内容，item[2]是发布时间，item[3]是点赞数
                temp_text2 = temp_text1.replace("<span>","")
                text  = temp_text2.replace("</span>","")
                pageStories.append([item[0].strip(),text.strip(),item[2].strip(),item[3].strip()])
        return pageStories
        
    #加载并提取页面内容加入列表
    def loadPage(self):
        #如果当前未看到页面数少于2页，加载新一页
        if self.enable == True:
            if len(self.stories)<2:
                #获取新一页
                pageStories=self.getPageItems(self.pageIndex)
                #将该页的段子存放到全局list中
                if pageStories:
                    self.stories.append(pageStories)
                    #获取完之后页码索引加一，表示下次读取下一页
                    self.pageIndex+=1
                        
    #调用该方法，每次敲回车打印输出一个段子
    def getOneStory(self,pageStories,page):
        #遍历一页的段子
        for story in pageStories:
            #等待用户输入
            myinput=input()
            #每当输入回车一次，判断一下是否要加载新页面
            self.loadPage()
            #输入Q程序结束
            if myinput == 'Q':
                self.enable=False
                return
            print("第%d页\t发布人: %s\t发布时间：%s\t赞：%s\n%s"%(page,story[0],story[2],story[3],story[1]))
        
    #开始方法
    def start(self):
        print(u'正在读取，按回车查看新段子，Q退出')
        #使变量为true，使程序可以正常工作
        self.enable=True
        #先加载1页
        self.loadPage()
        #局部变量，控制当前读到第几页
        nowPage=0
        while self.enable:
            if len(self.stories)>0:
                #从全局list中获取1页段子
                pageStories=self.stories[0]
                #当前读到页数加1
                nowPage+=1
                #将全局list中第一个元素删除，因为已经取出
                del self.stories[0]
                #输出该页段子
                self.getOneStory(pageStories,nowPage)
                    
spider = QSBK()
spider.start()
                    
                