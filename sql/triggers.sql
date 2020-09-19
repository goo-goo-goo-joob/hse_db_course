DROP trigger IF EXISTS chech_покупатель;
DROP trigger IF EXISTS chech_сеанс;
DROP trigger IF EXISTS create_сеанс;

DELIMITER $$
CREATE TRIGGER check_покупатель
    BEFORE INSERT
    ON покупатель
    FOR EACH ROW
BEGIN
    IF (NEW.почта REGEXP '^[A-Za-z0-9._-]+@[A-Za-z0-9.-]+$') = 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Введите существующую электронную почту';
    END IF;
    IF (NEW.телефон REGEXP '^\\+7[0-9]{10}$') = 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Введите существующий номер телефона';
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
    SELECT @типсеанса := типсеанса.id, @надбавкасеанса := типсеанса.надбавкасеанса
    FROM типсеанса
    WHERE типсеанса.времяначала <= TIME(NEW.датавремя)
      and типсеанса.времяконца >= TIME(NEW.датавремя);

    SELECT @надбавказала := типзала.надбавказала
    FROM типзала
    WHERE типзала.id = (
        SELECT зал.idтипзала
        FROM зал
        WHERE зал.id = NEW.idзал);

    SELECT @базоваяцена := кинотеатр.базоваяцена
    FROM кинотеатр
    WHERE кинотеатр.id = (
        SELECT зал.idкинотеатр
        FROM зал
        WHERE зал.id = NEW.idзал);

    SET @цена = @надбавкасеанса + @надбавказала + @базоваяцена;

    UPDATE сеанс
    SET цена        = @цена,
        idтипсеанса = @типсеанса
    WHERE id = NEW.id;

    SET @ряд = 1, @место = 1;

    SELECT @макс_ряд := числорядов
    FROM зал
    WHERE зал.id = NEW.idзал;

    SELECT @макс_место := длинаряда
    FROM зал
    WHERE зал.id = NEW.idзал;

    while @ряд <= @макс_ряд
        do
            while @место <= @макс_место
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