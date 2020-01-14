import pandas as pd
from sqlalchemy import create_engine
engine = create_engine('mysql+mysqlconnector://root:aA100100!!@47.106.246.213:3306/test?auth_plugin=mysql_native_password', echo=False)

data = pd.read_sql("select * from stocksTricks where symbol in ('sz000005','sz000001','sz000002');",engine)
print(data)