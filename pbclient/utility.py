def bytify(s):
    if issubclass(s.__class__, str) is True:
        return s.encode('ASCII')
    else:
        return s

def stringify(b):
    if issubclass(b.__class__, bytes) is True:
        return b.decode('ASCII')
    else:
        return b

