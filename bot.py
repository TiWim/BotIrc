import irclib
import ircbot
import random
import urllib2
import re
import time
from datetime import date
import operator
import hashlib

from apiclient.discovery import build
class BetezedBot(ircbot.SingleServerIRCBot):
    count_daily_message = {} 
    yesterday = date.today().day
    first_flood = True
    last_time = time.time()
    current_time = 99999999999
    canal = "#open-newbiecontest"
    canal_test = "#pixistest"
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
    commands = { 
        "bot" : "Reveille le bot",
        "boobies" : "Afficher une image de BonjourMadame",
        "md5" : "Calcul du md5 d'une chaine",
        "rmd5" : "Cherche le reverse md5 d'un md5",
        "stat" : "Sans argument, affiche le nombre de post et le premier posteur. Avec un chiffre X (X<6), affiche le top X des posteurs"
    }
    def __init__(self):
        ircbot.SingleServerIRCBot.__init__(self, [("irc.worldnet.net", 6667)], self.name, "Bot de Pixis")

    def on_welcome(self, serv, ev):
        serv.join(self.canal)
        #serv.join(self.canal_test)

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
        if date.today().day != self.yesterday:
            self.yesterday = date.today().day
            self.count_daily_message = {}
        handle = irclib.nm_to_n(ev.source())
        if handle not in self.count_daily_message.keys():
            self.count_daily_message[handle] = 0
        self.count_daily_message[handle] += 1
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
        if "!stat" in message and "!stats" not in message:
            c_message = message
            c_message = c_message.split("!stat ", 1)
            if len(c_message) > 1:
                c_message = c_message[1]
            else:
                c_message = ""
            total = 0
            for item in self.count_daily_message:
                total += self.count_daily_message[item]
            sorted_x = sorted(self.count_daily_message.items(), key=operator.itemgetter(1), reverse=True)
            first_poster = sorted_x[0][0]
            first_poster_messages = sorted_x[0][1]
            if total > 1:
                message_spell = "messages"
            else:
                message_spell = "message"
            serv.privmsg(handle, "Il y a eu \002" + str(total) + " " + message_spell + "\017 aujourd'hui sur \002" + self.canal)
            if (first_poster_messages > 1):
                message_spell = "messages"
            else:
                message_spell = "message"

            serv.privmsg(handle, first_poster + " est le plus bavard avec " + str(first_poster_messages) + " " + message_spell + " aujourd'hui !")
            if self.is_numeric(c_message):
                c_message = int(c_message)
                print "On va afficher les " + str(c_message) + " dernieres stats"
                if c_message > 5:
                    serv.privmsg(handle, "(L'historique ne remonte qu'aux 5 premiers posteurs de la journee)")
                    c_message = 5 
                for num in range(1, min(c_message, len(sorted_x))):
                    rank = num
                    rank +=1
                    if sorted_x[num][1] > 1:
                        message_spell = "messages"
                    else:
                        message_spell = "message"
                    serv.privmsg(handle, str(rank) + ". " + sorted_x[num][0] + ": " + str(sorted_x[num][1]) + " " + message_spell)

        if "!rmd5 " in message:
            c_message = message
            c_message = c_message.split("!rmd5 ", 1) 
            if len(c_message) > 1:
                c_message = c_message[1]
            else:
                c_message = ""
            url = "http://md5.gromweb.com/?md5=" + str(c_message)
            response = urllib2.urlopen(url)
            response = response.read()
            reObj = re.search("succesfully reversed into the string (.*)\.</p>", response)
            if (reObj is not None):
                string = reObj.group(1)
                string = string[2:-2]
            else:
                string = "No match"
            serv.privmsg(self.canal, "rmd5(" + c_message + ") = " + string)


        if "!md5 " in message:
            c_message = message
            c_message = c_message.split("!md5 ", 1)
            if len(c_message) > 1:
               c_message = c_message[1]
            else:
               c_message = ""
            m = hashlib.md5()
            m.update(c_message)
            serv.privmsg(self.canal, "md5(" + c_message +") = " + m.hexdigest())
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

    def is_numeric(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

        
