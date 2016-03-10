import getpass

class Users(object):

    def __init__(self, dependencies):
        self.config = dependencies.getConfiguration()

    def determineUser(self, passedUserValue):
        if passedUserValue is not None:
            return passedUserValue
        if self.config.user:
            return self.config.user
        else:
            return getpass.getuser()
