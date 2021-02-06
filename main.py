import requests
import time
import pandas as pd
import urllib.parse as urp
import re
from matplotlib import pyplot as plt
import jieba
from wordcloud import WordCloud
import PIL.Image as image
import numpy as np
from pylab import *
mpl.rcParams['font.sans-serif'] = ['Arial Unicode MS']
def get_data(i,keyword):
    url = 'https://tousu.sina.com.cn/api/index/s?&keywords='+keyword+'&page_size=10&page='+i
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363'}
    data = requests.get(url,headers=headers).text
    qingqiupat = ',"appeal":"(.*?)"'
    neironpat = '"summary":"(.*?)"'
    locationpat = 'location":"(.*?)"}},'
    titlepat = '"title":"(.*?)","uid":'
    qingqiulist = re.compile(qingqiupat).findall(data)
    neironlist = re.compile(neironpat).findall(data)
    locationlist = re.compile(locationpat).findall(data)
    titlelist = re.compile(titlepat).findall(data)
    return neironlist, qingqiulist, locationlist, titlelist
neironlists = []
qingqiulists = []
locationlists = []
titlelists = []
key = input('请输入搜索关键词:  ')
keyword = urp.quote(key)
i = eval(input('请输入需要爬取的投诉条数(不能少于10）:   '))
i = math.floor(i/10)
for i in range(i):  
    o = str(i)
    print('正在爬取第{}页'.format(i))      
    neironlist, qingqiulist,locationlist,titlelist = get_data(o,keyword)
    try:
        
        for neiron in neironlist:
                p = neiron.encode('utf-8').decode('unicode_escape')
                neironlists.append(p)
                
        for qingqiu in qingqiulist:
                p = qingqiu.encode('utf-8').decode('unicode_escape')
                qingqiulists.append(p)
                
        for location in locationlist:     
                p = location.encode('utf-8').decode('unicode_escape')
                locationlists.append(p)
                
        for title in titlelist:
                p = title.encode('utf-8').decode('unicode_escape')
                titlelists.append(p)
                
        time.sleep(0.5)
    except :
        print('eeeeesorry')
        pass
print('开始处理数据')
#print('处理标题')
titlelists = ','.join(titlelists)
neironlists = ','.join(neironlists)
for ch in '!@#$%^&*()_+-=[]{}\|""'':?><;,./`~qazwsxedcrfvtgbyhnujmikolpQAZWSXEDCRFVTGBYHNUJMIKOLP1234567890':
    titlelists = titlelists.replace(ch,'')
    neironlists = neironlists.replace(ch,'')
#print('画柱形图')
qingqiulistss = ','.join(qingqiulists)
qingqiulists = qingqiulistss.split(',')
qingqiu = set(qingqiulists)
qingqiu = list(qingqiu)
times=[]
for i in qingqiu:
    times.append(qingqiulists.count(i))
qingqiuFrame = pd.DataFrame(qingqiu,times)
g = qingqiuFrame[qingqiuFrame.index>2]#如果投诉请求太密集可以修改这个数字
#print(h)
plt.title(key)
plt.xlabel('数量')
plt.ylabel('投诉理由')
plt.barh(g[0],g.index)
plt.show()
#地址
location = set(locationlists)
location = list(location)
while '其他' in location:
    location.remove('其他')
time2=[]
for i in location:
    time2.append(locationlists.count(i))
locatFrame = pd.DataFrame(location,time2)
l = locatFrame[locatFrame.index>1]#如果太密集可以修改这个数字
plt.title('地址')
plt.xlabel('数量')
plt.ylabel('地名')
plt.barh(l[0],l.index)
plt.show()
# 分词
def fenci(text):
 # 接收分词的字符串
    word_list = jieba.cut(text)
    # 分词后在单独个体之间加上空格
    result = " ".join(word_list)
    return result
titletext = fenci(titlelists)
neirontext = fenci(neironlists)
keywords = fenci(key)
keywords = keywords.split(' ')
keywords.append('匿名')
keywords.append('其他')
wordcloud = WordCloud(
        prefer_horizontal = 0.95,
        font_path = "simhei.ttf",
        background_color="white", #背景颜色
        max_words=100, #显示最大词数
        stopwords = (keywords),
        min_font_size=10,
        max_font_size=50,
        scale=2,        # 比列放大  数值越大  词云越清晰
        # width=1680,  #图幅宽度
        # height=1050,
        random_state=50,
        relative_scaling=0.5,
        collocations = False
    ).generate(titletext)
image_produce = wordcloud.to_image()
image_produce.show()
    #由于发现标题更适合生成词云，因此未将内容再进行词云生成，若有需要可以重复上面的过程