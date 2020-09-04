import os

import pymysql
from PyQt5 import QtSql


class DBCinema:
    def __init__(self, host, user, password, database):
        self.conn = pymysql.connect(host=host,
                                    user=user,
                                    password=password,
                                    db=database,
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.Cursor)
        # self.db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
        # self.db.setHostName(host)
        # self.db.setDatabaseName('labs')
        # self.db.setUserName(user)
        # self.db.setPassword(password)
        # self.db.open()

    def close(self):
        self.conn.close()

    def get_all_stuff(self):
        # self.query = QtSql.QSqlQuery(self.db)
        # self.query.prepare("SELECT * FROM сотрудники")
        # self.query.exec()
        # return self.query.result()
        with self.conn.cursor() as c:
            sql = "SELECT * FROM сотрудники "
            c.execute(sql)
            return c.fetchall()


if __name__ == '__main__':
    db = DBCinema(os.getenv('DB_HOST'), os.getenv('DB_USER'), os.getenv('DB_PASSWORD'),
                  os.getenv('DB_DATABASE'))
    # print(*db.get_all_stuff(), sep='\n==================\n')
    db.close()
