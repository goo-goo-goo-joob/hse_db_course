# GROUP BY и SORT сколько разных фильмов идет в ближайшую неделю в каждом кинотеатре (отсортировать в порядке убывания)
# входных данных нет
select кинотеатр.название as `Кинотеатр`, адрес as `Адрес`, count(*) as `Количество фильмов`
from кинотеатр join
(select distinct зал.idкинотеатр, сеанс.idфильм
from сеанс join зал on сеанс.idзал = зал.id
where сеанс.датавремя > now() and сеанс.датавремя <= now() + interval 1 week) a
on кинотеатр.id = a.idкинотеатр
group by кинотеатр
order by `Количество фильмов` desc, `Кинотеатр`;

# HAVING - вывести те кинотеатры, в которых минимальная цена билета на ближайшую неделю не больше заданного значения
# вход - максимальная цена price
drop procedure if exists func1;
delimiter $$

create procedure func1(price int unsigned)
begin
select кинотеатр.название as `Кинотеатр`, адрес as `Адрес`, min(a.цена) `Минимальная цена билета`
from кинотеатр join
(select зал.idкинотеатр, сеанс.цена
from сеанс join зал on сеанс.idзал = зал.id
where сеанс.датавремя > now() and сеанс.датавремя <= now() + interval 1 week) a
on кинотеатр.id = a.idкинотеатр
group by кинотеатр
having min(a.цена) <= price
order by min(a.цена), `Кинотеатр`;
end $$

delimiter ;

call func1(300);

# SUM - *для админки* ожидаемая выручка по кинотеатрам за ближайшую неделю
# входных данных нет
select кинотеатр.название as `Кинотеатр`, адрес as `Адрес`, sum(a.цена) `Ожидаемая выручка, руб.`
from кинотеатр join
(select зал.idкинотеатр, сеанс.цена, билетнаместо.idпокупатель
from сеанс join зал on сеанс.idзал = зал.id
join билетнаместо on сеанс.id = билетнаместо.idсеанс
where сеанс.датавремя > now() and сеанс.датавремя <= now() + interval 2 day
and билетнаместо.idпокупатель is not null) a
on кинотеатр.id = a.idкинотеатр
group by кинотеатр
order by sum(a.цена) desc, `Кинотеатр`;

select * from типзала;
select * from кинотеатр;
select * from типсеанса;
select * from жанр;
select * from режиссер order by id;
select * from возрастноеограничение order by id;
select * from фильм;
select * from зал;
select * from форматыфильмов;
select * from жанрыфильмов;
select * from покупатель;
select * from сеанс;
select * from билетнаместо;
