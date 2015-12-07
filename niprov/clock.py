import datetime


class Clock(object):

    def getNowString(self):
        now = datetime.datetime.now()
        return str(now).replace(' ','_').replace(':','-').split('.')[0]
