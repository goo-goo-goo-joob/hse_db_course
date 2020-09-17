DROP table IF EXISTS жанрыфильмов;
DROP table IF EXISTS форматыфильмов;
DROP table IF EXISTS билетнаместо;
DROP table IF EXISTS сеанс;
DROP table IF EXISTS зал;
DROP table IF EXISTS фильм;
DROP table IF EXISTS покупатель;
DROP table IF EXISTS типзала;
DROP table IF EXISTS кинотеатр;
DROP table IF EXISTS типсеанса;
DROP table IF EXISTS жанр;
DROP table IF EXISTS режиссер;
DROP table IF EXISTS возрастноеограничение;

create table покупатель
(
    id      int primary key auto_increment,
    фио     varchar(100) not null,
    телефон varchar(25),
    почта   varchar(100)
);

create table типзала
(
    id       int primary key auto_increment,
    название varchar(100) not null
);

create table кинотеатр
(
    id       int primary key auto_increment,
    название varchar(100) not null,
    адрес    varchar(100) not null
);

create table типсеанса
(
    id       int primary key auto_increment,
    название varchar(100) not null
);

create table жанр
(
    id       int primary key auto_increment,
    название varchar(100) not null
);

create table режиссер
(
    id  int primary key auto_increment,
    фио varchar(100) not null
);

create table возрастноеограничение
(
    id      int primary key auto_increment,
    возраст varchar(100) not null
);

create table фильм
(
    id         int primary key auto_increment,
    название   varchar(100) not null,
    описание   varchar(500) not null,
    idрежиссер int          not null,
    idвозраст  int          not null,
    constraint режиссер_fk
        foreign key (idрежиссер) references режиссер (id),
    constraint возраст_fk
        foreign key (idвозраст) references возрастноеограничение (id)
);

create table зал
(
    id          int primary key auto_increment,
    название    varchar(100) not null,
    длинаряда   int          not null,
    числорядов  int          not null,
    idтипзала   int          not null,
    idкинотеатр int          not null,
    constraint типзала_fk
        foreign key (idтипзала) references типзала (id),
    constraint кинотеатр_fk
        foreign key (idкинотеатр) references кинотеатр (id)
);

create table сеанс
(
    id          int primary key auto_increment,
    дата        date not null,
    время       time not null,
    idзал       int  not null,
    idтипсеанса int  not null,
    idфильм     int  not null,
    constraint зал_fk
        foreign key (idзал) references зал (id),
    constraint типсеанса_fk
        foreign key (idтипсеанса) references типсеанса (id),
    constraint фильм_fk
        foreign key (idфильм) references фильм (id)
);

create table билетнаместо
(
    id           int primary key auto_increment,
    номерместа   int not null,
    номерряда    int not null,
    цена         int not null,
    idпокупатель int,
    idсеанс      int not null,
    constraint покупатель_fk
        foreign key (idпокупатель) references покупатель (id),
    constraint сеанс_fk
        foreign key (idсеанс) references сеанс (id)
);

create table форматыфильмов
(
    id        int primary key auto_increment,
    idфильм   int not null,
    idтипзала int not null,
    constraint фильмформат_fk
        foreign key (idфильм) references фильм (id),
    constraint типформат_fk
        foreign key (idтипзала) references типзала (id)
);

create table жанрыфильмов
(
    id      int primary key auto_increment,
    idфильм int not null,
    idжанр  int not null,
    constraint фильмжанр_fk
        foreign key (idфильм) references фильм (id),
    constraint жанрфильм_fk
        foreign key (idжанр) references жанр (id)
);