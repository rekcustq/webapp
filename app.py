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
parser.add_argument('urlId', type=int, required=True)
parser.add_argument('urlName', type=str)
parser.add_argument('metaStat', type=bool)
parser.add_argument('strStat', type=bool)
parser.add_argument('meta', type=str)

class checkWeb(Resource):
    def get(self, url):
        return check.detect(url)

    def delete(self, url):
        conn = db_connect.connect()
        conn.execute('DELETE FROM urls WHERE urlName = "' + url + '";')
        conn.close()
        return 'del', 204

    def put(self, url):
        args = parser.parse_args()
        urlId = args['urlId']
        urlName = args['urlName']
        metaStat = args['metaStat']
        strStat = args['strStat']
        meta = args['meta']

        conn = db_connect.connect()
        conn.execute('''UPDATE urls 
                        SET urlId = "''' + str(urlId) + '''", 
                            urlName = "''' + str(urlName) + '''",
                            metaStat = "''' + str(metaStat) + '''",
                            strStat = "''' + str(strStat) + '''",
                            meta = "''' + str(meta) + '''"
                        WHERE urlName = "''' + url + '";')
        conn.close()
        return 'Url changed', 200

class checkAll(Resource):
    def get(self):
        print(url)
        return check.sched()

def webStat(web):
    data = {}
    url = web[1]
    data[url] = []
    mts = 'Changed' if web[2] == 'True' else 'Normal' # metaStat
    sts = 'Illegal' if web[3] == 'True' else 'Normal' # strStat
    data[url].append({ 
        'Meta': mts,
        'Strings': sts 
    })

    return data

class webList(Resource):
    def get(self):
        conn = db_connect.connect()
        webs = conn.execute('SELECT * FROM urls').cursor.fetchall()

        data = {}
        for web in webs:
            data.update(webStat(web))

        conn.close()
        return data

class webInfo(Resource):
    def get(self, url):
        conn = db_connect.connect()
        web = conn.execute('SELECT * FROM urls WHERE urlName = "' + url + '"').cursor.fetchall()

        data = webStat(web[0])
        data[url][0].update({'Meta Info': web[0][4]})

        conn.close()
        return data

scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(func=check.sched, trigger="interval", minutes=15)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())

api.add_resource(webList, '/web')
api.add_resource(webInfo, '/web/<url>')
api.add_resource(checkAll, '/check')
api.add_resource(checkWeb, '/check/<url>')

if __name__ == '__main__':
    app.run(debug=True)