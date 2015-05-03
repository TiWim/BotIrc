class ModBot:

    dico = ['test', 'romain']
    current_word = ""
    currently_playing = False

    def __init__(self):
        pass

    def execute(self, serv, canal, handle, message):
        if "Pixis" == handle:
            message = message.split(" ")
            serv.privmsg("Pixis", str(message))