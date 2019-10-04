from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
import check
import schedule

app = Flask(__name__)
api = Api(app)

db_connect = create_engine('sqlite:///deface.db')
conn = db_connect.connect()

class checkWeb(Resource):
    def get(self, url):
        data = check.detect(url)
        return data

api.add_resource(checkWeb, '/check/<url>')

if __name__ == '__main__':
    schedule.every(5).minutes.do(check.sched())
    app.run(debug=True)