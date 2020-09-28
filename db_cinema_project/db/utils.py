import os

import pymysql


class DBException(Exception):
    pass


class DBCinema:
    def __init__(self, host, user, password, database):
        self.conn = pymysql.connect(host=host,
                                    user=user,
                                    password=password,
                                    db=database,
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.Cursor)

    def close(self):
        self.conn.close()

    def get_all_stuff(self):
        with self.conn.cursor() as c:
            sql = "SELECT * FROM сотрудники "
            c.execute(sql)
            return c.fetchall()

    def get_all_genre(self):
        with self.conn.cursor() as c:
            sql = """SELECT * FROM жанр ORDER BY id"""
            c.execute(sql)
            return c.fetchall(), c.description

    def get_one_genre(self, id):
        with self.conn.cursor() as c:
            sql = 'SELECT * FROM жанр WHERE id = %s'
            c.execute(sql, (id,))
            return c.fetchone()

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

    def add_user(self, name, email, number, hash):
        with self.conn.cursor() as c:
            sql = 'INSERT INTO cinemadb.покупатель (фио, телефон, почта, хэш) VALUES( %s, %s, %s, %s)'
            c.execute(sql, (name, number, email, hash))
            self.conn.commit()
            return c.lastrowid

    def add_genre(self, name):
        try:
            with self.conn.cursor() as c:
                sql = 'INSERT INTO cinemadb.жанр (название) VALUES( %s)'
                c.execute(sql, (name,))
                self.conn.commit()
        except pymysql.IntegrityError as e:
            code, message = e.args
            if code == 1062:
                raise DBException("Указанное название жанра уже существует.", *e.args)
            raise DBException("Не удалось добавить жанр.", *e.args)
        except pymysql.DataError as e:
            raise DBException("Слишком длинное название жанра.", *e.args)
        except Exception as e:
            raise DBException("Не удалось добавить жанр.", *e.args)

    def update_genre(self, gid, name):
        try:
            with self.conn.cursor() as c:
                sql = 'UPDATE жанр SET название = %s WHERE id = %s'
                c.execute(sql, (name, gid,))
                self.conn.commit()
        except pymysql.IntegrityError as e:
            code, message = e.args
            if code == 1062:
                raise DBException("Указанное название жанра уже существует.", *e.args)
            raise DBException("Не удалось обновить жанр.", *e.args)
        except pymysql.DataError as e:
            raise DBException("Слишком длинное название жанра.", *e.args)
        except Exception as e:
            raise DBException("Не удалось обновить жанр.", *e.args)

    def check_for_email(self, email):
        with self.conn.cursor() as c:
            sql = "SELECT id, хэш FROM покупатель WHERE почта = %s"
            c.execute(sql, email)
            return c.rowcount, c.fetchone()

    def delete_one_genre(self, id):
        try:
            with self.conn.cursor() as c:
                sql = 'DELETE FROM жанр WHERE id = %s'
                c.execute(sql, (id,))
                self.conn.commit()
        except Exception as e:
            raise DBException("Не удалось удалить жанр.", *e.args)



if __name__ == '__main__':
    db = DBCinema(os.getenv('DB_HOST'), os.getenv('DB_USER'), os.getenv('DB_PASSWORD'),
                  os.getenv('DB_DATABASE'))
    # print(*db.get_all_stuff(), sep='\n==================\n')
    db.close()
