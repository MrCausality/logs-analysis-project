#!/usr/bin/env python3

import psycopg2


def printtable(cursor):
    """Formats output of SQL queries into user-friendly table."""
    results = cursor.fetchall()
    widths = []
    columns = []
    tavnit = "|"
    separator = "+"

    lengths = []
    for prop in results[0]:
        lengths.append(0)

    for i in results:
        k = 0
        for j in i:
            if len(str(j)) > lengths[k]:
                lengths[k] = len(str(j))
            k += 1

    i = 0
    for cd in cursor.description:
        widths.append(max(lengths[i], len(cd[0])))
        columns.append(cd[0])
        i += 1

    for w in widths:
        tavnit += " %-"+"%ss |" % (w,)
        separator += "-"*w + "--+"

    r = ""
    r += separator + "\n"
    r += (tavnit % tuple(columns)) + "\n"
    r += separator + "\n"
    for row in results:
        r += (tavnit % row) + "\n"
    r += separator + "\n"
    r += ""
    return r


def execute_query(query):
    """execute_query takes an SQL query as a parameter.
       Executes the query and returns the results as a list of tuples.
      args:
          query - an SQL query statement to be executed.

      returns:
          A list of tuples containing the results of the query.
   """
    try:
        db = psycopg2.connect("dbname=news")
        c = db.cursor()
        c.execute(query)
        results = printtable(c)
        db.close
        return results
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_top3():
    """Return top 3 articles by successful views."""
    query = """SELECT ROW_NUMBER() OVER () AS rank, title, count AS views
            FROM top3;"""
    print("Top Viewed Articles\n" + execute_query(query))


def get_top_authors():
    """Return authors ranked by total successful views."""
    query = """SELECT authors.name, SUM(views) AS total_views FROM art_views
            JOIN articles ON path LIKE CONCAT('%',slug,'%')
            JOIN authors ON articles.author = authors.id
            GROUP BY authors.name ORDER BY total_views DESC;"""
    print("Top Authors by Total Views\n" + execute_query(query))


def get_error_rate():
    """Return days where page request error rate exceeded one percent."""
    query = "SELECT * FROM error WHERE percent_error > 1;"
    print("Days With > 1% Page Request Error Rate\n" + execute_query(query))


if __name__ == '__main__':
    get_top3()
    get_top_authors()
    get_error_rate()
