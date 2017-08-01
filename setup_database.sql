DROP DATABASE IF EXISTS news;

CREATE DATABASE news;

\c news

\i newsdata.sql

/* create views necessary for main.py queries */

CREATE VIEW art_views AS
SELECT path,
       count(*) AS views
FROM log
WHERE status LIKE '%200%'
  AND path != '/'
GROUP BY path
ORDER BY views DESC;

CREATE VIEW top3 AS
SELECT path,
       count(*),
       title
FROM articles
JOIN log ON log.path LIKE CONCAT('%',articles.slug,'%')
WHERE status LIKE '%200%'
GROUP BY path,
         title
ORDER BY COUNT DESC
LIMIT 3;

CREATE VIEW total_view_date AS
SELECT TO_CHAR(TIME, 'YYYY-MM-DD') AS date,
        count(*) AS total_views
FROM log
WHERE status LIKE '%%'
GROUP BY date
ORDER BY date DESC;

CREATE VIEW succ_view_date AS
SELECT TO_CHAR(TIME, 'YYYY-MM-DD') AS date,
       count(*) AS successes
FROM log
WHERE status LIKE '%200%'
GROUP BY date
ORDER BY date DESC;

CREATE VIEW fail_view_date AS
SELECT TO_CHAR(TIME, 'YYYY-MM-DD') AS date,
       count(*) AS failures
FROM log
WHERE status LIKE '%404%'
GROUP BY date
ORDER BY date DESC;

CREATE VIEW error AS
SELECT total_view_date.date,
       cast(100 * cast(failures AS decimal) / cast(total_views AS decimal) AS decimal(16,2)) AS percent_error
FROM total_view_date
JOIN fail_view_date ON total_view_date.date = fail_view_date.date
ORDER BY date DESC;
