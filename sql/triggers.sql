DROP trigger IF EXISTS check_покупатель;
DROP PROCEDURE IF EXISTS procedure_сеанс;
DROP trigger IF EXISTS check_сеанс1;
DROP trigger IF EXISTS check_сеанс2;
DROP trigger IF EXISTS create_сеанс;
DROP PROCEDURE IF EXISTS procedure_ограничение;
DROP trigger IF EXISTS check_ограничение1;
DROP trigger IF EXISTS check_ограничение2;


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
    IF (возраст REGEXP '^[1-9]?[0-9][+]') = 0 THEN
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
CREATE PROCEDURE procedure_сеанс(IN idфильм_ int, датавремя_ time,
                                 idзал_ int)
BEGIN
    DECLARE длительность_ time;
    DECLARE свободно_ int unsigned;

    SELECT фильм.длительность
    INTO длительность_
    FROM фильм
    WHERE фильм.id = idфильм_;

    IF (датавремя_ < NOW()) = 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Дата и время сеанса меньше текщего времени.';
    END IF;

    SELECT COUNT(*)
    INTO свободно_
    FROM сеанс
             LEFT JOIN фильм ф on сеанс.idфильм = ф.id
    WHERE idзал_ = сеанс.idзал
      AND ((датавремя_ > сеанс.датавремя AND
            датавремя_ < сеанс.датавремя + ф.длительность) OR
           (датавремя_ + длительность_ > сеанс.датавремя AND
            датавремя_ + длительность_ < сеанс.датавремя + ф.длительность));

    IF (свободно_ = 0) THEN
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
    CALL procedure_сеанс(NEW.idфильм, NEW.датавремя, NEW.idзал);
END;
$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER check_сеанс2
    BEFORE UPDATE
    ON сеанс
    FOR EACH ROW
BEGIN
    CALL procedure_сеанс(NEW.idфильм, NEW.датавремя, NEW.idзал);
END;
$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER create_сеанс
    AFTER INSERT
    ON сеанс
    FOR EACH ROW
BEGIN
    DECLARE типсеанса_ int unsigned;
    DECLARE надбавкасеанса_ int unsigned;
    DECLARE надбавказала_ int unsigned;
    DECLARE базоваяцена_ int unsigned;
    DECLARE макс_ряд_ int unsigned;
    DECLARE макс_место_ int unsigned;

    SELECT типсеанса.id, типсеанса.надбавкасеанса
    INTO типсеанса_, надбавкасеанса_
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

    SET @цена = надбавкасеанса_ + надбавказала_ + базоваяцена_;

    UPDATE сеанс
    SET цена        = @цена,
        idтипсеанса = @типсеанса
    WHERE id = NEW.id;

    SET @ряд = 1, @место = 1;

    SELECT числорядов
    INTO макс_ряд_
    FROM зал
    WHERE зал.id = NEW.idзал;

    SELECT длинаряда
    INTO макс_место_
    FROM зал
    WHERE зал.id = NEW.idзал;

    while @ряд <= макс_ряд_
        do
            while @место <= макс_место_
                do
                    INSERT INTO билетнаместо (номерместа, номерряда, idсеанс)
                    VALUES (@место, @ряд, NEW.id);
                    set @место = @место + 1;
                end while;
            set @ряд = @ряд + 1;
        end while;
END;
$$
DELIMITER ;
