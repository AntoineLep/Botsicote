import logging
import threading
import time
from datetime import datetime

from requests.exceptions import HTTPError

from StockDataManager import StockDataManager
from Utils import format_raw_data
from exceptions.KrakenAPICallRateException import KrakenAPICallRateException

API_DELAY = 5
CHECK_SERVER_TIME_EVERY_SEC = 60


class TimeFrameManager(object):
    """Time frame manager"""

    _LAST_SERVER_TIME_CHECK = datetime(2017, 12, 25, 0, 0, 0)
    _LAST_API_SERVER_TIME = 0
    _SERVER_TIME = 0

    def __init__(self, time_frame_length, pair, pair2, krakenex_instance, call_rate_manager, lock):
        """
        Time frame manager constructor

        :param time_frame_length: The length of the time frame in minute
        :type time_frame_length: int
        :param pair: Name of the key to retrieve data after an OHLC api call (default Xcrypto followed by Zcurrency)
        :type pair: str
        :param pair2: Name of the key to retrieve data after an OHLC api call (default Xcrypto followed by Zcurrency)
        :type pair2: str
        :param krakenex_instance: Instance of krakenex
        :type krakenex_instance: Krakenex
        :param call_rate_manager: The kraken api call rate manager
        :type call_rate_manager: KrakenAPICallRateManager
        :param lock: The threading lock
        :type lock: threading.Lock
        """
        self._time_frame_length = time_frame_length
        self._pair = pair
        self._pair2 = pair2
        self.stock_data_manager = StockDataManager()
        self._since_cursor = 0
        self._k = krakenex_instance
        self._call_rate_manager = call_rate_manager
        self._t_run = True
        self._t = threading.Thread(target=self._worker)
        self._lock = lock
        self.last_update_datetime = None
        logging.info("New time frame manager created! Pair: %s, time frame: %d min"
                     % (self._pair, self._time_frame_length))

    def feed(self):
        """Feed the stock data managers with new values"""
        response, self._since_cursor = self._feed(self._since_cursor, self._time_frame_length)
        self.stock_data_manager.update_data(format_raw_data(response, self._time_frame_length * 60, self._pair2))
        self.last_update_datetime = datetime.now()

    def _feed(self, cursor, interval):
        """
        Feed the stock data managers with new values

        :param cursor: Timestamp of last data age
        :type cursor: int
        :param interval: Time frame
        :type interval: int
        :return: A tuple containing the http request response and the new cursor value
        :rtype: tuple
        """
        while True:
            try:
                logging.info("Retrieving %s OHLC data for %d min interval" % (self._pair, interval))
                self._call_rate_manager.increase_api_call_rate(1)
                response = self._k.query_public("OHLC",
                                                data={"pair": self._pair, "since": cursor, "interval": interval})
                return response, max([item[0] for item in response["result"][self._pair2]])
            except HTTPError as http_err:
                logging.warning("Http request failed, trying again... Details: %s" % str(http_err))
            except KrakenAPICallRateException as api_call_rate_err:
                logging.warning("API call rate error, trying again... Details: %s" % str(api_call_rate_err))
                time.sleep(1)
            except KeyError as key_err:
                logging.warning("Data format error, trying again... Details: %s" % str(key_err))

    def start(self):
        """Starts the time frame manager (worker)"""
        self._t.start()

    def stop(self):
        """Stops the time frame manager (worker)"""
        self._t_run = False

    def _worker(self):
        """Threaded function that retrieve the OHLC data"""
        while self._t_run:
            with self._lock:
                while self._t_run:
                    try:
                        td = datetime.now() - TimeFrameManager._LAST_SERVER_TIME_CHECK
                        if td.total_seconds() > CHECK_SERVER_TIME_EVERY_SEC:
                            self._call_rate_manager.increase_api_call_rate(1)
                            response = self._k.query_public("Time")
                            TimeFrameManager._SERVER_TIME = response["result"]["unixtime"]
                            TimeFrameManager._LAST_API_SERVER_TIME = response["result"]["unixtime"]
                            TimeFrameManager._LAST_SERVER_TIME_CHECK = datetime.now()
                        else:
                            TimeFrameManager._SERVER_TIME = TimeFrameManager._LAST_API_SERVER_TIME + \
                                                            int(td.total_seconds())
                        break
                    except HTTPError as http_err:
                        logging.warning("Http request failed, trying again... Details: %s" % str(http_err))
                    except KrakenAPICallRateException as api_call_rate_err:
                        logging.warning("API call rate error, trying again... Details: %s" % str(api_call_rate_err))
                        time.sleep(1)
                    except KeyError as key_err:
                        logging.warning("Data format error, trying again... Details: %s" % str(key_err))

                if self._since_cursor + self._time_frame_length * 60 < TimeFrameManager._SERVER_TIME + API_DELAY:
                    self.feed()

                time_to_sleep = self._since_cursor + self._time_frame_length * 60 - TimeFrameManager._SERVER_TIME

                if time_to_sleep < 1:
                    time_to_sleep = 2
                    logging.debug("The server is late on the data for %s with %d min interval, sleep a little to retry "
                                  "quickly" % (self._pair, self._time_frame_length))

            logging.info("Next data acquisition of %s for %d min interval in %d sec"
                         % (self._pair, self._time_frame_length, time_to_sleep))
            for i in range(time_to_sleep):
                if self._t_run:
                    time.sleep(1)
                else:
                    break
        logging.info("Ending time frame manager thread for data acquisition. Pair: %s, time frame: %d min"
                     % (self._pair, self._time_frame_length))
