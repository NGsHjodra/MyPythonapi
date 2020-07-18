from flask import jsonify, request, Flask
from function import read_data, send_data, Function
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
Database = read_data('dummy')


@app.route('/', methods=['GET', 'POST'])
def home():
    return "<h1> Distance_API_Version 1.0.0 </h1>"


# approximate radius of earth in km
@app.route('/api/call_distance/', methods=['GET', 'POST'])
def send_call_distance():
    print("begin" + str(datetime.now()))
    log_db = 'Log_API_FIND_DISTANCE'
    lat = request.args.get('latitude', type=float)  # lat
    lon = request.args.get('longitude', type=float)  ## long
    filters = request.args.get('range', default=1.5, type=float)  ### filter

    if type(lat) != float or type(lon) != float:
        log = {
            "timestamp": str(datetime.now()),
            "log": "error please check you reqeust message"
        }

        send_data(log_db, log)
        return jsonify({'message': 'error please check you reqeust message'}), 421

    else:
        input_1 = Function(lat, lon, filters, Database)
        data = input_1.think()

        res = {"res": data,
               "timestamp": str(datetime.now())
               }

    #    log = {
     #       "timestamp": str(datetime.now()),
    #        "log": data
    #    }
    #    print('before_send_log'+str(datetime.now()))
    #    send_data(log_db, log)
        print('after_send_log' + str(datetime.now()))
        return jsonify(res)


@app.route('/api/market-list/', methods=['GET', 'POST'])
def list_1():
    return jsonify({"message": Database}), 200


if __name__ == '__main__':
    app.run()



#fr-------------------------------------------------------------------------------------------------------
from flask import jsonify, request, Flask
from function import read_data, send_data, Function
from datetime import datetime
import redis
import json
import os

app = Flask(__name__)
app.config['DEBUG'] = True
R_data = redis.Redis(host="ec2-52-1-83-234.compute-1.amazonaws.com", port=11809, username='h',
                     password="p09cc1910db74f853b8d2473ce60b5ee5dbda668f087a0d4b6979f9369258bfb6")
#R_data = redis.from_url(os.environ.get("redis://h:p09cc1910db74f853b8d2473ce60b5ee5dbda668f087a0d4b6979f9369258bfb6@ec2-52-1-83-234.compute-1.amazonaws.com:11809"))


# db = read_data('dummy')host='localhost',port=6379, db=3


@app.route('/', methods=['GET', 'POST'])
def home():

    R_data.set("My_data", json.dumps(read_data('dummy')))  # set data to redis use this code in
    print('Assigning')

    return "<h1> Distance_API_Version 1.0.0 </h1>"


# approximate radius of earth in km
@app.route('/api/call_distance/', methods=['GET', 'POST'])
def send_call_distance():
    Database = json.loads(R_data.get("My_data"))
    print('Begin')
    log_db = 'Log_API_FIND_DISTANCE'
    lat = request.args.get('latitude', type=float)  # lat
    lon = request.args.get('longitude', type=float)  # long
    filters = request.args.get('range', default=1.5, type=float)  # filter

    if type(lat) != float or type(lon) != float:
        log = {
            "timestamp": str(datetime.now()),
            "log": "error please check you reqeust message"
        }

        send_data(log_db, log)
        return jsonify({'message': 'error please check you reqeust message'}), 421

    else:
        input_1 = Function(lat, lon, filters, Database)
        data = input_1.think()

        res = {"res": data,
               "timestamp": str(datetime.now())
               }

        log = {
            "timestamp": str(datetime.now()),
            "log": data
        }
        print('before_send_log' + str(datetime.now()))
        send_data(log_db, log)
        print('after_send_log' + str(datetime.now()))
        return jsonify(res)


@app.route('/api/market-list/', methods=['GET', 'POST'])
def list_1():

    Database = read_data('dummy')
    input = json.dumps(Database)
  #  Database = json.loads(input)
  #  return Database
    return jsonify({"message": input}), 200


if __name__ == '__main__':
    app.run()
