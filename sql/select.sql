select фильм.название as фильм, фильм.длительность, типзала.название as формат, фильм.id, типзала.id
from форматыфильмов join фильм on форматыфильмов.idфильм = фильм.id
join типзала on форматыфильмов.idтипзала = типзала.id
where типзала.id = 1
order by фильм.id;


select * from сеанс;
select * from билетнаместо;
select * from фильм
order by год;