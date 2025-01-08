import datetime

LOGFILE = './log.txt'


def log(message, error=False):
    pre = str(datetime.datetime.now())
    if error:
        pre = ' ERROR - '
    with open(LOGFILE, 'a') as f:
        f.write(message + '\n')
