# SUMMARY
This logs analysis project is an exercise in building PostgreSQL queries on a database with over a million records.
It searches for 3 particular sets of data (seen below) and returns in nicely formatted, email-friendly tables.

<ul>
    <li>What are the most popular three articles of all time?</li>
    <li>Who are the most popular article authors of all time?</li>
    <li>On which days did more than 1% of page requests lead to errors?</li>
</ul>

# REQUIREMENTS
<ul>
    <li>Python 3</li>
    <li><a href="http://initd.org/psycopg/">psycopg2</a></li>
</ul>

# INSTRUCTIONS
Place the main.py script in the same directory as the newsdata.sql database.  Create all views listed below, as they are
necessary for the python script.  Execute python script from console to view output of program.


# VIEWS
## art_views
All articles, total views.

    CREATE VIEW art_views AS
    SELECT path,
           count(*) AS views
    FROM log
    WHERE status LIKE '%200%'
      AND path != '/'
    GROUP BY path
    ORDER BY views DESC;

## top3
Top 3 viewed articles.

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
    
## total_view_date
Total page view requests by date.

    CREATE VIEW total_view_date AS
    SELECT TO_CHAR(TIME, 'YYYY-MM-DD') AS date,
            count(*) AS total_views
    FROM log
    WHERE status LIKE '%%'
    GROUP BY date
    ORDER BY date DESC;

## succ_view_date
Total successful page views by date.

    CREATE VIEW succ_view_date AS
    SELECT TO_CHAR(TIME, 'YYYY-MM-DD') AS date,
           count(*) AS successes
    FROM log
    WHERE status LIKE '%200%'
    GROUP BY date
    ORDER BY date DESC;

## fail_view_date
Total failed pages requests by date.

    CREATE VIEW fail_view_date AS
    SELECT TO_CHAR(TIME, 'YYYY-MM-DD') AS date,
           count(*) AS failures
    FROM log
    WHERE status LIKE '%404%'
    GROUP BY date
    ORDER BY date DESC;

## error
Error rate by date.

    CREATE VIEW error AS
    SELECT total_view_date.date,
           cast(100 * cast(failures AS decimal) / cast(total_views AS decimal) AS decimal(16,2)) AS percent_error
    FROM total_view_date
    JOIN fail_view_date ON total_view_date.date = fail_view_date.date
    ORDER BY date DESC;
    
# RESOURCES
<ul>
    <li>SQL DB provided by Udacity
    <li>Table output code adapted from 
        <a href="https://stackoverflow.com/questions/10865483/print-results-in-mysql-format-with-python">
            StackOverflow
        </a>
    </li>
</ul>
