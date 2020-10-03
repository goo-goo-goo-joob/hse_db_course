DROP trigger IF EXISTS check_покупатель;
DROP PROCEDURE IF EXISTS procedure_сеанс;
DROP trigger IF EXISTS check_сеанс1;
DROP trigger IF EXISTS check_сеанс2;
DROP trigger IF EXISTS create_сеанс1;
DROP trigger IF EXISTS create_сеанс2;
DROP trigger IF EXISTS update_сеанс;
DROP PROCEDURE IF EXISTS procedure_ограничение;
DROP trigger IF EXISTS check_ограничение1;
DROP trigger IF EXISTS check_ограничение2;
DROP PROCEDURE IF EXISTS procedure_типсеанса;
DROP trigger IF EXISTS check_типсеанса1;
DROP trigger IF EXISTS check_типсеанса2;


DELIMITER $$
CREATE TRIGGER check_покупатель
    BEFORE INSERT
    ON покупатель
    FOR EACH ROW
BEGIN
    IF (NEW.почта REGEXP '^[A-Za-z0-9._-]+@[A-Za-z0-9.-]+$') = 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Введите существующую электронную почту.';
    END IF;
    IF (NEW.телефон REGEXP '^[+][7][0-9]{10}') = 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT =
                    'Введите существующий номер телефона соответствии с форматом +7xxxxxxxxxx.';
    END IF;
END;
$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE procedure_ограничение(IN возраст VARCHAR(3))
BEGIN
    IF (возраст REGEXP '^[1-9]?[0-9][+]$') = 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Введите ограничение в соответствии с форматом x+.';
    END IF;
END;
$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER check_ограничение1
    BEFORE INSERT
    ON возрастноеограничение
    FOR EACH ROW
BEGIN
    CALL procedure_ограничение(NEW.возраст);
END;
$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER check_ограничение2
    BEFORE UPDATE
    ON возрастноеограничение
    FOR EACH ROW
BEGIN
    CALL procedure_ограничение(NEW.возраст);
END;
$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE procedure_типсеанса(IN начало time, конец time, id_ int)
BEGIN
    DECLARE времясвободно_ int unsigned;

    IF начало >= конец THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT =
                    'Время начала типа сеанса должно быть меньше времени конца сеанса.';
    END IF;

    SELECT COUNT(*)
    INTO времясвободно_
    FROM типсеанса
    WHERE типсеанса.id != id_
      AND ((начало > типсеанса.времяначала AND
            начало < типсеанса.времяконца) OR
           (конец > типсеанса.времяначала AND
            конец < типсеанса.времяконца));

    IF (времясвободно_ > 0) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT =
                    'Указанное время уже принадлежит другому типу сеанса.';
    END IF;
END;
$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER check_типсеанса1
    BEFORE INSERT
    ON типсеанса
    FOR EACH ROW
BEGIN
    CALL procedure_типсеанса(NEW.времяначала, NEW.времяконца, -1);
END;
$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER check_типсеанса2
    BEFORE UPDATE
    ON типсеанса
    FOR EACH ROW
BEGIN
    CALL procedure_типсеанса(NEW.времяначала, NEW.времяконца, NEW.id);
END;
$$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE procedure_сеанс(IN idфильм_ int, датавремя_ datetime,
                                 idзал_ int, id_ int)
BEGIN
    DECLARE длительность_ time;
    DECLARE свободно_ int unsigned;

    SELECT фильм.длительность
    INTO длительность_
    FROM фильм
    WHERE фильм.id = idфильм_;

    IF (датавремя_ < NOW()) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Дата и время сеанса меньше текущего времени.';
    END IF;

    SELECT COUNT(*)
    INTO свободно_
    FROM сеанс
             LEFT JOIN фильм ф on сеанс.idфильм = ф.id
    WHERE idзал_ = сеанс.idзал
      AND сеанс.id != id_
      AND ((датавремя_ > сеанс.датавремя AND
            датавремя_ < сеанс.датавремя + ф.длительность) OR
           (датавремя_ + длительность_ > сеанс.датавремя AND
            датавремя_ + длительность_ < сеанс.датавремя + ф.длительность));

    IF (свободно_ > 0) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT =
                    'В указанном зале уже проходит сеанс на установленное время.';
    END IF;
END;
$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER check_сеанс1
    BEFORE INSERT
    ON сеанс
    FOR EACH ROW
BEGIN
    CALL procedure_сеанс(NEW.idфильм, NEW.датавремя, NEW.idзал, -1);
END;
$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER check_сеанс2
    BEFORE UPDATE
    ON сеанс
    FOR EACH ROW
