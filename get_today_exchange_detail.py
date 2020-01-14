from io  import StringIO
import time,json,lxml
import random
import requests,pandas as pd
from bs4 import BeautifulSoup as bs

#爬取完整数据，根据进度条查看有多少页，在分页表爬取所要的信息
# 两种方式拿页码：一是直接利用BeautifulSoup拿链接原数据处理，二是遍历每一页，拼接数据，解构页码
#url：即是我们输入的url网址

def _code_to_symbol(code):
    #生成symbol代码标志,如输入000001，返回sz000001
    if len(code) != 6:
        return code
    else:
        if code[:1] in ['5', '6', '9'] or code[:2] in ['11', '13']:
            return 'sh%s' % code
        else:
            return 'sz%s' % code

#code方法
def getExchangeDetail(code):
    symbol = _code_to_symbol(code)

    #时间格式，字符串strftime格式:年月日，localtime本地时间
    date = time.strftime("%Y-%m-%d", time.localtime())

    #直接找的网址
    apiUrlTemplate = "http://vip.stock.finance.sina.com.cn/quotes_service/" \
             "api/json_v2.php/CN_Transactions.getAllPageTime?date=%s&symbol=%s"

    #直接请求URL，URL返回json数据 （原材料） 相当于获取完整页码
    URL = apiUrlTemplate%(date,symbol)

    #response简写res
    res = requests.get(URL)

    #防止乱码
    res.encoding = 'GBK'
    data_str = res.text

    #插头除尾
    data_str = data_str[1:-1]
    # {detailPages: [{  page: 1, begin_ts: "14:56:44", end_ts: "15:00:03"},
    #                   {page: 1, begin_ts: "14:56:44", end_ts: "15:00:03"}], detailDate: "2019-11-04"}

    #eval方法表示把上面的字符串data_str可当做命令来执行 （globals全局变量，locals局部变量）
    #每一个key加上“”，type创造类型，继承dict类，lambda是匿名函数返回n，最后返回一个dict
    data_str = eval(data_str, type('Dummy', (dict,), dict(__getitem__=lambda s, n: n))())
    pages = len(data_str['detailPages'])

    #空的DataFrame表
    data = pd.DataFrame()
    # for pNo in range(1, 2):
    for pNo in range(1, pages + 1):
        pause = random.randrange(5, 20)

        #返回一个空的DataFrame，不断添加内容进去
        data = data.append(_today_ticks(symbol, date, pNo,
                                        pause), ignore_index=True)

        #添加symbol列，长度定义与data列一样
        data['symbol'] = [symbol for _ in range(len(data))]
    return data
    # ({detailPages: [{page: 1, begin_ts: "09:32:53", end_ts: "09:36:48"}], detailDate: "2019-11-04"})


#获取某一页的数据 开始时间，介绍时间，页码
def _today_ticks(symbol, tdate, pageNo, pause):
    time.sleep(pause)

    #特地在Network中找的网址
    urlTemplate ="http://vip.stock.finance.sina.com.cn/quotes_service/" \
                 "view/vMS_tradedetail.php?symbol=%s&date=%s&page=%d"

    #分页爬取
    URL = urlTemplate%(symbol,tdate,pageNo)
    wb_data = requests.get(URL)

    #过滤乱码
    wb_data.encoding ='GBK'
    #lxml解释器 bs是BeautifulSoup的简写
    soup = bs(wb_data.text, 'lxml')

    #css中的table标签
    # 遍历table<class="datatbl">标签
    datatbl = soup.select('table[class="datatbl"]')[0]
    ls = datatbl.select('tr')
    lista = []

    # [[a,b,c],[a1,b1,c1]]
    #因为有重复的或者是没有出现过的属性，所以要过滤掉
    for item in ls[1:]:
        exchangetime = item.select('th')[0].get_text()
        price = item.select('td')[0].get_text()
        pchange = item.select('td')[1].get_text()
        change = item.select('td')[2].get_text()
        volume = item.select('td')[3].get_text()
        amount = item.select('td')[4].get_text()
        type = item.select('th')[1].get_text()
        lista.append([exchangetime, price, pchange, change, volume, amount, type])
        #print(lista)
    data = pd.DataFrame(lista, columns=['time', 'price', 'pchange', 'change', 'volume', 'amount', 'type'])

    data['pchange'] = data['pchange'].str.replace('+', '')
    data['tchange'] = data['tchange'].str.replace('+', '')
    data['volume'] = data['volume'].str.replace('+', '')
    data['amount'] = data['amount'].str.replace('+', '')

    data['time'] = ['%s  %s'%(tdate, part) for part in data['time']]
    print("---")
    return  data
#print(getExchangeDetail('002551'))