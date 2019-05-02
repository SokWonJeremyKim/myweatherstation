#!flask/bin/python
# -*- coding: utf-8 -*-

import json
import time

from flask import Flask, request
from sqlalchemy import create_engine

import model
from model import Location, Session

app = Flask(__name__)
app.config.from_pyfile("config.py")

app.db_engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"], pool_recycle = 3600, echo = False, encoding="utf-8")
model.Base.metadata.bind = app.db_engine
model.Session.configure(bind = app.db_engine)

@app.route('/')
def index():
    return "hello world! =)"

@app.route('/rainingHere/', methods = ['POST'])
def reportRain():
    json_content = request.get_json()
    print json_content

    sido = json_content.get("sido")
    sigungu = json_content.get("sigungu")

    Session.add(Location(sido, sigungu))
    Session.commit()
    return 'SUCCESSFULLY RETURNED'

@app.route('/rainingLocations/', methods = ['GET'])
def getrainingLocations():
    rainingLocationsPastHour = Session.query(Location).filter(Location.reportedTime > (time.time() - 7200)).all()
    if rainingLocationsPastHour is None:
        print 'no raining locations' 
        return 'NONE'
    json_objects = []
    for result in rainingLocationsPastHour:
        json_objects.append('{"sido":"' + result.sido + '","sigungu":"' + result.sigungu + '","reportedTime":"' + str(int(result.reportedTime)) + '"}')  
    json_result = ','.join(json_objects)
    json_result = '{"locations":[' + json_result + ']}'
    return json_result

@app.teardown_appcontext
def close_session(exception = None):
    Session.remove()

if __name__ == '__main__':
    model.Base.metadata.create_all()
    # app.run(host='0.0.0.0', port=80)
    app.run(debug=True)
