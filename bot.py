# -*- coding: utf-8 -*-
# from config import Config
import time
from lib import ircbot, irclib
import re
from modules import ModSay, ModBot, ModRmd5, ModMd5, ModHelp, utils
# , ModStat, ModVote


class BetezedBot(ircbot.SingleServerIRCBot):
    # config = Config()
    admin = ["Pixis", "TiWim"]  # "Betezed"]
    first_flood = True
    last_time = time.time()
    current_time = 99999999999
    canal = "#Bots_room"  # "#open-newbiecontest"
    # canal = "#0x90r00t"
    server = "irc.root-me.org"  # "irc.worldnet.net"
    port = 6667
    canal_test = canal  # "#pixistest"
    name = "PixiBot"
    flood_time = 3
    mods = {
        ModSay: {"module": "modules.ModSay.ModSay",
                 "instance": None,
                 "enabled": True,
                 "cmd": "!say"},
#        ModVote: {"module": "modules.ModVote.ModVote",
#                  "instance": None,
#                  "enabled": False,
#                  "cmd": "!vote"},
        ModBot: {"module": "modules.ModBot.ModBot",
                 "instance": None,
                 "enabled": True,
                 "cmd": "!bot"},
#        ModStat: {"module": "modules.ModStat.ModStat",
#                  "instance": None,
#                  "enabled": True,
#                  "cmd": "!stat"},
        ModRmd5: {"module": "modules.ModRmd5.ModRmd5",
                  "instance": None,
                  "enabled": True,
                  "cmd": "!rmd5"},
        ModMd5: {"module": "modules.ModMd5.ModMd5",
                 "instance": None,
                 "enabled": True,
                 "cmd": "!md5"},
        ModHelp: {"module": "modules.ModHelp.ModHelp",
                  "instance": None,
                  "enabled": True,
                  "cmd": "!help"}
    }

    def __init__(self):
        utils.logs("Bot start " + self.name)
        ircbot.SingleServerIRCBot.__init__(self, [(self.server, self.port)],
                                           self.name, "Bot de Pixis", 10)
        self.init_mods()

    def on_welcome(self, serv, ev):
        serv.join(self.canal)
        # serv.join("#nboobz_cmb")
        # serv.join("#0x90r00t")
        # serv.join(self.canal_test)
  #      serv.privmsg('NickServ', "IDENTIFY " + self.config.password)

    def on_join(self, serv, ev):
        handle = irclib.nm_to_n(ev.source())
        canal = ev.target()

    def on_kick(self, serv, ev):
        canal = ev.target()
        time.sleep(2)
        serv.join(canal)

    def on_pubmsg(self, serv, ev):
        handle = irclib.nm_to_n(ev.source())
        canal = ev.target()
        message = ev.arguments()[0]
        utils.logs(message)
        if handle in self.admin:
            if '!reload' in message:
                custom_message = utils.extract_message(message, '!reload')
                self.check_reload(serv, canal, handle, custom_message)
            if '!enable' in message:
                custom_message = utils.extract_message(message, '!enable')
                self.enable(serv, canal, handle, custom_message, True)
            if '!disable' in message:
                custom_message = utils.extract_message(message, '!disable')
                self.enable(serv, canal, handle, custom_message, False)
        for mod, value in self.mods.items():
            if value['cmd'] == message or re.match(r'^' + value['cmd'] + " ",
                                                   message) is not None:
                if not self.check_flood(serv, canal, handle):
                    if self.mods[mod]['enabled']:
                        custom_message = utils.extract_message(message,
                                                               value['cmd'])
                        self.mods[mod]['instance'].execute(serv, canal, handle,
                                                           custom_message)
                    else:
                        serv.privmsg(canal, "Disabled")

    def on_privmsg(self, serv, ev):
        handle = irclib.nm_to_n(ev.source())
        canal = ev.target()
        message = ev.arguments()[0]
        for mod, value in self.mods.items():
            if value['cmd'] == message or re.match(r'^' + value['cmd'] + " ",
                    message) is not None:
                if not self.check_flood(serv, canal, handle):
                    custom_message = utils.extract_message(message,
                                                           value['cmd'])
                    self.mods[mod]['instance'].execute(serv, canal, handle,
                                                       custom_message)

    def check_flood(self, serv, canal, handle):
        self.current_time = time.time()
        if self.current_time - self.last_time < self.flood_time and handle not in self.admin:
            print "Flood : " + str(self.current_time) + " - " + str(self.last_time)
            self.last_time = time.time()
            if self.first_flood:
                serv.privmsg(canal, "Hey doucement " + handle +
                             ", je ne suis pas un robot !")
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
            mod_loaded = mod_loaded + " " + module
            key = reload(key)
        serv.privmsg(canal, "* Reload des modules" + mod_loaded + " *")
        self.init_mods()

    def enable(self, serv, canal, handle, message, enable):
        for mod, value in self.mods.items():
            if value['cmd'].strip("!") == message.strip():
                if self.mods[mod]['enabled'] == enable:
                    if enable:
                        serv.privmsg(canal, message + " already enabled !")
                    else:
                        serv.privmsg(canal, message + " already disabled !")
                else:
                    self.mods[mod]['enabled'] = enable
                    if not enable:
                        serv.privmsg(canal, message + " disabled !")
                    else:
                        serv.privmsg(canal, message + " enabled !")

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
                    logfile.write(value['cmd'] + " " + custom_message +
                                  " (raw : " + message + ")\n")
