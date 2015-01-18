from collections import OrderedDict
import json
from pymongo import MongoClient

from flask import Flask, make_response

app = Flask(__name__)

#####################################################
#                 INITIALISATION                    #
#####################################################

# Stats
count_message_daily = {}
count_message_weekly = {}
count_message_monthly = {}
count_message_all = {}


# Mongo
client = MongoClient()
db = client.botncDB
day_collection = db.day
week_collection = db.week
month_collection = db.month
all_collection = db.all


#####################################################
#                   GET METHODS                     #
#####################################################


@app.route('/open-newbiecontest/stats/')
def get_stats():
    stats = OrderedDict()
    stats['day'] = {}
    stats['week'] = {}
    stats['month'] = {}
    stats['all'] = {}

    # Message title
    stats['day']['title'] = "Daily statistics"
    stats['week']['title'] = "Weekly statistics"
    stats['month']['title'] = "Monthly statistics"
    stats['all']['title'] = "All time statistics"

    # Mongo information
    stats['day']['mongo'] = day_collection.find({})
    stats['week']['mongo'] = week_collection.find({})
    stats['month']['mongo'] = month_collection.find({})
    stats['all']['mongo'] = all_collection.find({})

    # Array initialization
    for key, value in stats.items():
        stats[key]['detailed'] = []

    # Detailed information
    for key, value in stats.items():
        for current_handle in value['mongo']:
            stats[key]['detailed'].append(dict(handle=current_handle['handle'],
                                               messages=int(current_handle['messages'])))
        value.pop('mongo', None)
        stats[key]['detailed'] = sorted(stats[key]['detailed'], key=lambda k: k['messages'], reverse=True)

    # Total count
    stats['day']['total'] = day_collection.aggregate([{"$group": {"_id": "null", "total": {"$sum": "$messages"}}}])
    stats['day']['total'] = int(stats['day']['total']['result'][0]['total'])
    stats['week']['total'] = week_collection.aggregate([{"$group": {"_id": "null", "total": {"$sum": "$messages"}}}])
    stats['week']['total'] = int(stats['week']['total']['result'][0]['total'])
    stats['month']['total'] = month_collection.aggregate([{"$group": {"_id": "null", "total": {"$sum": "$messages"}}}])
    stats['month']['total'] = int(stats['month']['total']['result'][0]['total'])
    stats['all']['total'] = all_collection.aggregate([{"$group": {"_id": "null", "total": {"$sum": "$messages"}}}])

    response = make_response(json.dumps(stats))
    response.mimetype = "application/json"
    response.status_code = 200
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5668, debug=True)