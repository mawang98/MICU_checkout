import json
from  icucheckOut_sqlite3 import *
import sqlite3

ParameterValues = {}
ParameterValues['beds'] = {0:'1',1:'2',2:'3',3:'4',4:'5',5:'6',6:'7',7:'8',8:'9',9:'10',10:'11',11:'12',12:'13',13:'14',14:'15',15:'16',16:'17',18:'18',19:'19',20:'20',21:'21',22:'22',23:'23',24:'24',25:'25',26:'26',27:'27',28:'J1',29:'J2',30:'J3'}
ParameterValues['fromWhere'] = {0:'急诊',1:'外科转入',2:'外科转入',3:'外科术后转入',4:'重症普通病房转入'}
ParameterValues['toWhere'] = {0:'自动出院',1:'死亡',2:'转外科',3:'转内科'}

a = tuple(dict.items(ParameterValues['beds']))
print(str(a)[1:-1])

conn = sqlite3.connect('datas.db')
cur = conn.cursor()
sql = 'INSERT INTO towhere VALUES '
sql2 = sql+str(a)[1:-1]
print(sql2)

cur.execute(sql2)
conn.commit()
cur.close()
conn.close()