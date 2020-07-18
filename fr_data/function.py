from pymongo import MongoClient
from math import sin, cos, sqrt, atan2, radians
from datetime import datetime

client = MongoClient('mongodb://NGs:ts6G2rd@ds221416.mlab.com:21416/heroku_pnx01mgk?retryWrites=false')
database = client["heroku_pnx01mgk"]


# อ่านข้อมููลจาก Database นะครับ
def read_data(collection_name):
    market_info = []
    my_collection = database[collection_name]  # เรียก collection
    for all_data in my_collection.find():  # เรียก data ทั้ง db
        latitude = all_data['Latitude']
        longitude = all_data['Longitude']
        name = all_data['Name']
        pack = {
            'Name': name,
            'Latitude': latitude,
            'Longitude': longitude
        }
        market_info.append(pack)
    return market_info


def send_data(collection_name, log):  # collection ที่ต้องการส่ง และข้อมูล
    my_collection = database[collection_name]  # เรียก collection
    my_collection.insert_one(log)  # ส่ง data


# approximate radius of earth in km
def get_distance(lat_user, lon_user, lat_market, lon_market):
    # degrees to radians
    lat_user = radians(lat_user)
    lon_user = radians(lon_user)
    lat_market = radians(lat_market)
    lon_market = radians(lon_market)
    r = 6373.0
    dis_lon = lon_market - lon_user
    dis_lat = lat_market - lat_user
    # calculating distance
    a = sin(dis_lat / 2) ** 2 + cos(lat_user) * cos(lat_market) * sin(dis_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = r * c
    return distance


def sort_listed_data(lat, lon, filters, database):
    print('sort'+str(datetime.now()))
    market_info = database
    data = []
    for i in market_info:
        dist = get_distance(lat, lon, i["Latitude"], i["Longitude"])
        if dist < filters:
            i['Dist'] = float('%.3f' % dist)
            data.append(i)
    if not data:
        return 'no market found'
    sorted_data = sorted(data, key=lambda x: x['Dist'])
    print('sorted'+str(datetime.now()))
    return sorted_data


class Function:
    def __init__(self, user_latitude, user_longitude, user_filter, database):
        self.user_latitude = user_latitude
        self.user_longitude = user_longitude
        self.user_filter = user_filter
        self.database = database

    def think(self):
        return sort_listed_data(self.user_latitude, self.user_longitude, self.user_filter, self.database)


""" 
    def set_user_info(self, user_latitude, user_longitude, user_filter):
        self.user_latitude = user_latitude
        self.user_longitude = user_longitude
        self.user_filter = user_filter
"""
