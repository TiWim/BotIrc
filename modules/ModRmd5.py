import urllib2
import re

class ModRmd5:
    def __init__(self):
        pass

    def execute(self, serv, canal, handle, message):
        url = "http://md5.gromweb.com/?md5=" + str(message)
        response = urllib2.urlopen(url)
        response = response.read()
        reObj = re.search("succesfully reversed into the string (.*)\.</p>", response)
        if reObj is not None:
            string = reObj.group(1)
            string = string[2:-2]
        else:
            string = "No match"
        serv.privmsg(canal, "rmd5(" + message + ") = " + string)
