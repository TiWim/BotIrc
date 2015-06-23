from pymongo import MongoClient
import utils

class ModVote:
    client = MongoClient()
    db = client.ModVote
    poll_collection = db.polls

    count = 0
    countY = 0
    countN = 0
    current_poll = ""
    poll_id = 0
    nicks = []
    poll_list = []
    no_poll_cmds = ["logs", "log", "list", "history", "new"]
    def __init__(self):
        self.poll_list = list(self.poll_collection.find({}))
        if len(self.poll_list) > 0:
            self.poll_id = self.poll_list[-1]['poll_id'] + 1
        pass

    def execute(self, serv, canal, handle, message):
        message = message.lower()
        cmd = utils.extract_command(message)
        
        if message == "h" or message == "help" or message.strip() == "":
            serv.notice(handle,"Command : !vote <action>")
            serv.notice(handle,"actions :")
            serv.notice(handle,"    new <poll_name>")
            serv.notice(handle,"    y")
            serv.notice(handle,"    n")
            serv.notice(handle,"    results")
            serv.notice(handle,"    clear")
            serv.notice(handle,"    DESACTIVATED (ask win and Aste ..) log (aliases : history, logs, list)")
        elif self.current_poll == "" and "new" in message:
            if utils.extract_message(message, "").strip() == "":
                serv.privmsg(canal,"You have to give a name ! You stupid winw")
            else:
                self.current_poll = utils.extract_message(message, "")
                serv.privmsg(canal,"New poll created : " + self.current_poll)
                self.insert_database()
        elif self.current_poll != "" and "new" in message:
            serv.privmsg(canal,"You can't create a new poll, because poll " + self.current_poll + " is not cleared")
        elif self.current_poll == "" and cmd not in self.no_poll_cmds:
            serv.privmsg(canal,"No poll currently running. !vote new <poll> or !vote history") 
        elif message == "y" or message == "n":
            if handle not in self.nicks:
                self.nicks.append(handle)
                if message == "y":
                    self.countY += 1
                    serv.privmsg(canal,"Y - " + str(self.countY) + "/" + str(self.countN) + " - N") 
                elif message == "n":
                    self.countN += 1
                    serv.privmsg(canal,"Y - " + str(self.countY) + "/" + str(self.countN) + " - N")
            else:
                serv.privmsg(canal,"<" + handle + "> : You've already voted for poll " + str(self.poll_id))
#        elif
        elif message == "clear":
            self.poll_list.append({"poll_id": self.poll_id, "name": self.current_poll, "y": str(self.countY), "n": str(self.countN), "nicks": self.nicks})
            self.update_database()
            self.poll_id += 1
            self.current_poll = ""
            self.countY = 0
            self.nicks = []
            self.countN = 0
            serv.privmsg(canal, "Poll Nb " + str(self.poll_id - 1) + " saved and cleared.")
        elif message == "results":
            serv.privmsg(canal, "Results for poll " + self.current_poll)
            serv.privmsg(canal, "Yes : " + str(self.countY))
            serv.privmsg(canal, "No  : " + str(self.countN))
        elif message in ["logs", "log", "list", "history"] and 1==0:
            if len(self.poll_list) == 0:
                serv.privmsg(canal, "Empty history.")
            else:
                serv.privmsg(canal, "History of " + str(len(self.poll_list)) + " polls in notice")
                for poll in self.poll_list:
                    serv.notice(handle, "Poll " + str(poll["poll_id"]) + " : " + poll["name"])
                    serv.notice(handle, "Y - " + str(poll["y"]) + "/" + str(poll["n"]) + " - N")
        else:
            serv.notice(handle,"Command : !vote <action>")
            serv.notice(handle,"actions :")
            serv.notice(handle,"    new <poll_name>")
            serv.notice(handle,"    y")
            serv.notice(handle,"    n")
            serv.notice(handle,"    results")
            serv.notice(handle,"    clear")
            serv.notice(handle,"    DESACTIVATED (ask win and Aste ..) log (aliases : history, logs, list)")
        if self.current_poll != "":
            self.update_database()

    def update_database(self):
        self.poll_collection.update({'poll_id': self.poll_id}, {'$set': {'y': str(self.countY)}})
        self.poll_collection.update({'poll_id': self.poll_id}, {'$set': {'n': str(self.countN)}})
        self.poll_collection.update({'poll_id': self.poll_id}, {'$set': {'nicks': self.nicks}})
    def insert_database(self):
        self.poll_collection.insert({'poll_id': self.poll_id, 'name': self.current_poll, 'y': str(self.countY), 'n': str(self.countN), 'nicks': self.nicks})
