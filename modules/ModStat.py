import irclib
import ircbot
import utils
import operator
from datetime import date



class ModStat:
    count_message_daily = {}
    count_message_weekly = {}
    count_message_monthly = {}
    count_message_all = {}
    last_day = date.today().day
    last_week = date.today().weekday()
    last_month = date.today().month
    max_stats = 5

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
        self.count_message_daily[handle] = 1 if handle not in self.count_message_daily.keys() else self.count_message_daily[handle] + 1
        self.count_message_weekly[handle] = 1 if handle not in self.count_message_weekly.keys() else self.count_message_weekly[handle] + 1
        self.count_message_monthly[handle] = 1 if handle not in self.count_message_monthly.keys() else self.count_message_monthly[handle] + 1
        self.count_message_all[handle] = 1 if handle not in self.count_message_all.keys() else self.count_message_all[handle] + 1

    def reset_count(self, period):
        if period == 'month':
            self.last_month = date.today().month
            self.count_message_monthly = {}
        elif period == 'week':
            self.last_week = date.today().weekday()
            self.count_message_weekly = {}
        elif period == 'day':
            self.last_day = date.today().day
            self.count_message_daily = {}
    
    def execute(self, serv, canal, handle, message):
        total = 0
        for item in self.count_message_daily:
            total += self.count_message_daily[item]
        sorted_x = sorted(self.count_message_daily.items(), key=operator.itemgetter(1), reverse=True)
        first_poster = sorted_x[0][0]
        first_poster_messages = sorted_x[0][1]
        message_spell = "messages" if total > 1 else "message"
        serv.privmsg(handle, "Il y a eu \002" + str(total) + " " + message_spell + "\017 aujourd'hui sur \002" + canal)
        message_spell = "messages" if first_poster_messages > 1 else "message"
        serv.privmsg(handle, first_poster + " est le plus bavard avec " + str(first_poster_messages) + " " + message_spell + " aujourd'hui !")
        if utils.is_numeric(message):
            message = int(message)
            print "On va afficher les " + str(message) + " dernieres stats"
            if message > self.max_stats:
                serv.privmsg(handle, "(L'historique ne remonte qu'aux " + str(self.max_stats) + " premiers posteurs de la journee)")
                message = self.max_stats
            for num in range(1, min(message, len(sorted_x))):
                rank = num
                rank += 1
                message_spell = "messages" if sorted_x[num][1] > 1 else "message"

                serv.privmsg(handle, str(rank) + ". " + sorted_x[num][0] + ": " + str(sorted_x[num][1]) + " " + message_spell)