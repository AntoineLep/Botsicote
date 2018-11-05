class BotsicoteException(Exception):
    """Generic botsicote exception"""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "/!\ BOTSICOTE EXCEPTION: " + self.message
