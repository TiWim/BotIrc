import time
import irclib
import ircbot
from modules import ModBot, ModBoobies, ModStat, ModRmd5, ModMd5, utils


class BetezedBot(ircbot.SingleServerIRCBot):
    first_flood = True
    last_time = time.time()
    current_time = 99999999999
    canal = "#open-newbiecontest"
    canal_test = "#pixistest"
    name = "PixiBot"
    flood_time = 3
    mods = [
        ModBot,
        ModBoobies,
        ModStat,
        ModRmd5,
        ModMd5,
        utils
    ]
    bots = {
        "!bot": None,
        "!boobies": None,
        "!md5": None,
        "!rmd5": None,
        "!stat": None
    }


    def __init__(self):
        ircbot.SingleServerIRCBot.__init__(self, [("irc.worldnet.net", 6667)], self.name, "Bot de Pixis")
        self.init_bots()

    def on_welcome(self, serv, ev):
        #serv.join(self.canal)
        serv.join(self.canal_test)

    def on_kick(self, serv, ev):
        canal = ev.target()
        time.sleep(2)
        serv.join(canal)

    def on_pubmsg(self, serv, ev):
        handle = irclib.nm_to_n(ev.source())
        canal = ev.target()
        message = ev.arguments()[0]
        self.bots['!stat'].update_counts(handle)
        if '!reloadPix' == message:
            self.check_reload()
        for mod, value in self.bots.items():
            if mod in message:
                if not self.check_flood(serv, handle):
                    custom_message = utils.extract_message(message, mod)
                    self.bots[mod].execute(serv, canal, handle, custom_message)

    def check_flood(self, serv, handle):
        self.current_time = time.time()
        if self.current_time - self.last_time < self.flood_time:
            print "Flood : " + str(self.current_time) + " - " + str(self.last_time)
            self.last_time = time.time()
            if self.first_flood:
                serv.privmsg(self.canal, "Hey doucement " + handle + ", je ne suis pas un robot !")
                self.first_flood = False
            return True
        else:
            self.first_flood = True
            self.last_time = time.time()
            return False
        
    def check_reload(self):
        for value in self.mods:
            value = reload(value)
        self.init_bots()

    def init_bots(self):
        self.bots = {
            "!bot": self.get_class('modules.ModBot.ModBot')(),
            "!boobies": ModBoobies.ModBoobies(),
            "!md5": ModMd5.ModMd5(),
            "!rmd5": ModRmd5.ModRmd5(),
            "!stat": ModStat.ModStat()
        }

    def get_class(self, kls):
        parts = kls.split('.')
        module = ".".join(parts[:-1])
        m = __import__( module )
        for comp in parts[1:]:
            m = getattr(m, comp)
        return m
