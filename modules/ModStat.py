import operator
from datetime import date
from pymongo import MongoClient
import utils


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
        if period == 'month':
            self.last_month = date.today().month
            self.month_collection.remove({})
        elif period == 'week':
            self.last_week = date.today().weekday()
            self.week_collection.remove({})
        elif period == 'day':
            self.last_day = date.today().day
            self.day_collection.remove({})

    def execute(self, serv, canal, handle, message):

        stats = dict(day={}, week={}, month={}, all={})

        # Detailed
        stats['day']['mongo'] = self.day_collection.find({})
        stats['week']['mongo'] = self.week_collection.find({})
        stats['month']['mongo'] = self.month_collection.find({})
        stats['all']['mongo'] = self.all_collection.find({})

        for key, value in stats.items():
            stats[key]['detailed'] = []

        for key, value in stats.items():
            for current_handle in value['mongo']:
                stats[key]['detailed'].append(dict(handle=current_handle['handle'],
                                                   messages=int(current_handle['messages'])))
            value.pop('mongo', None)
        # Total
        stats['day']['total'] = self.day_collection.aggregate([{"$group": {"_id": "null", "total": {"$sum": "$messages"}}}])
        stats['day']['total'] = int(stats['day']['total']['result'][0]['total'])
        stats['week']['total'] = self.week_collection.aggregate([{"$group": {"_id": "null", "total": {"$sum": "$messages"}}}])
        stats['week']['total'] = int(stats['week']['total']['result'][0]['total'])
        stats['month']['total'] = self.month_collection.aggregate([{"$group": {"_id": "null", "total": {"$sum": "$messages"}}}])
        stats['month']['total'] = int(stats['month']['total']['result'][0]['total'])
        stats['all']['total'] = self.all_collection.aggregate([{"$group": {"_id": "null", "total": {"$sum": "$messages"}}}])
        stats['all']['total'] = int(stats['all']['total']['result'][0]['total'])

        print str(stats)

        sorted_x = sorted(self.count_message_daily.items(), key=operator.itemgetter(1), reverse=True)
        first_poster = sorted_x[0][0]
        first_poster_messages = sorted_x[0][1]
        message_spell = "messages" if total > 1 else "message"
        serv.privmsg(handle, "Il y a eu \002" + str(total) + " " + message_spell + "\017 aujourd'hui sur \002" + canal)
        message_spell = "messages" if first_poster_messages > 1 else "message"
        serv.privmsg(handle, first_poster + " est le plus bavard avec " + str(
            first_poster_messages) + " " + message_spell + " aujourd'hui !")
        if utils.is_numeric(message):
            message = int(message)
            print "On va afficher les " + str(message) + " dernieres stats"
            if message > self.max_stats:
                serv.privmsg(handle, "(L'historique ne remonte qu'aux " + str(
                    self.max_stats) + " premiers posteurs de la journee)")
                message = self.max_stats
            for num in range(1, min(message, len(sorted_x))):
                rank = num
                rank += 1
                message_spell = "messages" if sorted_x[num][1] > 1 else "message"

                serv.privmsg(handle,
                             str(rank) + ". " + sorted_x[num][0] + ": " + str(sorted_x[num][1]) + " " + message_spell)

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