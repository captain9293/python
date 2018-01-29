# -*- coding:utf-8 -*-
'''
草榴社区网页爬虫
用来直接找到种子链接
'''
import re
import time
import requests

BODY = ''
WITE = 0

home_page = 'http://cl.w7g.xyz//' #首页链接
pat1 = 'http://www.viidii.info/\\?http://www______rmdown______com/link______php\\?hash=[a-zA-Z0-9]+' #种子下载页面规则
pat2 = 'htm_data\\/[0-9]+\\/[0-9]+\\/[0-9]+\\.html' #帖子链接规则
pat3 = '<h3><a href="htm_data\\/[0-9]+\\/[0-9]+\\/[0-9]+\\.html" target="_blank" id="">.*秦先生.*' #帖子标题规则


def get_html(url):
    '''
    获取页面
    '''
    page = requests.get(url)
    page.encoding = 'GBK'
    return page.text


def get_content(pat, text):
    '''
    根据规则获取内容
    '''
    content = re.compile(pat)
    conlist = re.findall(content, text)
    return conlist


print('正在获取主题列表....')

print('正在拼装网页主体....')
for i in range(1, 100):
    pageurl = 'http://cl.w7g.xyz/thread0806.php?fid=25&search=&page=%d'%i #进入亚洲无码区
    print(pageurl)
    listpage = get_html(pageurl)
    titlst = get_content(pat3, listpage)
    for x in titlst:
        print(get_content(pat2, x)[0])
        newurl = home_page + get_content(pat2, x)[0]
        zzpage = get_html(newurl)
        zzurl = get_content(pat1, zzpage)
        zzurl_len = len(zzurl)
        if zzurl_len == 0:
            continue
        elif len(zzurl) >= 1:
            x = re.sub(pat2, zzurl[0], x)
            BODY = BODY + x
        WITE = WITE + 1
        print(WITE)

html = '''<html>
<head></head>
<body>%s</body>
</html>
'''%(BODY)

tim = time.strftime('%Y%m%d%H%M%S', time.localtime())

print('正在保存网页....')

f = open('秦先生%s.html'%tim, 'w', encoding='UTF-8')
f.write(html)
f.close()

print('抓取完成！')
