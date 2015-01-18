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
            self.reset_count('day')
        if date.today().weekday() == 0:
            self.reset_count('week')
        if date.today().month != self.last_month:
            self.reset_count('month')
        self.add_count(handle)

    def add_count(self, handle):
        day_user = {}
        week_user = {}
        month_user = {}
        all_user = {}

        # Day
        if self.find_handle(handle, self.day_collection) is not None:
            day_user = self.find_handle(handle, self.day_collection)
            day_user['messages'] += 1
            ref = {'_id': day_user['_id']}
            self.day_collection.update(ref, day_user)
        else:
            day_user['handle'] = handle
            day_user['messages'] = 1
            self.day_collection.insert(day_user)

        # Week
        if self.find_handle(handle, self.week_collection) is not None:
            week_user = self.find_handle(handle, self.week_collection)
            week_user['messages'] += 1
            ref = {'_id': week_user['_id']}
            self.week_collection.update(ref, week_user)
        else:
            week_user['handle'] = handle
            week_user['messages'] = 1
            self.week_collection.insert(week_user)

        # Month
        if self.find_handle(handle, self.month_collection) is not None:
            month_user = self.find_handle(handle, self.month_collection)
            month_user['messages'] += 1
            ref = {'_id': month_user['_id']}
            self.month_collection.update(ref, month_user)
        else:
            month_user['handle'] = handle
            month_user['messages'] = 1
            self.month_collection.insert(month_user)

        # All
        if self.find_handle(handle, self.all_collection) is not None:
            all_user = self.find_handle(handle, self.all_collection)
            all_user['messages'] += 1
            ref = {'_id': all_user['_id']}
            self.all_collection.update(ref, all_user)
        else:
            all_user['handle'] = handle
            all_user['messages'] = 1
            self.all_collection.insert(all_user)

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
        stats['day']['detailed'] = self.day_collection.find({})
        stats['week']['detailed'] = self.day_collection.find({})
        stats['month']['detailed'] = self.day_collection.find({})
        stats['all']['detailed'] = self.day_collection.find({})

        print str(stats['day']['detailed'])
        exit

        # Total
        stats['day']['total'] = self.day_collection.aggregate([{"$group": {"_id": "null", "total": {"$sum": "$messages"}}}])
        stats['day']['total'] = int(stats['day']['total']['result'][0]['total'])
        stats['week']['total'] = self.week_collection.aggregate([{"$group": {"_id": "null", "total": {"$sum": "$messages"}}}])
        stats['week']['total'] = int(stats['week']['total']['result'][0]['total'])
        stats['month']['total'] = self.month_collection.aggregate([{"$group": {"_id": "null", "total": {"$sum": "$messages"}}}])
        stats['month']['total'] = int(stats['month']['total']['result'][0]['total'])
        stats['all']['total'] = self.all_collection.aggregate([{"$group": {"_id": "null", "total": {"$sum": "$messages"}}}])
        stats['all']['total'] = int(stats['all']['total']['result'][0]['total'])

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
        collection = collection.find({'handle': handle})
        for user in collection:
            user['_id'] = str(user['_id'])
            handles.append(user)
        if len(handles) == 0:
            return None
        return handles[0]