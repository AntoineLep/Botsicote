from exceptions.BotsicoteException import BotsicoteException


class KrakenAPICallRateException(BotsicoteException):
    """Kraken api call rate exception"""

    def __init__(self, message):
        super(KrakenAPICallRateException, self).__init__(message)
