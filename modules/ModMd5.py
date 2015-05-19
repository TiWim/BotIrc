import hashlib
import urllib2


class ModMd5:
    def __init__(self):
        pass

    def execute(self, serv, canal, handle, message):
        m = hashlib.md5()
        m.update(message)
        serv.privmsg(canal, "md5(" + message + ") = " + m.hexdigest())
	url = "http://md5.gromweb.com/?string=" + str(message)
        response = urllib2.urlopen(url)
