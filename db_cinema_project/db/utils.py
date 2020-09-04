import os

import pymysql


class DBCinema:
    def __init__(self, host, user, password, database):
        self.conn = pymysql.connect(host=host,
                                    user=user,
                                    password=password,
                                    db=database,
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)

    def close(self):
        self.conn.close()

    def get_all_stuff(self):
        with self.conn.cursor() as c:
            sql = "SELECT * FROM сотрудники "
            c.execute(sql)
            return c.fetchall()


if __name__ == '__main__':
    db = DBCinema(os.getenv('DB_HOST'), os.getenv('DB_USER'), os.getenv('DB_PASSWORD'),
                  os.getenv('DB_DATABASE'))
    print(*db.get_all_stuff(), sep='\n==================\n')
    db.close()
