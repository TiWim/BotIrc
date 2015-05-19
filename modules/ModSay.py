class ModSay:
    def __init__(self):
        pass

    def execute(self, serv, canal, handle, message):
        if "pixis" == handle.lower():
            message = message.split(" ", 1)
            cmd = message[0]
            send_mess = message[1]
            print(cmd)
            print(send_mess)
            serv.send_raw(cmd + " " + send_mess)
