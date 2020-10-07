DROP PROCEDURE IF EXISTS procedure_сеанс;
DROP trigger IF EXISTS check_сеанс1;
DROP trigger IF EXISTS check_сеанс2;

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
      AND ((датавремя_ >= сеанс.датавремя AND
            датавремя_ <= сеанс.датавремя + ф.длительность) OR
           (датавремя_ + длительность_ >= сеанс.датавремя AND
            датавремя_ + длительность_ <= сеанс.датавремя + ф.длительность));

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