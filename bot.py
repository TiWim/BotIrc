import irclib
import ircbot
import random
import urllib2
import re
import time
from apiclient.discovery import build
class BetezedBot(ircbot.SingleServerIRCBot):
    first_flood = True
    last_time = time.time()
    current_time = 99999999999
    canal = "#open-newbiecontest"
    #canal = "#pixistest"
    name = "PixiBot"
    hello_phrases = [
        "Salut ",
        "Hey ",
        "Yop ",
        "Bonjour ",
        "Hellooo ",
        "Coucou ",
        "Yop yop ",
        "Bienvenue ",
        "Moi aussi je suis relou avec mes messages auto ! Salut quand meme "
    ]
    def __init__(self):
        ircbot.SingleServerIRCBot.__init__(self, [("irc.worldnet.net", 6667)], self.name, "Bot de Pixis")

    def on_welcome(self, serv, ev):
        serv.join(self.canal)

    def on_join(self, serv, ev):
        handle = irclib.nm_to_n(ev.source())
        canal = ev.target()
        if (handle != self.name): 
            phrase = random.randrange(0, len(self.hello_phrases))
            #serv.privmsg(self.canal, self.hello_phrases[phrase] + handle)

    def on_kick(self, serv, ev):
        time.sleep(2)
        serv.join(self.canal)

    def on_pubmsg(self, serv, ev):
        handle = irclib.nm_to_n(ev.source())
        message = ev.arguments()[0]
        if self.name.lower() in message.lower():
            if not self.check_flood(serv, ev, handle):
                serv.privmsg(self.canal, "Que .. Quoi ? Qui me parle ?"); 
        if "!bot" in message:
            if not self.check_flood(serv, ev, handle):
                print "!bot"
                serv.privmsg(self.canal, "Ya pas de bot ici !");
        if "!boobies" in message:
            if not self.check_flood(serv, ev, handle):
                page = random.randrange(0, 2000)
                url = "http://www.bonjourmadame.fr/page/" + str(page)
                response = urllib2.urlopen(url)
                print "Madame, page " + url 
                response = response.read()
                reObj = re.search("src=\"([A-Za-z:/\.0-9_]*)\" alt=\"", response)
                print reObj.group(1)
                serv.privmsg(self.canal, handle + " -=- Bonjour Madame ! -=- " + reObj.group(1))
        if "!reload" + self.name.lower() in message.lower():
            print "test reload"
        if "!google " in message:
            if not self.check_flood(serv, ev, handle):
                message = message.split("!google ", 1)
                message = message[1]
                service = build("customsearch", "v1",
                    developerKey="AIzaSyCy6tveUHlfNQDUtH0TJrF6PtU0h894S2I")
                res = service.cse().list(
                    q = message,
                    cx = '005983647730461686104:qfayqkczxfg',
                ).execute()
                if 1 <= res['queries']['request'][0]['totalResults']:
                    if res.has_key('items'):
                        result = res['items'][0]
                    else:
                        result = {} 
                        result['link'] = "Not found"
                        result['snippet'] = ""
                    url = result['link']
                    description = result['snippet']
                    google = "\002\00307G \00302O \00303O \00305G \00304L \00309E \017 \00399 "
#                    serv.privmsg(self.canal, google + url)
#                    if description != "":
#                        serv.privmsg(self.canal, "\002" + description) 
                else:
                        response = 'Not found: ' + terms[1]
                
    def check_flood(self, serv, ev, handle):
        self.current_time = time.time()
        if (self.current_time - self.last_time < 3):
            print "Flood : " + str(self.current_time) + " - " + str(self.last_time)
            self.last_time = time.time()
            if (self.first_flood):
                serv.privmsg(self.canal, "Hey doucement " + handle + ", je ne suis pas un robot !")
                self.first_flood = False
            return True;
        else:
            self.first_flood = True
            self.last_time = time.time()
            return False;

        
