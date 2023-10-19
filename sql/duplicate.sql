SELECT ROWID, PRESSMARK, COUNT(*) AS count FROM tblRawStatistics GROUP BY PRESSMARK HAVING count > 1;

-- SELECT * FROM tblRawStatistics AS main
-- WHERE EXISTS (
--   SELECT 1 FROM tblRawStatistics AS s
--   WHERE main.PRESSMARK = s.PRESSMARK
--   AND main.rowid <> s.rowid
-- )
-- ORDER BY main.PRESSMARK;

-- SELECT ROWID, PRESSMARK, SUM(POSITION) AS counted FROM tblRawStatistics GROUP BY PRESSMARK;

CREATE TABLE tblRawStatisticsND ("PRESSMARK" TEXT,  "POSITION" TEXT,  "PERIOD" INTEGER, UNIQUE ("PRESSMARK"))

INSERT INTO tblRawStatisticsND SELECT m.PRESSMARK, SUM(m.POSITION) AS "POSITION", "PERIOD" FROM tblRawStatistics AS m GROUP BY m.PRESSMARK;

ALTER TABLE tblRawStatistics RENAME TO old_tblRawStatistics;
ALTER TABLE tblRawStatisticsND RENAME TO tblRawStatistics;

DROP TABLE old_tblRawStatistics;
