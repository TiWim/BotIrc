import urllib2
class ModNc:
    def __init__(self):
        pass
    def execute(self, serv, canal, handle, message):
        if "aspi" not in str(message):
	    message = message.strip().replace(" ", "%20")
            url = "http://www.newbiecontest.org/index.php?page=info_membre&nick=" + str(message)
            response = urllib2.urlopen(url)
            if "Erreur !" not in response.read():
                serv.privmsg(canal, "http://www.newbiecontest.org/index.php?page=info_membre&nick=" + str(message))
            else:
                serv.privmsg(canal, "Ce membre n'existe pas")
        else:
            serv.privmsg(canal, "Ben voyons ...")
        
