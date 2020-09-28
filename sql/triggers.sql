DROP trigger IF EXISTS check_покупатель;
DROP trigger IF EXISTS check_сеанс;
DROP trigger IF EXISTS create_сеанс;

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
    IF (NEW.телефон REGEXP '^([+][7][0-9]{10})') = 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Введите существующий номер телефона соответствии с форматом +7xxxxxxxxxx.';
    END IF;
END;
$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER check_сеанс
    BEFORE INSERT
    ON сеанс
    FOR EACH ROW
BEGIN
    IF (NEW.датавремя < NOW()) = 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Дата и время сеанса меньше текщего времени.';
    END IF;
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

INSERT INTO cinemadb.покупатель (фио, телефон, почта)
VALUES ('Самоделкина Мария Владимировна', '+78005553535', 'mvsamodelkina_4@edu.hse.ru')