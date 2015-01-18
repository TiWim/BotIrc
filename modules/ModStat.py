import operator
from datetime import date
from pymongo import MongoClient
import utils
from collections import OrderedDict


class ModStat:
    # Stats

    count_message_daily = {}
    count_message_weekly = {}
    count_message_monthly = {}
    count_message_all = {}
    last_day = date.today().day
    last_week = date.today().weekday()
    last_month = date.today().month
    max_stats = 5
    week_reset = False

    # Mongo

    client = MongoClient()
    db = client.botncDB
    day_collection = db.day
    week_collection = db.week
    month_collection = db.month
    all_collection = db.all

    def __init__(self):
        pass

    def update_counts(self, handle):
        if date.today().day != self.last_day:
            print "#Day: " + str(date.today().day) + " vs " + str(self.last_day)
            self.reset_count('day')
        if date.today().weekday() == 1 and self.week_reset is False:
            print "#Week: " + str(date.today().weekday()) + " vs 0"
            self.week_reset = True
            self.reset_count('week')
        if date.today().weekday() != 1 and self.week_reset is True:
            self.week_reset = False
        if date.today().month != self.last_month:
            print "#Month: " + str(date.today().month) + " vs " + str(self.last_month)
            self.reset_count('month')
        self.add_count(handle)

    def add_count(self, handle):
        self.day_collection.update({'handle': handle}, {'$inc': {'messages': 1}}, upsert=True)
        self.week_collection.update({'handle': handle}, {'$inc': {'messages': 1}}, upsert=True)
        self.month_collection.update({'handle': handle}, {'$inc': {'messages': 1}}, upsert=True)
        self.all_collection.update({'handle': handle}, {'$inc': {'messages': 1}}, upsert=True)

    def reset_count(self, period):
        if period == 'day':
            self.last_day = date.today().day
            self.day_collection.remove({})
        elif period == 'week':
            self.last_week = date.today().weekday()
            self.week_collection.remove({})
        elif period == 'month':
            self.last_month = date.today().month
            self.month_collection.remove({})

    def execute(self, serv, canal, handle, message):
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
        stats['day']['mongo'] = self.day_collection.find({})
        stats['week']['mongo'] = self.week_collection.find({})
        stats['month']['mongo'] = self.month_collection.find({})
        stats['all']['mongo'] = self.all_collection.find({})

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
        stats['day']['total'] = self.day_collection.aggregate([{"$group": {"_id": "null", "total": {"$sum": "$messages"}}}])
        stats['day']['total'] = int(stats['day']['total']['result'][0]['total'])
        stats['week']['total'] = self.week_collection.aggregate([{"$group": {"_id": "null", "total": {"$sum": "$messages"}}}])
        stats['week']['total'] = int(stats['week']['total']['result'][0]['total'])
        stats['month']['total'] = self.month_collection.aggregate([{"$group": {"_id": "null", "total": {"$sum": "$messages"}}}])
        stats['month']['total'] = int(stats['month']['total']['result'][0]['total'])
        stats['all']['total'] = self.all_collection.aggregate([{"$group": {"_id": "null", "total": {"$sum": "$messages"}}}])
        stats['all']['total'] = int(stats['all']['total']['result'][0]['total'])

        serv.privmsg(handle, "\00303\002Messages count statistics")
        for key, value in stats.items():
            message_spell = "messages" if value['total'] > 1 else "message"
            serv.privmsg(handle, "\00302\002" + value['title'])
            serv.privmsg(handle, "\002Total :\017 " + str(value['total']) + " " + message_spell)
            if utils.is_numeric(message):
                for num in range(0, min(int(message), len(value['detailed']))):
                    message_spell = "messages" if value['detailed'][num]['messages'] > 1 else "message"
                    serv.privmsg(handle, "\002" + str(num + 1) + ". "
                                 + value['detailed'][num]['handle']
                                 + ": \017" + str(value['detailed'][num]['messages']) + " " + message_spell)
            serv.privmsg(handle, "****************")

    @staticmethod
    def find_handle(handle, collection):
        handles = []
        users = collection.find({'handle': handle})
        for user in users:
            user['_id'] = str(user['_id'])
            handles.append(user)
        if len(handles) == 0:
            return None
        return handles[0]