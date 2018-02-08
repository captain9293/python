# -*- coding:utf-8 -*-
'''
草榴社区网页爬虫
用来直接找到种子链接
'''
import re
import sys
import time
import requests

MAIN_PAGE = 'http://cl.w7g.xyz/' #首页链接
pat1 = 'http://www.viidii.info/\\?http://www______rmdown______com/link______php\\?hash=[a-zA-Z0-9]+' #种子下载页面规则
pat2 = 'htm_data\\/[0-9]+\\/[0-9]+\\/[0-9]+\\.html' #帖子链接规则
pat3 = '<a href="htm_data\\/[0-9]+\\/[0-9]+\\/[0-9]+\\.html" target="_blank" id="">.*秦先生.*<\\/a>' #帖子标题规则

def get_torrentlist(page_index):
    '''
    抓取页面资源
    '''
    pageurl = 'http://cl.w7g.xyz/thread0806.php?fid=25&search=&page=%d'%page_index #进入亚洲无码区
    listpage = requests.get(pageurl, timeout=50)
    listpage.encoding = 'GBK' 
    titlist = re.findall(pat3, listpage.text.replace('\r',''))
    newitemlist = []
    count = 0
    for item in titlist:
        name = re.findall(r'>(.+?)<', item)[0]
        url = MAIN_PAGE + re.findall(r'href="(.+?)"', item)[0]
        torrentpage = requests.get(url, timeout=50).content.decode('GBK').replace('\r','')
        torrenturl = re.findall(pat1, torrentpage)
        if len(torrenturl) != 0:
            newitem = re.sub(pat2, torrenturl[0], item)
            newitemlist.append(newitem)
            count += 1
            print(count)
    
    return newitemlist

def make_html(itemlist):
    '''
    生成网页
    '''
    body = ''
    if len(itemlist) > 0:
        print('正在生成网页...')
        for x in itemlist:
            body = body + x + '</br>'
        html = '''<html>
        <head></head>
        <body>%s</body>
        </html>
        '''%body

        filename = time.strftime('%Y%m%d%H%M%S', time.localtime())
        with open('%s.html'%filename, 'w') as code:
            code.write(html)

        itemlist.clear()
        print('网页生成完毕！') 
    else:
        print('没有找到资源...')

   

if __name__ == '__main__':    
    itemlist = []
    page_index = sys.argv[1]
    for i in range(1, int(page_index)+1):
        print('正在获取第%d页的资源...'%i)
        singlelist = get_torrentlist(i)
        if len(singlelist) > 0:
            for item in singlelist:
                itemlist.append(item)

    make_html(itemlist)
