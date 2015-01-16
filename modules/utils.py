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
