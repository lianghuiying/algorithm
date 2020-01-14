from queue_fifo import putQueue
import pandas as pd
import kazoo

stockList= pd.read_excel('stockList.xls',dtype = {'code' : str})
codes = stockList['code']
for code in codes:
    try:
        putQueue(code)
    except kazoo.exceptions.NodeExistsError as e:
        print("kazoo.exceptions.NodeExistsError")
        continue
