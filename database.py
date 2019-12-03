import sqlite3

url_list = [('stackoverflow.com', 'False', 'False', ''),
            ('instagram.com', 'False', 'False', ''),
            ('python.org', 'False', 'False', ''),
            ('youtube.com', 'False', 'False', '')]

conn = sqlite3.connect('deface.db')

c = conn.cursor()

# c.execute('''CREATE TABLE urls (
#               urlId integer PRIMARY KEY,
#               urlName varchar(255) NOT NULL UNIQUE,
#               metaStat bool,
#               strStat bool,
#               meta varchar(255) DEFAULT "",
#               company varchar(255)
#           )''')

# c.executemany('INSERT INTO urls(urlName, metaStat, strStat, meta) VALUES (?,?,?,?)', url_list)
# for i in range(8, 10):
#     c.execute("DELETE FROM urls WHERE urlId==" + str(i))
# c.execute('UPDATE urls SET company = "" WHERE urlName = "youtube.com"')
# c.execute('UPDATE urls SET meta = "" WHERE urlName = "Google.com"')
url = 'gmail.com'
urlId = 9
urlName = 'gmail.com'
metaStat = True
strStat = False
meta = 'asdf'
company = 'google'
https = True
# conn.execute('''UPDATE urls
#                 SET urlId = "''' + str(urlId) + '''", 
#                     urlName = "''' + str(urlName) + '''",
#                     metaStat = "''' + str(metaStat) + '''",
#                     strStat = "''' + str(strStat) + '''",
#                     meta = "''' + str(meta) + '''"
#                 WHERE urlName = "''' + url + '";')
# c.execute('''INSERT INTO urls (urlName, company) 
#              SELECT "''' + url + '", "' + company + '''"
#              WHERE NOT EXISTS 
#              (SELECT * FROM urls WHERE urlName = "''' + url + '")')
# c.execute('''UPDATE urls 
#              SET meta = "''' + meta + '''" 
#              WHERE urlName = "''' + url + '"')
# c.execute('ALTER TABLE urls ADD company varchar(255);')

for row in c.execute('SELECT * FROM urls ORDER BY urlId'):
    print(row, '\n')

# print(c.execute('SELECT * FROM urls WHERE company = "google"').fetchall()[0])
# c.execute("DROP TABLE urls")

conn.commit()
conn.close()

# stackoverflow.com
# instagram.com
# python.org
# youtube.com
# google.com
# github.com
# dev.to