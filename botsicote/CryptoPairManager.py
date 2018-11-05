import logging
from exceptions.BotsicoteException import BotsicoteException
from TimeFrameManager import TimeFrameManager


SUPPORTED_TIME_FRAME_LENGTH = [1, 5, 15, 30, 60, 240, 1440, 10080, 21600]


class CryptoPairManager(object):
    """Crypto pair manager"""

    def __init__(self, crypto, currency, krakenex_instance, call_rate_manager, lock, pair2=None):
        """
        Crypto pair manager constructor

        :param crypto: Name of the crypto to trade with
        :type crypto: str
        :param currency: Name of the currency to trade with
        :type currency: str
        :param krakenex_instance: Instance of krakenex
        :type krakenex_instance: Krakenex
        :param call_rate_manager: The kraken api call rate manager
        :param lock: The threading lock
        :type lock: threading.Lock
        :param pair2: Name of the key to retrieve data after an OHLC api call (default Xcrypto followed by Zcurrency)
        :type pair2: str
        """
        self.pair = "%s%s" % (crypto, currency)
        self.pair2 = "X%sZ%s" % (crypto, currency) if pair2 is None else pair2
        self._time_frames = {}
        self._k = krakenex_instance
        self._call_rate_manager = call_rate_manager
        self._lock = lock
        logging.info("New crypto pair manager created! Pair: %s" % self.pair)

    def add_time_frame(self, time_frame_length):
        """
        Add a new time frame

        :param time_frame_length: The length of the time frame in minute (1, 5, 15, 30, 60, 240, 1440, 10080, 21600)
        :type time_frame_length: int
        """
        if time_frame_length not in SUPPORTED_TIME_FRAME_LENGTH:
            raise BotsicoteException("Time frame length must be one of the following: %s " %
                                     ", ".join([str(item) for item in SUPPORTED_TIME_FRAME_LENGTH]))

        if time_frame_length in self._time_frames:
            logging.warning("Time frame length (%d) is already managed for pair %s" % (time_frame_length, self.pair))
            return

        self._time_frames[time_frame_length] = TimeFrameManager(time_frame_length, self.pair, self.pair2, self._k,
                                                                self._call_rate_manager, self._lock)

    def start_time_frame_acq(self, time_frame_length):
        """
        Starts the data acquisition for a given time frame

        :param time_frame_length: The given time frame
        :type time_frame_length: int
        """
        if time_frame_length not in self._time_frames:
            raise BotsicoteException("Trying to start a non existing time frame %d for pair %s"
                                     % (time_frame_length, self.pair))

        self._time_frames[time_frame_length].start()

    def start_all_time_frame_acq(self):
        """Starts the data acquisition for all time frames"""
        for key in self._time_frames.keys():
            self.start_time_frame_acq(key)

    def stop_time_frame_acq(self, time_frame_length):
        """
        Stops the data acquisition for a given time frame

        :param time_frame_length: The given time frame
        :type time_frame_length: int
        """
        if time_frame_length not in self._time_frames:
            raise BotsicoteException("Trying to stop a non existing time frame %d for pair %s"
                                     % (time_frame_length, self.pair))

        self._time_frames[time_frame_length].stop()

    def stop_all_time_frame_acq(self):
        """Stops the data acquisition for all time frames"""
        for key in self._time_frames.keys():
            self.stop_time_frame_acq(key)

    def get_time_frame(self, time_frame_length):
        """
        Return the given time frame instance
        :param time_frame_length: The given time frame
        :type time_frame_length: int
        :return: The given time frame instance
        :rtype: TimeFrameManager
        """
        if time_frame_length not in self._time_frames:
            raise BotsicoteException("Trying to access a non existing time frame %d for pair %s"
                                     % (time_frame_length, self.pair))

        return self._time_frames[time_frame_length]
