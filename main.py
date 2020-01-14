import pandas as pd
from sqlalchemy import create_engine
from get_today_exchange_detail import  getExchangeDetail
from queue_fifo import getQueue,putQueue
import time
engine = create_engine('mysql+mysqlconnector://root:aA100100!!@47.106.246.213:3306/test?auth_plugin=mysql_native_password', echo=False)
'''
建表语句
create table stocksTricks(
id int primary key not null auto_increment,
time VARCHAR(20),
price FLOAT,
pchange FLOAT,
tchange VARCHAR(20),
volume INT, 
amount INT, 
type VARCHAR(20),
symbol VARCHAR(20)
)
'''
stop = False
while not stop :
    try:
        code = getQueue()
    except Exception as e:
        print(e)
    if code == None:
        stop =True
    try:
        data = getExchangeDetail(code)
    except Exception as e:
        putQueue(code)
        time.sleep(360)
        print(e)
        continue
    data.to_sql(name='lianghuiying', con=engine, if_exists='append', index=False, chunksize=10)
