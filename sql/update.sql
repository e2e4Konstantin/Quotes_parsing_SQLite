UPDATE tblQuotes
SET statistics = CASE WHEN number_of_pages > 0 THEN (number_of_pages - 1) ELSE 0 END
WHERE whatever_condition

update books
set number_of_pages = number_of_pages - 1
where number_of_pages > 0 AND book_id = 10

update books
set number_of_pages = 0
where number_of_pages <= 0 AND book_id = 10


UPDATE tblQuotes SET statistics = 55 WHERE code = '6.5' AND period = 68


