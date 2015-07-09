from bot import BetezedBot
import config

if __name__ == "__main__":
    try:
        BetezedBot().start()

    except KeyboardInterrupt:
        print "user interruption"
