SELECT DISTINCT ж.id, ж.название
FROM жанрыфильмов
         JOIN жанр ж on ж.id = жанрыфильмов.idжанр
WHERE idфильм = 11
ORDER BY ж.название;

SELECT *
FROM возрастноеограничение
ORDER BY CHAR_LENGTH(возраст), возраст;

SELECT DISTINCT(кинотеатр.адрес)
FROM кинотеатр
         JOIN зал з on кинотеатр.id = з.idкинотеатр
         JOIN типзала т on т.id = з.idтипзала
         JOIN форматыфильмов ф on т.id = ф.idтипзала
WHERE ф.idфильм = 12
ORDER BY кинотеатр.название, адрес;

SELECT DISTINCT (зал.название)
FROM зал
         JOIN форматыфильмов ф on зал.idтипзала = ф.idтипзала
         JOIN кинотеатр к on к.id = зал.idкинотеатр
WHERE к.адрес = "пос. Воскресенское, Чечерский пр., 51"
  and ф.idфильм = 3;
  
SELECT фильм.id,
       название as 'Название',
       описание as 'Описание',
       год as 'Год',
       длительность as 'Длительность',
       возраст as 'Ограничение',
       фио as 'Режиссер'
FROM фильм
         JOIN возрастноеограничение в on в.id = фильм.idвозраст
         JOIN режиссер р on р.id = фильм.idрежиссер
WHERE описание LIKE '%Матрица%' OR название LIKE '%Матрица%'
ORDER BY название, год, р.фио;


SELECT фильм.id,
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
ORDER BY название, год, р.фио;

SELECT *
FROM сеанс
WHERE датавремя < NOW() + INTERVAL 1 week;

select кинотеатр.id,
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
order by sum(a.цена) desc, `Кинотеатр`;

select кинотеатр.id,
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
having min(a.цена) <= 300
order by min(a.цена), `Кинотеатр`;

SELECT сеанс.id,
       ф.название      as 'Фильм',
       р.фио           as 'Режиссер',
       ф.год           as 'Год',
       к.адрес         as 'Кинотеатр',
       сеанс.датавремя as ' Дата',
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
WHERE к.адрес = 'ул. Маршала Бирюзова, 32'
  AND (date(сеанс.датавремя) = date('2020-10-10') and time(сеанс.датавремя) >= time('4:00')
    or date(сеанс.датавремя) = date('2020-10-10') + Interval 1 day and
       time(сеанс.датавремя) < time('4:00'))
  AND t.tot != 0
ORDER BY ф.название, р.фио, ф.год, к.адрес, з.название, сеанс.датавремя, сеанс.цена;

SELECT сеанс.id,
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
WHERE сеанс.idфильм = 3
  AND (date(сеанс.датавремя) = date('2020-10-10') and time(сеанс.датавремя) >= time('4:00')
    or date(сеанс.датавремя) = date('2020-10-10') + Interval 1 day and
       time(сеанс.датавремя) < time('4:00'))
  AND t.tot != 0
ORDER BY к.адрес, сеанс.датавремя, сеанс.цена;

SELECT т.id
FROM форматыфильмов
         JOIN типзала т on т.id = форматыфильмов.idтипзала
WHERE idфильм = 3;

SELECT п.id, п.фио, номерряда, номерместа
FROM билетнаместо
         JOIN покупатель п on п.id = билетнаместо.idпокупатель
WHERE idсеанс = 100
ORDER BY п.фио, номерряда, номерместа;

select кинотеатр.id,
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
order by `Количество фильмов` desc, `Кинотеатр`;

SELECT *
FROM сеанс
         JOIN фильм ф on ф.id = сеанс.idфильм
WHERE сеанс.id = 200
  and датавремя + ф.длительность >= NOW() 
  and датавремя < NOW();

