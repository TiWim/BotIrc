class ModSay:
    def __init__(self):
        pass

    def execute(self, serv, canal, handle, message):
        if "Pixis" == handle:
            message = message.split(" ", 1)
            if len(message) == 1:
                send_serv = "#open-newbiecontest"
                send_mess = message[0]
            else:
                send_serv = message[0]
                send_mess = message[1]
            serv.privmsg(send_serv, send_mess)