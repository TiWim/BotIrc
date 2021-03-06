import time

def is_numeric(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def extract_message(s, mod):
    s = s.split(mod + " ", 1)
    if len(s) > 1:
        return s[1]
    else:
        return ""
def extract_command(s):
    s = s.split(" ", 1)
    return s[0]


def get_class(cls):
    parts = cls.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m

def logs(message, level="INFO"):
    """
    Used to uniformise log reports

    Params:
        message         Message to print in logs

    Output:
        Date Level Message

    """
    print time.strftime("%d-%m-%y %H:%M:%S"), level, message
