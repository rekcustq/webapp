from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import create_engine
from json import dumps
import check
import time
import atexit

app = Flask(__name__)
api = Api(app)

db_connect = create_engine('sqlite:///deface.db')

parser = reqparse.RequestParser()
parser.add_argument('scan', type=bool, default=0)
parser.add_argument('https', type=bool, default=1)
parser.add_argument('url', type=str, default="")
parser.add_argument('urlId', type=int, default=0)
parser.add_argument('urlName', type=str, default="")
parser.add_argument('metaStat', type=bool, default=0)
parser.add_argument('strStat', type=bool, default=0)
parser.add_argument('meta', type=str, default="")
parser.add_argument('company', type=str, default="")

def webStat(web):
    data = {}
    url = ('https://' if web[6] else 'http://') + web[1]
    data[url] = []
    mts = 'Changed' if web[2] == 'True' else 'Normal' # metaStat
    sts = 'Illegal' if web[3] == 'True' else 'Normal' # strStat
    comp = web[5]
    data[url].append({ 
        'Meta': mts,
        'Strings': sts,
    })
    data[url].append('Company: ' + comp)

    return data

def listComp(company):
    conn = db_connect.connect()
    lists = conn.execute('SELECT * FROM urls WHERE company = "' + company + '"').cursor.fetchall()
    if not lists:
        return 'No such company in Database'

    data = {}
    for web in lists:
        data.update(webStat(web))

    conn.close()
    return data

def listAll():
    conn = db_connect.connect()
    webs = conn.execute('SELECT * FROM urls').cursor.fetchall()
    if not webs:
        return 'Database is empty'

    data = {}
    for web in webs:
        data.update(webStat(web))

    conn.close()
    return data

class webList(Resource):
    def get(self):
        args = parser.parse_args()
        scan = args['scan']
        https = args['https']
        company = args['company']
        url = args['url']

        if not scan:
            if not company:
                return listAll()

            if not url:
                return listComp(company)

            conn = db_connect.connect()
            web = conn.execute('SELECT * FROM urls WHERE urlName = "' + url + '"').cursor.fetchall()
            if not web:
                return 'Not found in Database'

            data = webStat(web[0])
            data[url][0].update({'Meta Info': web[0][4]})

            conn.close()
            return data
        else:
            if not company:
                check.sched()
                return listAll()

            if not url:
                check.sched(company)
                return listComp(company)

            url = [company, https, url]
            return check.detect(url)

    def post(self):
        args = parser.parse_args()
        https = args['https']
        url = args['url']
        company = args['company']

        conn = db_connect.connect()
        conn.execute('''INSERT INTO urls("urlName", "company", "https")
                        VALUES ("''' + url + '", "' + company + '", "' + str(https) + '")')
        conn.close()
        return 'Created', 201

    def put(self):
        args = parser.parse_args()
        https = args['https']
        url = args['url']
        urlId = args['urlId']
        urlName = args['urlName']
        metaStat = args['metaStat']
        strStat = args['strStat']
        meta = args['meta']
        company = args['company']

        conn = db_connect.connect()
        conn.execute('''UPDATE urls
                        SET urlId = "''' + str(urlId) + '''", 
                            urlName = "''' + urlName + '''",
                            metaStat = "''' + str(metaStat) + '''",
                            strStat = "''' + str(strStat) + '''",
                            meta = "''' + meta + '''",
                            company = "''' + company + '''",
                            https = "''' + str(https) + '''"
                        WHERE urlName = "''' + url + '";')
        conn.close()
        return 'Modified', 200

    def delete(self):
        args = parser.parse_args()
        url = args['url']

        conn = db_connect.connect()
        conn.execute('DELETE FROM urls WHERE urlName = "' + url + '";')
        conn.close()
        return 'Deleted', 204

scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(func=check.sched, trigger="interval", minutes=15)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())

api.add_resource(webList, '/')

if __name__ == '__main__':
    app.run(debug=True)