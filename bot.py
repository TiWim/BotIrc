import time
from lib import ircbot, irclib
from modules import ModBot, ModBoobies, ModStat, ModRmd5, ModMd5, utils


class BetezedBot(ircbot.SingleServerIRCBot):
    first_flood = True
    last_time = time.time()
    current_time = 99999999999
    canal = "#open-newbiecontest"
    canal_test = "#pixistest"
    name = "PixiBot"
    flood_time = 3
    mods = {
        ModBot: {"module": "modules.ModBot.ModBot",
                 "instance": None,
                 "cmd": "!bot"},
        ModBoobies: {"module": "modules.ModBoobies.ModBoobies",
                     "instance": None,
                     "cmd": "!boobies"},
        ModStat: {"module": "modules.ModStat.ModStat",
                  "instance": None,
                  "cmd": "!stat"},
        ModRmd5: {"module": "modules.ModRmd5.ModRmd5",
                  "instance": None,
                  "cmd": "!rmd5"},
        ModMd5: {"module": "modules.ModMd5.ModMd5",
                 "instance": None,
                 "cmd": "!md5"}
    }

    def __init__(self):
        print "Bot start " + self.name
        ircbot.SingleServerIRCBot.__init__(self, [("irc.worldnet.net", 6667)], self.name, "Bot de Pixis")
        self.init_mods()

    def on_welcome(self, serv, ev):
        serv.join(self.canal)
        #serv.join(self.canal_test)

    def on_kick(self, serv, ev):
        canal = ev.target()
        time.sleep(2)
        serv.join(canal)

    def on_pubmsg(self, serv, ev):
        handle = irclib.nm_to_n(ev.source())
        canal = ev.target()
        message = ev.arguments()[0]
        self.log_message(message)
        self.mods[ModStat]['instance'].update_counts(handle)
        if '!reload' in message and "Pixis" == handle:
            custom_message = utils.extract_message(message, '!reload')
            self.check_reload(serv, canal, handle, custom_message)
        for mod, value in self.mods.items():
            if value['cmd'] == message or value['cmd'] + " " in message:
                if not self.check_flood(serv, canal, handle):
                    custom_message = utils.extract_message(message, value['cmd'])
                    self.mods[mod]['instance'].execute(serv, canal, handle, custom_message)

    def check_flood(self, serv, canal, handle):
        self.current_time = time.time()
        if self.current_time - self.last_time < self.flood_time:
            print "Flood : " + str(self.current_time) + " - " + str(self.last_time)
            self.last_time = time.time()
            if self.first_flood:
                serv.privmsg(canal, "Hey doucement " + handle + ", je ne suis pas un robot !")
                self.first_flood = False
            return True
        else:
            self.first_flood = True
            self.last_time = time.time()
            return False

    def check_reload(self, serv, canal, handle, message):
        mod_loaded = ""
        for key, value in self.mods.items():
            parts = value['module'].split(".")
            module = parts[2]
            if module != "ModStat" or "force" == message:
                mod_loaded = mod_loaded + " " + module
                key = reload(key)
        serv.privmsg(canal, "* Reload des modules" + mod_loaded + " *")
        self.init_mods()

    def init_mods(self):
        for key, mod in self.mods.items():
            self.mods[key]['instance'] = utils.get_class(mod['module'])()

    def log_message(self, message):
        if self.name in message:
            with open("log.txt", "a") as logfile:
                logfile.write("raw : " + message + "\n")
        if "pixis" in message.lower():
            with open("log.txt", "a") as logfile:
                logfile.write("** " + message + " **\n")
        for mod, value in self.mods.items():
            if value['cmd'] in message:
                custom_message = utils.extract_message(message, value['cmd'])
                with open("log.txt", "a") as logfile:
                    logfile.write(value['cmd'] + " " + custom_message + " (raw : " + message + ")\n")