BEGIN
    CALL procedure_сеанс(NEW.idфильм, NEW.датавремя, NEW.idзал, NEW.id);
END;
$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER create_сеанс1
    BEFORE INSERT
    ON сеанс
    FOR EACH ROW
BEGIN
    DECLARE надбавкасеанса_ int unsigned;
    DECLARE надбавказала_ int unsigned;
    DECLARE базоваяцена_ int unsigned;
    DECLARE макс_ряд_ int unsigned;
    DECLARE макс_место_ int unsigned;

    SELECT типсеанса.надбавкасеанса
    INTO надбавкасеанса_
    FROM типсеанса
    WHERE типсеанса.времяначала <= TIME(NEW.датавремя)
      and типсеанса.времяконца >= TIME(NEW.датавремя);

    SELECT типзала.надбавказала
    INTO надбавказала_
    FROM типзала
    WHERE типзала.id = (
        SELECT зал.idтипзала
        FROM зал
        WHERE зал.id = NEW.idзал);

    SELECT кинотеатр.базоваяцена
    INTO базоваяцена_
    FROM кинотеатр
    WHERE кинотеатр.id = (
        SELECT зал.idкинотеатр
        FROM зал
        WHERE зал.id = NEW.idзал);

    SET @цена = IFNULL(надбавкасеанса_, 0) + надбавказала_ + базоваяцена_;

    SELECT числорядов
    INTO макс_ряд_
    FROM зал
    WHERE зал.id = NEW.idзал;

    SELECT длинаряда
    INTO макс_место_
    FROM зал
    WHERE зал.id = NEW.idзал;

    SET new.цена = @цена;
    SET new.длинаряда = макс_место_;
    SET new.числорядов = макс_ряд_;
END;
$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER create_сеанс2
    AFTER INSERT
    ON сеанс
    FOR EACH ROW
BEGIN
    SET @ряд = 1, @место = 1;

    SET @макс_ряд_ = NEW.числорядов;
    SET @макс_место_ = NEW.длинаряда;

    while @ряд <= @макс_ряд_
        do
            while @место <= @макс_место_
                do
                    INSERT INTO билетнаместо (номерместа, номерряда, idсеанс)
                    VALUES (@место, @ряд, NEW.id);
                    set @место = @место + 1;
                end while;
            set @место = 1;
            set @ряд = @ряд + 1;
        end while;
END;
$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER update_сеанс
    BEFORE UPDATE
    ON сеанс
    FOR EACH ROW
BEGIN
    DECLARE надбавкасеанса_ int unsigned;
    DECLARE надбавказала_ int unsigned;
    DECLARE базоваяцена_ int unsigned;
    DECLARE макс_ряд_ int unsigned;
    DECLARE макс_место_ int unsigned;

    SELECT типсеанса.надбавкасеанса
    INTO надбавкасеанса_
    FROM типсеанса
    WHERE типсеанса.времяначала <= TIME(NEW.датавремя)
      and типсеанса.времяконца >= TIME(NEW.датавремя);

    SELECT типзала.надбавказала
    INTO надбавказала_
    FROM типзала
    WHERE типзала.id = (
        SELECT зал.idтипзала
        FROM зал
        WHERE зал.id = NEW.idзал);

    SELECT кинотеатр.базоваяцена
    INTO базоваяцена_
    FROM кинотеатр
    WHERE кинотеатр.id = (
        SELECT зал.idкинотеатр
        FROM зал
        WHERE зал.id = NEW.idзал);

    SET @цена = IFNULL(надбавкасеанса_, 0) + надбавказала_ + базоваяцена_;

    SELECT числорядов
    INTO макс_ряд_
    FROM зал
    WHERE зал.id = NEW.idзал;

    SELECT длинаряда
    INTO макс_место_
    FROM зал
    WHERE зал.id = NEW.idзал;

    SET new.цена = @цена;
    SET new.длинаряда = макс_место_;
    SET new.числорядов = макс_ряд_;

    DELETE from билетнаместо WHERE idсеанс = new.id;

    SET @ряд = 1, @место = 1;

    SET @макс_ряд_ = NEW.числорядов;
    SET @макс_место_ = NEW.длинаряда;

    while @ряд <= @макс_ряд_
        do
            while @место <= @макс_место_
                do
                    INSERT INTO билетнаместо (номерместа, номерряда, idсеанс)
                    VALUES (@место, @ряд, NEW.id);
                    set @место = @место + 1;
                end while;
            set @место = 1;
            set @ряд = @ряд + 1;
        end while;
END;
$$
DELIMITER ;