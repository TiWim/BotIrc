class ModHelp:
    def __init__(self):
        pass

    def execute(self, serv, canal, handle, message):
        serv.privmsg(canal, "[ " + handle + " ] !boobies - !md5 <String> - !rmd5 <md5> - !stat [1, 2, 3, ...] - !help")