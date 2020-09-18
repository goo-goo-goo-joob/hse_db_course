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
    телефон varchar(25)  unique,
    почта   varchar(100) not null unique
);

DELIMITER $$
CREATE TRIGGER trig_mail_check
    BEFORE INSERT
    ON покупатель
    FOR EACH ROW
BEGIN
    IF (NEW.почта REGEXP '^[A-Za-z0-9._-]+@[A-Za-z0-9.-]+$') = 0 THEN
        SIGNAL SQLSTATE '01001'
            SET MESSAGE_TEXT = 'Введите существующую электронную почту';
    END IF;
END$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER trig_phone_check
    BEFORE INSERT
    ON покупатель
    FOR EACH ROW
BEGIN
    IF (NEW.телефон REGEXP '^\\+[0-9][[:space:]-][0-9]{3}-?[0-9]{2}-?[0-9]{2}$') = 0 THEN
        SIGNAL SQLSTATE '01002'
            SET MESSAGE_TEXT = 'Введите существующий номер телефона';
    END IF;
END$$
DELIMITER ;

create table типзала
(
    id       int primary key auto_increment,
    название varchar(100) not null unique
);

create table кинотеатр
(
    id       int primary key auto_increment,
    название varchar(100) not null,
    адрес    varchar(100) not null unique
);

create table типсеанса
(
    id       int primary key auto_increment,
    название varchar(100) not null unique
);

create table жанр
(
    id       int primary key auto_increment,
    название varchar(100) not null unique
);

create table режиссер
(
    id  int primary key auto_increment,
    фио varchar(100) not null unique
);

create table возрастноеограничение
(
    id      int primary key auto_increment,
    возраст numeric(2, 0) not null unique
);

create table фильм
(
    id           int primary key auto_increment,
    название     varchar(100)  not null,
    описание     varchar(500)  not null,
    год          numeric(4, 0) not null,
    длительность time          not null,
    idрежиссер   int           not null,
    idвозраст    int           not null,
    constraint режиссер_fk
        foreign key (idрежиссер) references режиссер (id),
    constraint возраст_fk
        foreign key (idвозраст) references возрастноеограничение (id),
    unique (название, год, idрежиссер)
);

create table зал
(
    id          int primary key auto_increment,
    название    varchar(100) not null,
    длинаряда   int unsigned not null,
    числорядов  int unsigned not null,
    idтипзала   int          not null,
    idкинотеатр int          not null,
    constraint типзала_fk
        foreign key (idтипзала) references типзала (id),
    constraint кинотеатр_fk
        foreign key (idкинотеатр) references кинотеатр (id),
    unique (название, idкинотеатр)
);

create table сеанс
(
    id          int primary key auto_increment,
    датавремя   datetime not null,
    idзал       int      not null,
    idтипсеанса int      not null,
    idфильм     int      not null,
    constraint зал_fk
        foreign key (idзал) references зал (id),
    constraint типсеанса_fk
        foreign key (idтипсеанса) references типсеанса (id),
    constraint фильм_fk
        foreign key (idфильм) references фильм (id),
    unique (датавремя, idзал)
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
        foreign key (idсеанс) references сеанс (id),
    unique (номерместа, номерряда, idсеанс)
);

create table форматыфильмов
(
    id        int primary key auto_increment,
    idфильм   int not null,
    idтипзала int not null,
    constraint фильмформат_fk
        foreign key (idфильм) references фильм (id),
    constraint типформат_fk
        foreign key (idтипзала) references типзала (id),
    unique (idфильм, idтипзала)
);

create table жанрыфильмов
(
    id      int primary key auto_increment,
    idфильм int not null,
    idжанр  int not null,
    constraint фильмжанр_fk
        foreign key (idфильм) references фильм (id),
    constraint жанрфильм_fk
        foreign key (idжанр) references жанр (id),
    unique (idфильм, idжанр)
);