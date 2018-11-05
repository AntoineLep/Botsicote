from CryptoPairManager import CryptoPairManager


class Strategy(object):
    """Base class for strategies"""

    def __init__(self):
        """Strategy constructor"""
        self._crypto_pair_manager_list = None
        self._lock = None
        self._k = None
        self._call_rate_manager = None

    def run(self):
        """Run the strategy"""
        try:
            self.startup()
            self.run_strategy()
        except:
            self.cleanup()
            raise

        self.cleanup()

    def startup(self):
        """Method called at the beginning of the strategy execution"""
        raise NotImplementedError("startup method must be override")

    def run_strategy(self):
        """Method in which is performed the strategy logic"""
        raise NotImplementedError("run_strategy method must be override")

    def cleanup(self):
        """Method called at the end of the strategy execution"""
        raise NotImplementedError("cleanup method must be override")

    def set_crypto_pair_manager_list(self, crypto_pair_manager_list):
        """
        Set the crypto pair manager list

        :param crypto_pair_manager_list: The crypto pair manager list
        :type crypto_pair_manager_list: list[CryptoPairManager]
        """
        self._crypto_pair_manager_list = crypto_pair_manager_list

    def get_crypto_pair_manager_list(self):
        """
        Get the crypto pair manager list

        :return: The crypto pair manager
        :rtype: list[CryptoPairManager]
        """
        return self._crypto_pair_manager_list

    def set_lock(self, lock):
        """
        Set the lock

        :param lock: Lock used for data update
        :type lock: threading.Lock
        """
        self._lock = lock

    def get_lock(self):
        """
        Get the lock

        :return: The lock used for data update
        :rtype: threading.Lock
        """
        return self._lock

    def set_kraken_api_instance(self, k):
        """
        Set the kraken api instance

        :param k: The kraken api instance
        :type k: krakenex.API
        """
        self._k = k

    def get_kraken_api_instance(self):
        """
        Get the kraken api instance

        :return: The kraken api instance
        :rtype: krakenex.API
        """
        return self._k

    def set_call_rate_manager(self, call_rate_manager):
        """
        Set the call rate manager

        :param call_rate_manager: The call rate manager
        :type call_rate_manager: KrakenAPICallRateManager
        """
        self._call_rate_manager = call_rate_manager

    def get_call_rate_manager(self):
        """
        Get the call rate manager

        :return: The call rate manager
        :rtype: KrakenAPICallRateManager
        """
        return self._call_rate_manager
