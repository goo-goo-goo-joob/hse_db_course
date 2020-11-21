import pymysql
import os


class DBCinema:
    def __init__(self, host, user, password, database):
        self.conn = pymysql.connect(host=host,
                                    user=user,
                                    password=password,
                                    db=database,
                                    charset='utf8mb4',
                                    # charset='cp1251_general_ci',
                                    cursorclass=pymysql.cursors.Cursor)

    def close(self):
        self.conn.close()

    def create(self):
        with self.conn.cursor() as c:
            with open('create_tables.sql', 'r', encoding='utf8') as f:
                sql = "".join(f.read().splitlines())
                c.execute(sql)
                self.conn.commit()

    def triggers(self):
        with self.conn.cursor() as c:
            with open('triggers.sql', 'r', encoding='utf8') as f:
                sql = "".join(f.read().splitlines())
                c.execute(sql)
                self.conn.commit()

    def insert(self):
        with self.conn.cursor() as c:
            with open('insert_tables.sql', 'r', encoding='utf8') as f:
                sql = "".join(f.read().splitlines())
                c.execute(sql)
                self.conn.commit()
            with open('fill_tables.sql', 'r', encoding='utf8') as f:
                sql = "".join(f.read().splitlines())
                c.execute(sql)
                self.conn.commit()
            with open('fill_sessions.sql', 'r', encoding='utf8') as f:
                sql = "".join(f.read().splitlines())
                c.execute(sql)
                self.conn.commit()
            with open('buying_tickets.sql', 'r', encoding='windows-1251') as f:
                sql = "".join(f.read().splitlines())
                c.execute(sql)
                self.conn.commit()


def main():
    db = DBCinema(os.getenv('DB_HOST'), os.getenv('DB_USER'),
                  os.getenv('DB_PASSWORD'),
                  os.getenv('DB_DATABASE'))
    db.create()
    db.triggers()
    db.insert()
    db.close()


if __name__ == '__main__':
    main()
