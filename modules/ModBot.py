class ModBot:

    dico = ['test', 'romain']
    current_word = ""
    currently_playing = False

    def __init__(self):
        pass

    def execute(self, serv, canal, handle, message):
        if not self.currently_playing:
            self.current_word = self.dico[0]
            self.current_word.sort()
            serv.privmsg(canal, self.current_word)
        else:
            for letter in message:
                if letter not in self.current_word:
                    return False
            return len(message)