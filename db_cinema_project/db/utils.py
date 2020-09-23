import os

import pymysql


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

    def add_user(self, name, email, number, hash):
        with self.conn.cursor() as c:
            sql = 'INSERT INTO cinemadb.покупатель (фио, телефон, почта, хэш) VALUES( % s, % s, % s, % s)'
            c.execute(sql, (name, number, email, hash))
            self.conn.commit()
            return c.lastrowid

    def check_for_email(self, email):
        with self.conn.cursor() as c:
            sql = "SELECT id, хэш FROM покупатель WHERE почта = %s"
            c.execute(sql, email)
            return c.rowcount, c.fetchone()

    def get_user_name_by_id(self, uid):
        with self.conn.cursor() as c:
            sql = "SELECT фио FROM покупатель WHERE id = %s"
            c.execute(sql, uid)
            return c.fetchone()[0]

    def get_all_user_numbers(self):
        with self.conn.cursor() as c:
            sql = "SELECT фио, телефон FROM покупатель "
            c.execute(sql)
            return c.fetchall()


if __name__ == '__main__':
    db = DBCinema(os.getenv('DB_HOST'), os.getenv('DB_USER'), os.getenv('DB_PASSWORD'),
                  os.getenv('DB_DATABASE'))
    # print(*db.get_all_stuff(), sep='\n==================\n')
    db.close()
