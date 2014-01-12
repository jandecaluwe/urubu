def datetimeformat(value, format="%d-%b-%Y"):
    return value.strftime(format)

filters = {}
filters['datetimeformat'] = datetimeformat
