class ModSay:
    def __init__(self):
        pass

    def execute(self, serv, canal, handle, message):
        if "Pixis" == handle:
            message = message.split(" ")
            serv.privmsg("Pixis", str(message))