import threading
import time
import logging
from exceptions.KrakenAPICallRateException import KrakenAPICallRateException


class KrakenAPICallRateManager(object):
    """Kraken api call rate manager"""

    def __init__(self, tier_level):
        """
        Kraken api call rate manager constructor
        :param tier_level:
        """
        self._tier_level = tier_level

        if self._tier_level > 2:
            self._max_api_call_counter = 20
            self._decrease_counter_after_sec = 2
        elif self._tier_level == 2:
            self._max_api_call_counter = 15
            self._decrease_counter_after_sec = 3
        else:
            raise KrakenAPICallRateException("The given tier level (%d) doesn't grant enought rights to use the kraken "
                                             "api" % self._tier_level)

        self._api_call_counter = 0
        self._t = threading.Thread(target=self._worker)
        self._t_run = True
        self._lock = threading.RLock()

        logging.info("KrakenAPICallRateManager initialized for tier level %s." % self._tier_level)
        logging.info("Api call rate counter is initialized at 0. Max api call counter is %d."
                     % self._max_api_call_counter)
        logging.info("Api call counter is decreased by 1 every %s sec" % self._decrease_counter_after_sec)

    def increase_api_call_rate(self, number_to_add):
        """
        Increase the api call counter by a number
        :param number_to_add: Number to add to the the api call counter
        :type number_to_add: int
        """
        with self._lock:
            if self._api_call_counter + number_to_add > self._max_api_call_counter:
                raise KrakenAPICallRateException("Max api call counter reached!")
            else:
                self._api_call_counter += number_to_add

    def start(self):
        """Starts the api call counter computer (worker)"""
        self._t.start()

    def stop(self):
        """Stops the api call counter computer (worker)"""
        self._t_run = False

    def _worker(self):
        """Threaded function that decrease the api call counter after an amount of time"""
        while self._t_run:
            time.sleep(self._decrease_counter_after_sec)
            with self._lock:
                if self._api_call_counter > 0:
                    self._api_call_counter -= 1
