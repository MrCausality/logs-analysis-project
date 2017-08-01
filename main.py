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

    print(separator)
    print(tavnit % tuple(columns))
    print(separator)
    for row in results:
        print(tavnit % row)
    print(separator)
    print("")


def get_top3():
    """Return top 3 articles by successful views."""
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute("SELECT ROW_NUMBER() OVER () AS rank, title, count AS views "
              "FROM top3;")
    print("Top Viewed Articles:")
    printtable(c)
    db.close


def get_top_authors():
    """Return authors ranked by total successful views."""
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute("SELECT authors.name, SUM(views) AS total_views FROM art_views "
              "JOIN articles ON path LIKE CONCAT('%',slug,'%') "
              "JOIN authors ON articles.author = authors.id "
              "GROUP BY authors.name ORDER BY total_views DESC;")
    print("Top Authors by Total Views:")
    printtable(c)
    db.close


def get_error_rate():
    """Return days where page request error rate exceeded one percent."""
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute("SELECT * FROM error WHERE percent_error > 1;")
    print("Days with greater than 1% Page Request Error Rate:")
    printtable(c)
    db.close


get_top3()
get_top_authors()
get_error_rate()
