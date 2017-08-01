# SUMMARY
This logs analysis project is an exercise in building PostgreSQL queries on a database with over a million records.
The newsdata database is a mock database describing page views for a fictional news website.  It has 
three tables: author, articles, and log.  The purpose of this project is to demonstrate the authors ability
to efficiently query SQL records via Python script and present the output in a clean, reader friendly manner.

Demonstrated are 3 sample sets of data:

- What are the most popular three articles of all time?
- Who are the most popular article authors of all time?
- On which days did more than 1% of page requests lead to errors?

# REQUIREMENTS
- [Python v3.5.2](https://www.python.org/downloads/release/python-352/)
- [psycopg2 v2.7.3](http://initd.org/psycopg/)
- [PostgreSQL v9.5.7](https://www.postgresql.org/download/)

# INSTRUCTIONS
- Download and setup the news database
    - Download and extract the 
[newsdata.sql database](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
    - CD to directory with the SQL file and create the news database
     with command "psql -d news -f newsdata.sql"
    - Once db is created, connect with "psql -d news", and view schema using "\dt" and "\d [table name]"
- Create necessary views
    - Run all sql view statements in the order found in "VIEWS" section of this readme.
    
- Execute Python script to retrieve data
    - Place the main.py script in the same directory as the newsdata.sql database.
    - From console, while in directory, use command "python main.py" to display results of queries


# VIEWS
## art_views
All articles, total views.

```sql
CREATE VIEW art_views AS
SELECT path,
       count(*) AS views
FROM log
WHERE status LIKE '%200%'
  AND path != '/'
GROUP BY path
ORDER BY views DESC;
```

## top3
Top 3 viewed articles.

```sql
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
```
    
## total_view_date
Total page view requests by date.

```sql
CREATE VIEW total_view_date AS
SELECT TO_CHAR(TIME, 'YYYY-MM-DD') AS date,
        count(*) AS total_views
FROM log
WHERE status LIKE '%%'
GROUP BY date
ORDER BY date DESC;
```

## succ_view_date
Total successful page views by date.

```sql
CREATE VIEW succ_view_date AS
SELECT TO_CHAR(TIME, 'YYYY-MM-DD') AS date,
       count(*) AS successes
FROM log
WHERE status LIKE '%200%'
GROUP BY date
ORDER BY date DESC;
```

## fail_view_date
Total failed pages requests by date.

```sql
CREATE VIEW fail_view_date AS
SELECT TO_CHAR(TIME, 'YYYY-MM-DD') AS date,
       count(*) AS failures
FROM log
WHERE status LIKE '%404%'
GROUP BY date
ORDER BY date DESC;
```

## error
Error rate by date.

```sql
CREATE VIEW error AS
SELECT total_view_date.date,
       cast(100 * cast(failures AS decimal) / cast(total_views AS decimal) AS decimal(16,2)) AS percent_error
FROM total_view_date
JOIN fail_view_date ON total_view_date.date = fail_view_date.date
ORDER BY date DESC;
```
    
# RESOURCES
- SQL DB provided by Udacity
- Table output code adapted from 
[StackOverflow](https://stackoverflow.com/questions/10865483/print-results-in-mysql-format-with-python)

