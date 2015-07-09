class ModHelp:
    def __init__(self):
        pass

    def execute(self, serv, canal, handle, message):
        # Displays all commands
        serv.privmsg(canal, "[ " + handle + " ] !md5 <String> - !rmd5 <md5> - !stat <number> - !help")
