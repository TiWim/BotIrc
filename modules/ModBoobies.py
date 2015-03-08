import random
import urllib2
import re


class ModBoobies:
    def __init__(self):
        pass

    def execute(self, serv, canal, handle, message):
        page = random.randrange(0, 2000)
        url = "http://www.bonjourmadame.fr/page/" + str(page)
        response = urllib2.urlopen(url)
        print "Madame, page " + url
        response = response.read()
        reObj = re.search("src=\"([A-Za-z:/\.0-9_]*)\" alt=\"", response)
        print reObj.group(1)
        serv.privmsg(canal, handle + " -=- Bonjour Madame ! -=- " + reObj.group(1))