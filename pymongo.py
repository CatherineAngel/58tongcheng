import pymongo


class mongo():
    def __init__(self):
        #连接数据库
        client=pymongo.MongoClient("mongodb://localhost:27017/")
        self.db=client.dbms
        self.tc=self.db.tong
    def insert(self,datas):

        self.tc.insert_one(datas)
        return 1


    def query(self):
        pass

