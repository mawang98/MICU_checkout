import sqlite3
import datetime

conn = sqlite3.connect('datas.db')
cur = conn.cursor()
sql = '''SELECT checkoutDate FROM discharge WHERE (checkoutDate BETWEEN ? AND ?);'''

be = datetime.datetime.now().strftime('%Y-%m-%d')
to = (datetime.datetime.now()-datetime.timedelta(days=30)).strftime('%Y-%m-%d')
print(be,to)
c=cur.execute(sql,(to,be))
a = cur.fetchall()
print(a)
conn.commit()
cur.close()
conn.close()

z = datetime.datetime.now().strftime('%Y-%m-%d')
print(z)