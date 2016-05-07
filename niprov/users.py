import getpass

class Users(object):

    def __init__(self, dependencies):
        self.config = dependencies.getConfiguration()

    def determineUser(self, passedUserValue):
        """Determine the name of the user creating provenance.

        The following methods will be tried to determine the username;
        1) The passedUserValue argument if not None
        2) The configuration file or setting has a value for the key user
        3) The OS username.

        Args:
            passedUserValue (str): This value will override any other method
                to determine the username.

        Returns:
            string: The username or handle of the user.
        """
        if passedUserValue is not None:
            return passedUserValue
        if self.config.user:
            return self.config.user
        else:
            return getpass.getuser()
