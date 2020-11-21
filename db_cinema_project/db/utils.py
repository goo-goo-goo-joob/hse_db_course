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

    def get_all_genre(self):
        with self.conn.cursor() as c:
            sql = """SELECT * FROM жанр ORDER BY название"""
            c.execute(sql)
            return c.fetchall(), c.description

    def get_all_genre1(self):
        with self.conn.cursor() as c:
            sql = """SELECT DISTINCT ж.*
FROM жанрыфильмов
         JOIN жанр ж on ж.id = жанрыфильмов.idжанр
ORDER BY ж.название"""
            c.execute(sql)
            return c.fetchall(), c.description

    def get_genre_film(self, idfilm):
        with self.conn.cursor() as c:
            sql = """SELECT DISTINCT ж.id, ж.название
FROM жанрыфильмов
         JOIN жанр ж on ж.id = жанрыфильмов.idжанр
WHERE idфильм = %s
ORDER BY ж.название"""
            c.execute(sql, idfilm)
            return c.fetchall(), c.description

    def get_all_producer(self):
        with self.conn.cursor() as c:
            sql = """SELECT * FROM режиссер ORDER BY фио"""
            c.execute(sql)
            return c.fetchall(), c.description

    def get_all_restrict(self):
        with self.conn.cursor() as c:
            sql = """SELECT *
FROM возрастноеограничение
ORDER BY CHAR_LENGTH(возраст), возраст"""
            c.execute(sql)
            return c.fetchall(), c.description

    def get_all_typesess(self):
        with self.conn.cursor() as c:
            sql = """SELECT * FROM типсеанса ORDER BY времяначала"""
            c.execute(sql)
            return c.fetchall(), c.description

    def get_all_cinema(self):
        with self.conn.cursor() as c:
            sql = """SELECT * FROM кинотеатр ORDER BY название, адрес"""
            c.execute(sql)
            return c.fetchall(), c.description

    def get_all_cinema2(self):
        with self.conn.cursor() as c:
            sql = """SELECT id, название as "Название", адрес as "Адрес" FROM кинотеатр ORDER BY название, адрес"""
            c.execute(sql)
            return c.fetchall(), c.description

    def get_all_cinema1(self, idfilm):
        with self.conn.cursor() as c:
            sql = """SELECT DISTINCT(кинотеатр.адрес)
FROM кинотеатр
         JOIN зал з on кинотеатр.id = з.idкинотеатр
         JOIN типзала т on т.id = з.idтипзала
         JOIN форматыфильмов ф on т.id = ф.idтипзала
WHERE ф.idфильм = %s
ORDER BY кинотеатр.название, адрес"""
            c.execute(sql, (idfilm))
            return c.fetchall(), c.description

    def get_allcinema_hall(self, cinema):
        with self.conn.cursor() as c:
            sql = """SELECT название FROM зал WHERE idкинотеатр = %s"""
            c.execute(sql, self.get_id_cinema(cinema))
            return c.fetchall()

    def get_allcinema_hall1(self, cinema, film):
        with self.conn.cursor() as c:
            sql = """SELECT DISTINCT (зал.название)
FROM зал
         JOIN форматыфильмов ф on зал.idтипзала = ф.idтипзала
         JOIN кинотеатр к on к.id = зал.idкинотеатр
WHERE к.адрес = %s
  and ф.idфильм = %s"""
            c.execute(sql, (cinema, film))
            return c.fetchall()

    def get_all_typehall(self):
        with self.conn.cursor() as c:
            sql = """SELECT * FROM типзала ORDER BY название"""
            c.execute(sql)
            return c.fetchall(), c.description

    def get_all_hall(self):
        with self.conn.cursor() as c:
            sql = """SELECT зал.id,
       зал.название as `название`,
       длинаряда,
       числорядов,
       к.адрес      as `адрескинотеатра`,
       т.название   as `тип зала`
FROM зал
         JOIN кинотеатр к on к.id = зал.idкинотеатр
         JOIN типзала т on т.id = зал.idтипзала
ORDER BY к.адрес, название"""
            c.execute(sql)
            return c.fetchall(), c.description

    def get_all_film(self):
        with self.conn.cursor() as c:
            sql = """SELECT фильм.id,
       название as 'Название',
       описание as 'Описание',
       год as 'Год',
       длительность as 'Длительность',
       возраст as 'Ограничение',
       фио as 'Режиссер'
FROM фильм
         JOIN возрастноеограничение в on в.id = фильм.idвозраст
         JOIN режиссер р on р.id = фильм.idрежиссер
ORDER BY название, год, р.фио"""
            c.execute(sql)
            return c.fetchall(), c.description

    def get_desc_film(self, desc):
        with self.conn.cursor() as c:
            sql = """SELECT фильм.id,
       название as 'Название',
       описание as 'Описание',
       год as 'Год',
       длительность as 'Длительность',
       возраст as 'Ограничение',
       фио as 'Режиссер'
FROM фильм
         JOIN возрастноеограничение в on в.id = фильм.idвозраст
         JOIN режиссер р on р.id = фильм.idрежиссер
WHERE описание LIKE %s OR название LIKE %s
ORDER BY название, год, р.фио"""
            c.execute(sql, ("%" + desc + "%", "%" + desc + "%"))
            return c.fetchall(), c.description

    def get_allsession_film(self):
        '''
        возвращает все фильмы на которые есть сеансы и свободные места
        '''
        with self.conn.cursor() as c:
            sql = """SELECT DISTINCT фильм.id,
       название     as 'Название',
       описание     as 'Описание',
       год          as 'Год',
       длительность as 'Длительность',
       возраст      as 'Ограничение',
       фио          as 'Режиссер'
FROM фильм
         JOIN возрастноеограничение в on в.id = фильм.idвозраст
         JOIN режиссер р on р.id = фильм.idрежиссер
         LEFT JOIN сеанс с on фильм.id = с.idфильм
         JOIN (SELECT idсеанс, COUNT(id) as tot
               FROM билетнаместо
               WHERE idпокупатель IS NULL
               GROUP BY idсеанс) t on t.idсеанс = с.id
WHERE с.id IS NOT NULL
  AND t.tot != 0
ORDER BY название, год, р.фио;"""
            c.execute(sql)
            return c.fetchall(), c.description

    def get_all_session(self):
        with self.conn.cursor() as c:
            sql = """SELECT сеанс.id,
       ф.название as 'Фильм',
       р.фио as 'Режиссер',
       ф.год as 'Год',
       к.адрес as 'Кинотеатр',
       з.название as 'Зал',
       сеанс.датавремя as 'Дата'
FROM сеанс
         JOIN зал з on з.id = сеанс.idзал
         JOIN кинотеатр к on к.id = з.idкинотеатр
         JOIN фильм ф on ф.id = сеанс.idфильм
         JOIN режиссер р on р.id = ф.idрежиссер
ORDER BY ф.название, р.фио, ф.год, к.адрес, з.название, сеанс.датавремя"""
            c.execute(sql)
            return c.fetchall(), c.description

    def get_week_session(self):
        with self.conn.cursor() as c:
            sql = """SELECT *
FROM сеанс
WHERE датавремя < NOW() + INTERVAL 1 week"""
            c.execute(sql)
            return c.fetchall(), c.description

    def get_money(self):
        with self.conn.cursor() as c:
            sql = """select кинотеатр.id,
       кинотеатр.название as `Кинотеатр`,
       адрес              as `Адрес`,
       sum(a.цена)           `Ожидаемая выручка, руб.`
from кинотеатр
         join
     (select зал.idкинотеатр, сеанс.цена, билетнаместо.idпокупатель
      from сеанс
               join зал on сеанс.idзал = зал.id
               join билетнаместо on сеанс.id = билетнаместо.idсеанс
      where сеанс.датавремя > now()
        and сеанс.датавремя <= now() + interval 1 week
        and билетнаместо.idпокупатель is not null) a
     on кинотеатр.id = a.idкинотеатр
group by кинотеатр
order by sum(a.цена) desc, `Кинотеатр`;"""
            c.execute(sql)
            return c.fetchall(), c.description

    def get_cheap_session(self, money):
        with self.conn.cursor() as c:
            sql = """select кинотеатр.id,
       кинотеатр.название as `Кинотеатр`,
       адрес              as `Адрес`,
       min(a.цена)           `Минимальная цена билета`
from кинотеатр
         JOIN зал з on кинотеатр.id = з.idкинотеатр
         JOIN сеанс с on з.id = с.idзал
         join
     (select зал.idкинотеатр, сеанс.цена
      from сеанс
               join зал on сеанс.idзал = зал.id
      where сеанс.датавремя > now()
        and сеанс.датавремя <= now() + interval 1 week) a
     on кинотеатр.id = a.idкинотеатр
         JOIN (SELECT idсеанс, COUNT(id) as tot
               FROM билетнаместо
               WHERE idпокупатель IS NULL
               GROUP BY idсеанс) t on t.idсеанс = с.id
WHERE t.tot != 0
group by кинотеатр
having min(a.цена) <= %s
order by min(a.цена), `Кинотеатр`;"""
            c.execute(sql, money)
            return c.fetchall(), c.description

    def get_all_session_bycinematime(self, cinema, time):
        with self.conn.cursor() as c:
            sql = """SELECT сеанс.id,
       сеанс.датавремя as ' Дата',
       ф.название      as 'Фильм',
       р.фио           as 'Режиссер',
       ф.год           as 'Год',
       к.адрес         as 'Кинотеатр',
       сеанс.цена      as 'Стоимость',
       t.tot as 'Свободно'
FROM сеанс
         JOIN зал з on з.id = сеанс.idзал
         JOIN кинотеатр к on к.id = з.idкинотеатр
         JOIN фильм ф on ф.id = сеанс.idфильм
         JOIN режиссер р on р.id = ф.idрежиссер
         JOIN (SELECT idсеанс, COUNT(id) as tot
               FROM билетнаместо
               WHERE idпокупатель IS NULL
               GROUP BY idсеанс) t on t.idсеанс = сеанс.id
WHERE к.адрес = %s
  AND (date(сеанс.датавремя) = date(%s) and time(сеанс.датавремя) >= time('4:00')
    or date(сеанс.датавремя) = date(%s) + Interval 1 day and
       time(сеанс.датавремя) < time('4:00'))
  AND t.tot != 0
ORDER BY сеанс.датавремя, ф.название, р.фио, ф.год, к.адрес, з.название, сеанс.цена;"""
            c.execute(sql, (cinema, time, time))
            return c.fetchall(), c.description

    def get_all_session_byfilmtime(self, idfilm, time):
        with self.conn.cursor() as c:
            sql = """SELECT сеанс.id,
       к.адрес         as 'Кинотеатр',
       сеанс.датавремя as ' Дата',
       сеанс.цена as 'Стоимость',
       t.tot as 'Свободно'
FROM сеанс
         JOIN зал з on з.id = сеанс.idзал
         JOIN кинотеатр к on к.id = з.idкинотеатр
         JOIN (SELECT idсеанс, COUNT(id) as tot
               FROM билетнаместо
               WHERE idпокупатель IS NULL
               GROUP BY idсеанс) t on t.idсеанс = сеанс.id
WHERE сеанс.idфильм = %s
  AND (date(сеанс.датавремя) = date(%s) and time(сеанс.датавремя) >= time('4:00')
    or date(сеанс.датавремя) = date(%s) + Interval 1 day and
       time(сеанс.датавремя) < time('4:00'))
  AND t.tot != 0
ORDER BY к.адрес, сеанс.датавремя, сеанс.цена;"""
            c.execute(sql, (idfilm, time, time))
            return c.fetchall(), c.description

    def get_one_genre(self, id_):
        with self.conn.cursor() as c:
            sql = 'SELECT * FROM жанр WHERE id = %s'
            c.execute(sql, (id_,))
            return c.fetchone()

    def get_one_producer(self, id_):
        with self.conn.cursor() as c:
            sql = 'SELECT * FROM режиссер WHERE id = %s'
            c.execute(sql, (id_,))
            return c.fetchone()

    def get_one_restrict(self, id_):
        with self.conn.cursor() as c:
            sql = 'SELECT * FROM возрастноеограничение WHERE id = %s'
            c.execute(sql, (id_,))
            return c.fetchone()

    def get_one_typesess(self, id_):
        with self.conn.cursor() as c:
            sql = 'SELECT * FROM типсеанса WHERE id = %s'
            c.execute(sql, (id_,))
            return c.fetchone()

    def get_one_cinema(self, id_):
        with self.conn.cursor() as c:
            sql = 'SELECT * FROM кинотеатр WHERE id = %s'
            c.execute(sql, (id_,))
            return c.fetchone()

    def get_one_cinema1(self, idhall):
        with self.conn.cursor() as c:
            sql = 'SELECT к.* FROM зал JOIN кинотеатр к on к.id = зал.idкинотеатр WHERE зал.id = %s'
            c.execute(sql, (idhall,))
            return c.fetchone()

    def get_one_typehall(self, id_):
        with self.conn.cursor() as c:
            sql = 'SELECT * FROM типзала WHERE id = %s'
            c.execute(sql, (id_,))
            return c.fetchone()

    def get_one_hall(self, id_):
        with self.conn.cursor() as c:
            sql = 'SELECT * FROM зал WHERE id = %s'
            c.execute(sql, (id_,))
            return c.fetchone()

    def get_one_film(self, id_):
        with self.conn.cursor() as c:
            sql = 'SELECT * FROM фильм WHERE id = %s'
            c.execute(sql, (id_,))
            return c.fetchone()

    def get_one_session(self, id_):
        with self.conn.cursor() as c:
            sql = 'SELECT * FROM сеанс WHERE id = %s'
            c.execute(sql, (id_,))
            return c.fetchone()

    def get_id_genre(self, name):
        with self.conn.cursor() as c:
            sql = 'SELECT id FROM жанр WHERE название = %s'
            c.execute(sql, (name,))
            return c.fetchone()[0]

    def get_id_typehall2(self, hall, cinema):
        with self.conn.cursor() as c:
            sql = 'SELECT idтипзала FROM зал WHERE idкинотеатр = %s AND название = %s'
            c.execute(sql, (self.get_id_cinema(cinema), hall,))
            return c.fetchone()[0]

    def get_id_typehall(self, name):
        with self.conn.cursor() as c:
            sql = 'SELECT id FROM типзала WHERE название = %s'
            c.execute(sql, (name,))
            return c.fetchone()[0]

    def get_id_cinema(self, address):
        with self.conn.cursor() as c:
            sql = 'SELECT id FROM кинотеатр WHERE адрес = %s'
            c.execute(sql, (address,))
            return c.fetchone()[0]

    def get_id_producer(self, name):
        with self.conn.cursor() as c:
            sql = 'SELECT id FROM режиссер WHERE фио = %s'
            c.execute(sql, (name,))
            return c.fetchone()[0]

    def get_id_restrict(self, age):
        with self.conn.cursor() as c:
            sql = 'SELECT id FROM возрастноеограничение WHERE возраст = %s'
            c.execute(sql, (age,))
            return c.fetchone()[0]

    def get_id_hall(self, hall, cinema):
        with self.conn.cursor() as c:
            sql = '''SELECT зал.id 
            FROM зал JOIN кинотеатр к on к.id = зал.idкинотеатр 
            WHERE зал.название = %s AND к.адрес = %s'''
            c.execute(sql, (hall, cinema))
            return c.fetchone()[0]

    def get_film_genre(self, idfilm):
        with self.conn.cursor() as c:
            sql = 'SELECT ж.id FROM жанрыфильмов JOIN жанр ж on ж.id = жанрыфильмов.idжанр WHERE idфильм = %s'
            c.execute(sql, (idfilm,))
            return c.fetchall()

    def get_genre_film2(self, genre):
        with self.conn.cursor() as c:
            sql = '''SELECT DISTINCT ф.id,
       ф.название     as 'Название',
       ф.описание     as 'Описание',
       ф.год          as 'Год',
       ф.длительность as 'Длительность',
       возраст      as 'Ограничение',
       фио          as 'Режиссер'
FROM жанрыфильмов
         JOIN жанр ж on ж.id = жанрыфильмов.idжанр
         JOIN фильм ф on ф.id = жанрыфильмов.idфильм
         JOIN режиссер р on р.id = ф.idрежиссер
         JOIN возрастноеограничение в on в.id = ф.idвозраст
WHERE ж.название = %s'''
            c.execute(sql, (genre,))
            return c.fetchall(), c.description

    def get_film_typehall(self, idfilm):
        with self.conn.cursor() as c:
            sql = '''SELECT т.id
FROM форматыфильмов
         JOIN типзала т on т.id = форматыфильмов.idтипзала
WHERE idфильм = %s'''
            c.execute(sql, (idfilm,))
            return c.fetchall()

    def get_session_rowcol(self, idsess):
        with self.conn.cursor() as c:
            sql = 'SELECT числорядов, длинаряда FROM сеанс WHERE id = %s'
            c.execute(sql, (idsess,))
            return c.fetchone()

    def get_sessionplaces(self, idsess):
        with self.conn.cursor() as c:
            sql = 'SELECT номерряда, номерместа, idпокупатель FROM билетнаместо WHERE idсеанс = %s'
            c.execute(sql, (idsess,))
            return c.fetchall()

    def get_user_name_by_id(self, uid):
        with self.conn.cursor() as c:
            sql = "SELECT фио FROM покупатель WHERE id = %s"
            c.execute(sql, uid)
            return c.fetchone()[0]

    def get_user_tikets(self, uid):
        with self.conn.cursor() as c:
            sql = '''SELECT билетнаместо.id,
       с.датавремя as 'Дата',
       ф.название as 'Фильм',
       к.название as 'Кинотеатр',
       з.название as 'Зал',
       номерряда as 'Ряд',
       номерместа as 'Место',
       с.цена as 'Стоимость'
FROM билетнаместо
         JOIN сеанс с on с.id = билетнаместо.idсеанс
         JOIN фильм ф on ф.id = с.idфильм
         JOIN зал з on з.id = с.idзал
         JOIN кинотеатр к on к.id = з.idкинотеатр
WHERE idпокупатель = %s
ORDER BY 'Дата', 'Кинотеатр', 'Зал', 'Ряд', 'Место', 'Стоимость', 'Фильм' '''
            c.execute(sql, uid)
            return c.fetchall(), c.description

    def get_all_user_numbers(self):
        with self.conn.cursor() as c:
            sql = "SELECT фио, телефон FROM покупатель WHERE телефон IS NOT NULL "
            c.execute(sql)
            return c.fetchall()

    def get_all_filmshall(self, cinema, hall):
        with self.conn.cursor() as c:
            sql = "SELECT idфильм FROM форматыфильмов WHERE idтипзала = %s"
            c.execute(sql, (self.get_id_typehall2(hall, cinema)))
            return c.fetchall()

    def get_session_buyers(self, idsess):
        with self.conn.cursor() as c:
            sql = """SELECT п.id, п.фио, номерряда, номерместа
FROM билетнаместо
         JOIN покупатель п on п.id = билетнаместо.idпокупатель
WHERE idсеанс = %s
ORDER BY п.фио, номерряда, номерместа"""
            c.execute(sql, (idsess,))
            return c.fetchall(), c.description

    def get_variety(self):
        with self.conn.cursor() as c:
            sql = """select кинотеатр.id,
       кинотеатр.название as `Кинотеатр`,
       адрес              as `Адрес`,
       count(*)           as `Количество фильмов`
from кинотеатр
         join
     (select distinct зал.idкинотеатр, сеанс.idфильм
      from сеанс
               join зал on сеанс.idзал = зал.id
      where сеанс.датавремя > now()
        and сеанс.датавремя <= now() + interval 1 week) a
     on кинотеатр.id = a.idкинотеатр
group by кинотеатр
order by `Количество фильмов` desc, `Кинотеатр`;"""
            c.execute(sql)
            return c.fetchall(), c.description

    def add_user(self, name, email, number, hash_):
        try:
            with self.conn.cursor() as c:
                sql = 'INSERT INTO покупатель (фио, телефон, почта, хэш) VALUES( %s, %s, %s, %s)'
                c.execute(sql, (name, number, email, hash_))
                self.conn.commit()
                return c.lastrowid
        except pymysql.IntegrityError as e:
            code, message = e.args
            if code == 1062 and message[-6:] == 'почта\'':
                raise DBException(
                    "Пользователь с указанной почтой уже существует.") from e
            elif code == 1062 and message[-8:] == 'телефон\'':
                raise DBException(
                    "Пользователь с указанным номером телефона уже существует.") from e
            raise DBException("Не удалось зарегистрироваться.") from e
        except pymysql.OperationalError as e:
            _, message = e.args
            raise DBException(message) from e
        except pymysql.DataError as e:
            _, message = e.args
            if message[26:33] == 'телефон':
                raise DBException(
                    "Слишком длинный номер телефона. Введите его в соответствии с форматом +7xxxxxxxxxx.") from e
            raise DBException("Слишком длинные параметры ввода.") from e
        except Exception as e:
            raise DBException("Не удалось зарегистрироваться.") from e

    def add_genre(self, name):
        try:
            with self.conn.cursor() as c:
                sql = 'INSERT INTO жанр (название) VALUES( %s)'
                c.execute(sql, (name,))
                self.conn.commit()
        except pymysql.IntegrityError as e:
            code, *_ = e.args
            if code == 1062:
                raise DBException("Указанное название жанра уже существует.") from e
            raise DBException("Не удалось добавить жанр.") from e
        except pymysql.DataError as e:
            raise DBException("Слишком длинное название жанра.") from e
        except Exception as e:
            raise DBException("Не удалось добавить жанр.") from e

    def add_producer(self, name):
        try:
            with self.conn.cursor() as c:
                sql = 'INSERT INTO режиссер (фио) VALUES( %s)'
                c.execute(sql, (name,))
                self.conn.commit()
        except pymysql.IntegrityError as e:
            code, *_ = e.args
            if code == 1062:
                raise DBException("Указанное ФИО режиссера уже существует.") from e
            raise DBException("Не удалось добавить режиссера.") from e
        except pymysql.DataError as e:
            raise DBException("Слишком длинное ФИО режиссера.") from e
        except Exception as e:
            raise DBException("Не удалось добавить режиссера.") from e

    def add_restrict(self, name):
        try:
            with self.conn.cursor() as c:
                sql = 'INSERT INTO возрастноеограничение (возраст) VALUES( %s)'
                c.execute(sql, (name,))
                self.conn.commit()
        except pymysql.IntegrityError as e:
            code, *_ = e.args
            if code == 1062:
                raise DBException("Указанное ограничение уже существует.") from e
            raise DBException("Не удалось добавить ограничение.") from e
        except pymysql.DataError as e:
            raise DBException("Слишком длинное ограничение.") from e
        except pymysql.OperationalError as e:
            _, message = e.args
            raise DBException(message) from e
        except Exception as e:
            raise DBException("Не удалось добавить ограничение.") from e

    def add_typesess(self, name, begin, end, add):
        try:
            with self.conn.cursor() as c:
                sql = 'INSERT INTO типсеанса (название, времяначала, времяконца, надбавкасеанса) VALUES(%s, %s, %s, %s)'
                c.execute(sql, (name, begin, end, add,))
                self.conn.commit()
        except pymysql.IntegrityError as e:
            code, *_ = e.args
            if code == 1062:
                raise DBException("Указанное название типа сеанса уже существует.") from e
            raise DBException("Не удалось добавить тип сеанса.") from e
        except pymysql.DataError as e:
            raise DBException("Слишком название типа сеанса.") from e
        except pymysql.OperationalError as e:
            _, message = e.args
            raise DBException(message) from e
        except Exception as e:
            raise DBException("Не удалось добавить тип сеанса.") from e

    def add_cinema(self, name, address, price):
        try:
            with self.conn.cursor() as c:
                sql = 'INSERT INTO кинотеатр (название, адрес, базоваяцена) VALUES(%s, %s, %s)'
                c.execute(sql, (name, address, price,))
                self.conn.commit()
        except pymysql.IntegrityError as e:
            code, *_ = e.args
            if code == 1062:
                raise DBException("Указанный адрес кинотеатра уже существует.") from e
            raise DBException("Не удалось добавить кинотеатр.") from e
        except pymysql.DataError as e:
            raise DBException("Слишком название или адрес кинотеатра.") from e
        except pymysql.OperationalError as e:
            _, message = e.args
            raise DBException(message) from e
        except Exception as e:
            raise DBException("Не удалось добавить кинотеатр.") from e

    def add_typehall(self, name, price):
        try:
            with self.conn.cursor() as c:
                sql = 'INSERT INTO типзала (название, надбавказала) VALUES(%s, %s)'
                c.execute(sql, (name, price,))
                self.conn.commit()
        except pymysql.IntegrityError as e:
            code, *_ = e.args
            if code == 1062:
                raise DBException("Указанный тип зала уже существует.") from e
            raise DBException("Не удалось добавить тип зала.") from e
        except pymysql.DataError as e:
            raise DBException("Слишком длинное название типа зала.") from e
        except pymysql.OperationalError as e:
            _, message = e.args
            raise DBException(message) from e
        except Exception as e:
            raise DBException("Не удалось добавить тип зала.") from e

    def add_hall(self, name, length, number, typehall, cinema):
        try:
            with self.conn.cursor() as c:
                sql = '''INSERT INTO зал (название, длинаряда, числорядов, idтипзала, idкинотеатр)
VALUES (%s, %s, %s, %s, %s)'''
                c.execute(sql, (name, length, number, typehall, cinema,))
                self.conn.commit()
        except pymysql.IntegrityError as e:
            code, *_ = e.args
            if code == 1062:
                raise DBException("Указанное название зала уже существует.") from e
            raise DBException("Не удалось добавить зал.") from e
        except pymysql.DataError as e:
            raise DBException("Слишком длинное название зала.") from e
        except pymysql.OperationalError as e:
            _, message = e.args
            raise DBException(message) from e
        except Exception as e:
            raise DBException("Не удалось добавить зал.") from e

    def add_film(self, name, descript, year, duration,
                 idgenre, idproducer, idrestrict, idtypehall):
        try:
            with self.conn.cursor() as c:
                sql = '''INSERT INTO фильм (название, описание, год, длительность, idрежиссер, idвозраст)
VALUES (%s, %s, %s, %s, %s, %s)'''
                c.execute(sql, (name, descript, year, duration, idproducer, idrestrict))
                idf = c.lastrowid
                for idg in idgenre:
                    sql = '''INSERT INTO жанрыфильмов (idфильм, idжанр) VALUES (%s, %s)'''
                    c.execute(sql, (idf, idg))
                for idt in idtypehall:
                    sql = '''INSERT INTO форматыфильмов (idфильм, idтипзала) VALUES (%s, %s)'''
                    c.execute(sql, (idf, idt))
                self.conn.commit()
        except pymysql.IntegrityError as e:
            code, *_ = e.args
            if code == 1062:
                raise DBException(
                    "Фильм с заданным названием, годом и режиссером уже существует.") from e
            raise DBException("Не удалось добавить фильм.") from e
        except pymysql.DataError as e:
            raise DBException("Слишком длинное название или описание фильма.") from e
        except pymysql.OperationalError as e:
            _, message = e.args
            raise DBException(message) from e
        except Exception as e:
            raise DBException("Не удалось добавить фильм.") from e

    def add_session(self, hall, dateTime, film):
        try:
            with self.conn.cursor() as c:
                sql = 'INSERT INTO сеанс (датавремя, idзал, idфильм) VALUES(%s, %s, %s)'
                c.execute(sql, (dateTime, hall, film))
                self.conn.commit()
        except pymysql.IntegrityError as e:
            code, *_ = e.args
            if code == 1062:
                raise DBException("Указанный сеанс на дату и зал уже существует.") from e
            raise DBException("Не удалось добавить сеанс.") from e
        except pymysql.OperationalError as e:
            _, message = e.args
            raise DBException(message) from e
        except Exception as e:
            raise DBException("Не удалось добавить сеанс.") from e

    def buy_places(self, idsess, places, uid):
        try:
            with self.conn.cursor() as c:
                for pl in places:
                    sql = '''UPDATE билетнаместо 
                    SET idпокупатель = %s 
                    WHERE idсеанс = %s AND номерряда = %s AND номерместа = %s'''
                    c.execute(sql, (uid, idsess, pl[0], pl[1]))
                self.conn.commit()
        except Exception as e:
            raise DBException("Не удалось купить билеты. Попрообуйте снова.") from e

    def update_genre(self, gid, name):
        try:
            with self.conn.cursor() as c:
                sql = 'UPDATE жанр SET название = %s WHERE id = %s'
                c.execute(sql, (name, gid,))
                self.conn.commit()
        except pymysql.IntegrityError as e:
            code, *_ = e.args
            if code == 1062:
                raise DBException("Указанное название жанра уже существует.") from e
            raise DBException("Не удалось обновить жанр.") from e
        except pymysql.DataError as e:
            raise DBException("Слишком длинное название жанра.") from e
        except Exception as e:
            raise DBException("Не удалось обновить жанр.") from e

    def update_producer(self, gid, name):
        try:
            with self.conn.cursor() as c:
                sql = 'UPDATE режиссер SET фио = %s WHERE id = %s'
                c.execute(sql, (name, gid,))
                self.conn.commit()
        except pymysql.IntegrityError as e:
            code, *_ = e.args
            if code == 1062:
                raise DBException("Указанное ФИО режиссера уже существует.") from e
            raise DBException("Не удалось обновить ФИО режиссера.") from e
        except pymysql.DataError as e:
            raise DBException("Слишком длинное ФИО режиссера.") from e
        except Exception as e:
            raise DBException("Не удалось обновить ФИО режиссера.") from e

    def update_restrict(self, gid, name):
        try:
            with self.conn.cursor() as c:
                sql = 'UPDATE возрастноеограничение SET возраст = %s WHERE id = %s'
                c.execute(sql, (name, gid,))
                self.conn.commit()
        except pymysql.IntegrityError as e:
            code, *_ = e.args
            if code == 1062:
                raise DBException("Указанное ограничение уже существует.") from e
            raise DBException("Не удалось обновить ограничение.") from e
        except pymysql.DataError as e:
            raise DBException("Слишком длинное ограничение.") from e
        except pymysql.OperationalError as e:
            _, message = e.args
            raise DBException(message) from e
        except Exception as e:
            raise DBException("Не удалось обновить ограничение.") from e

    def update_typesess(self, gid, name, begin, end, add):
        try:
            with self.conn.cursor() as c:
                sql = '''UPDATE типсеанса 
                SET название = %s, времяначала = %s, времяконца = %s, надбавкасеанса = %s 
                WHERE id = %s'''
                c.execute(sql, (name, begin, end, add, gid,))
                self.conn.commit()
        except pymysql.IntegrityError as e:
            code, *_ = e.args
            if code == 1062:
                raise DBException("Указанное название типа сеанса уже существует.") from e
            raise DBException("Не удалось обновить тип сеанса.") from e
        except pymysql.DataError as e:
            raise DBException("Слишком длинное название типа сеанса.") from e
        except pymysql.OperationalError as e:
            _, message = e.args
            raise DBException(message) from e
        except Exception as e:
            raise DBException("Не удалось обновить тип сеанса.") from e

    def update_cinema(self, gid, name, address, price):
        try:
            with self.conn.cursor() as c:
                sql = 'UPDATE кинотеатр SET название = %s, адрес = %s, базоваяцена = %s WHERE id = %s'
                c.execute(sql, (name, address, price, gid,))
                self.conn.commit()
        except pymysql.IntegrityError as e:
            code, *_ = e.args
            if code == 1062:
                raise DBException("Указанный адрес кинотеатра уже существует.") from e
            raise DBException("Не удалось обновить кинотеатр.") from e
        except pymysql.DataError as e:
            raise DBException("Слишком длинное название или адрес кинотеатра.") from e
        except pymysql.OperationalError as e:
            _, message = e.args
            raise DBException(message) from e
        except Exception as e:
            raise DBException("Не удалось обновить кинотеатр.") from e

    def update_typehall(self, gid, name, price):
        try:
            with self.conn.cursor() as c:
                sql = 'UPDATE типзала SET название = %s, надбавказала = %s WHERE id = %s'
                c.execute(sql, (name, price, gid,))
                self.conn.commit()
        except pymysql.IntegrityError as e:
            code, *_ = e.args
            if code == 1062:
                raise DBException("Указанное название типа зала уже существует.") from e
            raise DBException("Не удалось обновить тип зала.") from e
        except pymysql.DataError as e:
            raise DBException("Слишком длинное название типа зала.") from e
        except pymysql.OperationalError as e:
            _, message = e.args
            raise DBException(message) from e
        except Exception as e:
            raise DBException("Не удалось обновить типа зала.") from e

    def update_hall(self, gid, name, length, number, typehall, cinema):
        try:
            with self.conn.cursor() as c:
                sql = '''UPDATE зал 
                SET название = %s, длинаряда = %s, числорядов = %s, idтипзала = %s, idкинотеатр = %s 
                WHERE id = %s'''
                c.execute(sql, (name, length, number, typehall, cinema, gid,))
                self.conn.commit()
        except pymysql.IntegrityError as e:
            code, *_ = e.args
            if code == 1062:
                raise DBException(
                    "Указанное название зала уже существует для выбранного кинотеатра.") from e
            raise DBException("Не удалось обновить зал.") from e
        except pymysql.DataError as e:
            raise DBException("Слишком длинное название зала.") from e
        except pymysql.OperationalError as e:
            _, message = e.args
            raise DBException(message) from e
        except Exception as e:
            raise DBException("Не удалось обновить зал.") from e

    def update_film(self, gid, name, descript, year, duration,
                    idgenre, idproducer, idrestrict, idtypehall):
        try:
            with self.conn.cursor() as c:
                sql = '''UPDATE фильм SET название = %s, описание = %s, год = %s, длительность = %s, idрежиссер = %s, idвозраст = %s
WHERE id = %s'''
                c.execute(sql,
                          (name, descript, year, duration, idproducer, idrestrict, gid))
                sql = 'DELETE FROM жанрыфильмов WHERE idфильм = %s'
                c.execute(sql, (gid,))
                for idg in idgenre:
                    sql = '''INSERT INTO жанрыфильмов (idфильм, idжанр) VALUES (%s, %s)'''
                    c.execute(sql, (gid, idg))
                sql = 'DELETE FROM форматыфильмов WHERE idфильм = %s'
                c.execute(sql, (gid,))
                for idt in idtypehall:
                    sql = '''INSERT INTO форматыфильмов (idфильм, idтипзала) VALUES (%s, %s)'''
                    c.execute(sql, (gid, idt))
                self.conn.commit()
        except pymysql.IntegrityError as e:
            code, *_ = e.args
            if code == 1062:
                raise DBException(
                    "Фильм с заданным названием, годом и режиссером уже существует.") from e
            raise DBException("Не удалось добавить фильм.") from e
        except pymysql.DataError as e:
            raise DBException("Слишком длинное название или описание фильма.") from e
        except pymysql.OperationalError as e:
            _, message = e.args
            raise DBException(message) from e
        except Exception as e:
            raise DBException("Не удалось добавить фильм.") from e

    def update_session(self, gid, hall, dateTime, film):
        try:
            with self.conn.cursor() as c:
                sql = 'UPDATE сеанс SET idзал = %s, датавремя = %s, idфильм = %s WHERE id = %s'
                c.execute(sql, (hall, dateTime, film, gid,))
                self.conn.commit()
        except pymysql.IntegrityError as e:
            code, *_ = e.args
            if code == 1062:
                raise DBException("Указанный сеанс на дату и зал уже существует.") from e
            raise DBException("Не удалось обновить сеанс.") from e
        except pymysql.OperationalError as e:
            _, message = e.args
            raise DBException(message) from e
        except Exception as e:
            raise DBException("Не удалось обновить сеанс.") from e

    def check_for_email(self, email):
        with self.conn.cursor() as c:
            sql = "SELECT id, хэш FROM покупатель WHERE почта = %s"
            c.execute(sql, email)
            return c.rowcount, c.fetchone()

    def check_hallincinema(self, hall, cinema):
        with self.conn.cursor() as c:
            sql = "SELECT id FROM зал WHERE idкинотеатр = %s AND название = %s"
            c.execute(sql, (self.get_id_cinema(cinema), hall))
            return c.rowcount

    def number_cinemasession(self, cinema):
        with self.conn.cursor() as c:
            sql = """SELECT *
FROM сеанс
         JOIN зал з on з.id = сеанс.idзал
         JOIN фильм ф on ф.id = сеанс.idфильм
WHERE idкинотеатр = %s
  AND сеанс.датавремя + ф.длительность >= NOW()"""
            c.execute(sql, (cinema))
            return c.rowcount

    def number_hallsession(self, hall):
        with self.conn.cursor() as c:
            sql = """SELECT *
FROM сеанс
         JOIN фильм ф on ф.id = сеанс.idфильм
WHERE idзал = %s
  AND сеанс.датавремя + ф.длительность >= NOW()"""
            c.execute(sql, (hall))
            return c.rowcount

    def number_bue_session(self, idsess):
        with self.conn.cursor() as c:
            sql = "SELECT id FROM билетнаместо WHERE idсеанс = %s AND idпокупатель IS NOT NUll"
            c.execute(sql, (idsess))
            return c.rowcount

    def number_film_session(self, idfilm):
        with self.conn.cursor() as c:
            sql = """SELECT *
FROM сеанс
         JOIN фильм ф on ф.id = сеанс.idфильм
WHERE idфильм = %s
  and датавремя + ф.длительность >= NOW()"""
            c.execute(sql, (idfilm))
            return c.rowcount

    def session_is_now(self, idsession):
        with self.conn.cursor() as c:
            sql = """SELECT *
FROM сеанс
         JOIN фильм ф on ф.id = сеанс.idфильм
WHERE сеанс.id = %s
  and датавремя + ф.длительность >= NOW() 
  and датавремя < NOW()"""
            c.execute(sql, (idsession))
            return c.rowcount

    def delete_one_genre(self, id_):
        try:
            with self.conn.cursor() as c:
                sql = 'DELETE FROM жанр WHERE id = %s'
                c.execute(sql, (id_,))
                self.conn.commit()
        except pymysql.IntegrityError as e:
            code, *_ = e.args
            if code == 1451:
                raise DBException(
                    "В удалении отказано. На указанный жанр уже созданы фильмы.") from e
            raise DBException("Не удалось удалить жанр.") from e
        except Exception as e:
            raise DBException("Не удалось удалить жанр.") from e

    def delete_one_producer(self, id_):
        try:
            with self.conn.cursor() as c:
                sql = 'DELETE FROM режиссер WHERE id = %s'
                c.execute(sql, (id_,))
                self.conn.commit()
        except pymysql.IntegrityError as e:
            code, *_ = e.args
            if code == 1451:
                raise DBException(
                    "В удалении отказано. На указанного режиссера уже созданы фильмы.") from e
            raise DBException("Не удалось удалить режиссера.") from e
        except Exception as e:
            raise DBException("Не удалось удалить режиссера.") from e

    def delete_one_restrict(self, id_):
        try:
            with self.conn.cursor() as c:
                sql = 'DELETE FROM возрастноеограничение WHERE id = %s'
                c.execute(sql, (id_,))
                self.conn.commit()
        except pymysql.IntegrityError as e:
            code, *_ = e.args
            if code == 1451:
                raise DBException(
                    "В удалении отказано. На указанное ограничение уже созданы фильмы.") from e
            raise DBException("Не удалось удалить ограничение.") from e
        except Exception as e:
            raise DBException("Не удалось удалить ограничение.") from e

    def delete_one_typesess(self, id_):
        try:
            with self.conn.cursor() as c:
                sql = 'DELETE FROM типсеанса WHERE id = %s'
                c.execute(sql, (id_,))
                self.conn.commit()
        except Exception as e:
            raise DBException("Не удалось удалить тип сеанса.") from e

    def delete_one_cinema(self, id_):
        try:
            with self.conn.cursor() as c:
                sql = 'DELETE FROM зал WHERE idкинотеатр = %s'
                c.execute(sql, (id_,))
                sql = 'DELETE FROM кинотеатр WHERE id = %s'
                c.execute(sql, (id_,))
                self.conn.commit()
        except Exception as e:
            raise DBException("Не удалось удалить кинотеатр.") from e

    def delete_one_typehall(self, id_):
        try:
            with self.conn.cursor() as c:
                sql = 'DELETE FROM типзала WHERE id = %s'
                c.execute(sql, (id_,))
                self.conn.commit()
        except pymysql.IntegrityError as e:
            code, *_ = e.args
            if code == 1451:
                raise DBException(
                    "В удалении отказано. На указанный тип зала уже созданы залы или фильмы.") from e
            raise DBException("Не удалось удалить тип зала.") from e
        except Exception as e:
            raise DBException("Не удалось удалить тип зала.") from e

    def delete_one_hall(self, id_):
        try:
            with self.conn.cursor() as c:
                sql = 'DELETE FROM зал WHERE id = %s'
                c.execute(sql, (id_,))
                self.conn.commit()
        except Exception as e:
            raise DBException("Не удалось удалить зал.") from e

    def delete_one_film(self, id_):
        try:
            with self.conn.cursor() as c:
                sql = 'DELETE FROM жанрыфильмов WHERE idфильм = %s'
                c.execute(sql, (id_,))
                sql = 'DELETE FROM форматыфильмов WHERE idфильм = %s'
                c.execute(sql, (id_,))
                sql = 'DELETE FROM фильм WHERE id = %s'
                c.execute(sql, (id_,))
                self.conn.commit()
        except Exception as e:
            raise DBException("Не удалось удалить фильм.") from e

    def delete_old_session(self):
        try:
            with self.conn.cursor() as c:
                sql = """DELETE б
FROM билетнаместо б
         JOIN сеанс с ON б.idсеанс = с.id
         JOIN фильм ф on ф.id = с.idфильм
WHERE с.датавремя + ф.длительность < NOW()"""
                c.execute(sql, )
                sql = """DELETE c
FROM сеанс c
         JOIN фильм ф on ф.id = c.idфильм
WHERE датавремя + ф.длительность < NOW()"""
                c.execute(sql, )
                self.conn.commit()
        except Exception as e:
            raise DBException("Не удалось удалить устаревшие сеансы.") from e

    def delete_one_session(self, id_):
        try:
            with self.conn.cursor() as c:
                sql = 'DELETE FROM билетнаместо WHERE idсеанс = %s'
                c.execute(sql, (id_,))
                sql = 'DELETE FROM сеанс WHERE id = %s'
                c.execute(sql, (id_,))
                self.conn.commit()
        except Exception as e:
            raise DBException("Не удалось удалить сеанс.") from e
