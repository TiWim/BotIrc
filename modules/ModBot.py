import irclib
import ircbot

class ModBot:
    def __init__(self):
        pass

    def execute(self, serv, canal, handle, message):
        serv.privmsg(canal, "Ya pas de bot ici !")