#!/usr/bin/env python
# Austin Weng
# Udacity FSND Log Analysis Project

import psycopg2

DBNAME = "news"

# Extract data from database


def retrieve_data(query):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(query)
    data = c.fetchall()
    db.close()
    return data


print('Log Analysis Project')
print('\n')

# Question One

qla_1 = "What are the three most popular articles of all time?"
query_one = ("SELECT title, COUNT(*) as num FROM articles "
             "  JOIN log ON log.path = CONCAT('/article/',articles.slug)"
             "  GROUP BY title ORDER BY num DESC LIMIT 3; ")

answer_one = retrieve_data(query_one)

print(qla_1)
for i in range(len(answer_one)):
    print(str(i+1) + "\t" + str(answer_one[i][0])
          + ": " + str(answer_one[i][1]) + " views")

print('\n')

# Question Two

qla_2 = "Who are the most popular article authors of all time?"
query_two = ("SELECT authors.name, count(*) as num"
             " FROM articles JOIN authors ON articles.author = authors.id "
             " JOIN log ON log.path = CONCAT('/article/',articles.slug)"
             " GROUP BY authors.name ORDER BY num DESC;")

answer_two = retrieve_data(query_two)

print(qla_2)

for i in range(len(answer_two)):
    print(str(i+1) + "\t" + str(answer_two[i][0])
          + ": " + str(answer_two[i][1]) + " views")

print('\n')

# Question Three


qla_3 = "On which days did more than one percent of requests lead to errors?"
query_three = (" SELECT * FROM"
               " (SELECT date(time),"
               " CAST(100.00*SUM(CASE log.status"
               " WHEN '404 NOT FOUND' THEN 1 ELSE 0 END)"
               " /COUNT(log.status)"
               " AS DECIMAL(10,3))"
               " AS errorrate FROM log"
               " GROUP BY date(time) ORDER BY errorrate DESC)"
               " AS subquery WHERE errorrate > 1;")


answer_three = retrieve_data(query_three)
print(qla_3)
for i in range(len(answer_three)):
    print("On " + str(answer_three[i][0]) + ", there was a "
          + str(answer_three[i][1]) + "%" + " request error.")
