import pymysql
from Common.readConfig import readconfigs


class DB_connect:
    def __init__(self, dbname="database", host=None):
        readconfig = readconfigs()
        if host is None:
            self.host = readconfig.get_db(dbname=dbname, name="host")
        else:
            self.host = host
        self.port = readconfig.get_db(dbname=dbname, name="port")
        self.user = readconfig.get_db(dbname=dbname, name="user")
        self.password = readconfig.get_db(dbname=dbname, name="password")
        self.database = readconfig.get_db(dbname=dbname, name="database")
        self.db = pymysql.connect(host=self.host, user=self.user, password=self.password, port=self.port,
                                  db=self.database)
        self.cursor = self.db.cursor()

    #
    # def open(self):
    #     # print(self.port,self.database)
    #

    def close(self):
        self.cursor.close()
        self.db.close()

    # 查询表中第一条数据
    def select_one(self, sql):
        try:
            if "select" in sql.lower():
                self.cursor.execute(sql)
                result = self.cursor.fetchone()
                # print(result)
                return result

            else:
                print("SQL syntax error, please enter select!")
                return
        except Exception as e:
            print('execute failure !', e)
        # self.close()

    # 查询表中所有数据
    def select_all(self, sql):
        try:
            if "select" in sql.lower():
                self.cursor.execute(sql)
                result = self.cursor.fetchall()
                print(result)
                return result

            else:
                print("SQL syntax error, please enter select!")
                return
        except Exception as e:
            print('execute failure !', e)
        # self.close()

    # 更新表中数据
    def update(self, sql):
        try:
            if "update" in sql.lower():
                row = self.cursor.execute(sql)
                self.db.commit()
                print("update successfully! the number of rows affected:%d" % row)
            else:
                print("SQL syntax error, please enter update!")
                return
        except Exception as e:
            self.db.rollback()
            print('execute failure !', e)
        # self.close()

    # 删除表中数据
    def delete(self, sql):
        try:
            if "delete" in sql.lower():
                row = self.cursor.execute(sql)
                self.db.commit()
                print("delete successfully! the number of rows affected:%d" % row)
            else:
                print("SQL syntax error, please enter delete!")
                return
        except Exception as e:
            self.db.rollback()
            print('execute failure !', e)
        # self.close()

    # 插入表中数据
    def insert(self, sql):
        try:
            if "insert" in sql.lower() and "into" in sql.lower():
                row = self.cursor.execute(sql)
                self.db.commit()
                print("insert successfully! the number of rows affected:%d" % row)
            else:
                print("SQL syntax error, please enter insert into!")
                return
        except Exception as e:
            self.db.rollback()
            print('execute failure !', e)
        # self.close()


if __name__ == '__main__':
    # db = DB_connect(dbname="hub_database")
    # db.select_one("SELECT * from t_user")
    # db.select_all("SELECT * from ets.document_statistics")
    # # # db.update("UpDATE t_user  set f_login_name='444' where f_login_name='44'")
    # db.insert("insert  INTO  t_watermark_doc VALUES ('10841','1','156735')")

    db_self = DB_connect(dbname="db_domain_self")
    db_self.delete("DELETE from t_domain_self")
    db_self.delete("DELETE from t_relationship_domain")
