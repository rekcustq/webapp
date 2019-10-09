import sqlite3

url_list = [('stackoverflow.com', 'False', 'False', ''),
            ('instagram.com', 'False', 'False', ''),
            ('python.org', 'False', 'False', ''),
            ('youtube.com', 'False', 'False', '')]

conn = sqlite3.connect('deface.db')

c = conn.cursor()

# c.execute('''CREATE TABLE urls (
#               urlId integer PRIMARY KEY,
#               urlName varchar(255) NOT NULL,
#               metaStat bool,
#               strStat bool,
#               meta varchar(255) DEFAULT ""
#           )''')

# c.executemany('INSERT INTO urls(urlName, metaStat, strStat, meta) VALUES (?,?,?,?)', url_list)
# for i in range(5, 6):
#     c.execute("DELETE FROM urls WHERE urlId==" + str(i))
c.execute('UPDATE urls SET metaStat = "True" WHERE urlName = "stackoverflow.com"')
url = 'stackoverflow.com'
urlId = 9
urlName = 'stackover.com'
metaStat = True
strStat = False
meta = ''
# conn.execute('''UPDATE urls
#                 SET urlId = "''' + str(urlId) + '''", 
#                     urlName = "''' + str(urlName) + '''",
#                     metaStat = "''' + str(metaStat) + '''",
#                     strStat = "''' + str(strStat) + '''",
#                     meta = "''' + str(meta) + '''"
#                 WHERE urlName = "''' + url + '";')

for row in c.execute('SELECT * FROM urls ORDER BY urlId'):
    print(row)

# web = c.execute('SELECT * FROM urls WHERE urlName = "stackoverflow.com"').fetchall()[0]
# c.execute("DROP TABLE urls")

conn.commit()
conn.close()