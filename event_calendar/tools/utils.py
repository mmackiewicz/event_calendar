__author__ = 'Marek Mackiewicz'

import datetime

def validate_date(date_str):
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return False
    else:
        return True
