import sqlite3
import datetime

class DatabaseTool():
    def __init__(self):
        self.conn = sqlite3.connect('datas.db')
        self.cur = self.conn.cursor()
    def closeDb(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

class CreateTable(DatabaseTool):
    def createTableDischarge(self):
        sql = '''CREATE TABLE IF NOT EXISTS discharge(icuNum INT PRIMARY KEY, fromWhere TEXT, checkinTip TEXT, checkinDate DATE, admNum INT, name TEXT, gender TEXT, age INT, bed TEXT, checkoutTo Text, checkoutTip TEXT, checkoutDate DATE, diagnosis TEXT, isImportant INT, finalTip TEXT, operateTime TEXT)'''
        self.cur.execute(sql)
        self.closeDb()

class  InsertDatas(DatabaseTool):
    def insertData(self,patientData):#数据为元祖
        data = patientData
        #print(data)
        sql = 'INSERT INTO discharge VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        self.cur.execute(sql,data)
        self.closeDb()

class  ReadTable(DatabaseTool):
    def readTheHead(self):
        #读取表头
        sql = 'PRAGMA table_info(discharge)'
        self.cur.execute(sql)
        a = self.cur.fetchall()
        return(a)
        self.closeDb()

    def readAllDatas(self):
        #读取所有数据 并 返回读取结果
        sql = 'SELECT * FROM discharge'
        self.cur.execute(sql)
        a = self.cur.fetchall()
        return(a)
        self.closeDb()

    def readDatasInDate(self,Interval=30):
        #读取30天内的患者信息
        sql = 'SELECT * FROM discharge Where(checkoutDate BETWEEN ? AND ?)'
        fromTime = (datetime.datetime.now()-datetime.timedelta(days=Interval)).strftime('%Y-%m-%d')
        toTime = (datetime.datetime.now()+datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        self.cur.execute(sql,(fromTime,toTime))
        a = self.cur.fetchall()
        return(a)
        self.closeDb()       

    def readDatasWithName(self,name,fromTime,toTime):
        nameA = '%'+name+'%'
        fromTimeA = fromTime
        toTimeA = toTime
        sql ='''SELECT * FROM discharge WHERE (name LIKE '%s') AND (checkoutDate BETWEEN '%s' AND '%s');'''%(nameA,fromTimeA,toTimeA)
        #print(sql)
        self.cur.execute(sql)
        a = self.cur.fetchall()
        return(a)
        self.closeDb()
    
    def readDatasWithAdmnum(self,admNUm,fromTime,toTime):
        admNUmA = admNUm
        fromTimeA = fromTime
        toTimeA = toTime
        sql ='''SELECT * FROM discharge WHERE (admNum = %s) AND (checkoutDate BETWEEN '%s' AND '%s');'''%(admNUmA,fromTimeA,toTimeA)
        #print(sql)
        self.cur.execute(sql)
        a = self.cur.fetchall()
        return(a)
        self.closeDb()
    
    def readDatasWithDiag(self,diagnosis,fromTime,toTime):
        diagnosisA = '%'+diagnosis+'%'
        fromTimeA = fromTime
        toTimeA = toTime
        sql ='''SELECT * FROM discharge WHERE (diagnosis LIKE '%s') AND (checkoutDate BETWEEN '%s' AND '%s');'''%(diagnosisA,fromTimeA,toTimeA)
        #print(sql)
        self.cur.execute(sql)
        a = self.cur.fetchall()
        return(a)
        self.closeDb()
    def readDatasWithIcunum(self,icuNum):
        icuNumA = icuNum
        sql ='''SELECT * FROM discharge WHERE (icuNum = %s) ;'''%(icuNumA)
        #print(sql)
        self.cur.execute(sql)
        a = self.cur.fetchall()
        return(a)
        self.closeDb()

########### 参数数据表 towhere,fromwhere,beds 操作##############################################
class Parameters(DatabaseTool):
    def creat_towhere(self):
        sql = 'CREATE TABLE IF NOT EXISTS towhere(snum INT PRIMARY KEY,towhere TEXT)'
        self.cur.execute(sql)
        self.closeDb()
    def creat_fromwhere(self):
        sql = 'CREATE TABLE IF NOT EXISTS fromwhere(snum INT PRIMARY KEY,fromwhere TEXT)'
        self.cur.execute(sql)
        self.closeDb()
    def creat_beds(self):
        sql = 'CREATE TABLE IF NOT EXISTS beds(snum INT PRIMARY KEY,bed TEXT)'
        self.cur.execute(sql)
        self.closeDb()       

    def delete_towhere(self):
        sql = 'DELETE FROM towhere'
        self.cur.execute(sql)
        self.closeDb()

    def refresh_towhere_values(self,values):#values为字典{1：'急诊'，.....}
        a = tuple(dict.items(values))
        sql = 'INSERT INTO towhere VALUES '
        sql2 = sql+str(a)[1:-1]
        self.cur.execute(sql2)
        self.closeDb()

    def delete_fromwhere(self):
        sql = 'DELETE FROM fromwhere'
        self.cur.execute(sql)
        self.closeDb()

    def refresh_fromwhere_values(self,values):#values为字典{1：'急诊'，.....}
        a = tuple(dict.items(values))
        sql = 'INSERT INTO fromwhere VALUES '
        sql2 = sql+str(a)[1:-1]
        self.cur.execute(sql2)
        self.closeDb()

    def delete_beds(self):
        sql = 'DELETE FROM beds'
        self.cur.execute(sql)
        self.closeDb()

    def refresh_beds_values(self,values):#values为字典{1：'急诊'，.....}
        a = tuple(dict.items(values))
        sql = 'INSERT INTO beds VALUES '
        sql2 = sql+str(a)[1:-1]
        self.cur.execute(sql2)
        self.closeDb()
    
    def read_towhere(self):
        sql = 'SELECT * FROM towhere'
        self.cur.execute(sql)
        a = self.cur.fetchall()
        b = {}
        for i in a:
            b[int(i[0])]=i[1]
        return(b)
        self.closeDb()
    
    def read_fromwhere(self):
        sql = 'SELECT * FROM fromwhere'
        self.cur.execute(sql)
        a = self.cur.fetchall()
        b = {}
        for i in a:
            b[int(i[0])]=i[1]
        return(b)
        self.closeDb()

    def read_beds(self):
        sql = 'SELECT * FROM beds'
        self.cur.execute(sql)
        a = self.cur.fetchall()
        b = {}
        for i in a:
            b[int(i[0])]=i[1]
        return(b)
        self.closeDb()
            


