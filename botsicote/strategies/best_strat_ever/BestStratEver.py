import copy
import logging
import time

from Strategy import Strategy
from strategies.best_strat_ever.Signal import Signal
from strategies.best_strat_ever.TechnicalAnalysis import TechnicalAnalysis
from strategies.best_strat_ever.TechnicalAnalysisResult import TechnicalAnalysisResult

MAX_TA_TO_STORE = 5

"""
Time frame list stores the time frames that the strategy will set up.
The order is important, indeed the first time frame will be the reference one.
The other time frames will be used to confirm or invalidate a tendency
and to add accuracy in the choice of following or not a given signal.
"""
TIME_FRAME_LIST = [15, 5, 1]


class BestStratEver(Strategy):
    """The best strategy ever"""

    def __init__(self):
        """The best strategy ever constructor"""

        super(BestStratEver, self).__init__()

        """
        The crypto pair manager list.
        It contains the crypto pair manager for each tracked crypto pair
        """
        self.crypto_pair_manager_list = None

        """
        Last processed update datetime dict for each crypto pair. 
        Each dict entry contains an array of last update datetime for tracked time frames
        """
        self.last_processed_update_dt_dict = {}

        """
        Technical analysis dict for each crypto pair. 
        Each dict entry contains an array of technical analysis for tracked time frames
        """
        self.technical_analysis_dict = {}

        """
        Will store the last (MAX_TA_TO_STORE) technical analysis computed for each crypto pair. 
        Each dict entry contains a dict of tracked time frames.
        Each tracked time frames contains an array of last technical analysis result
        """
        self.last_technical_analysis_result = {}

        """
        Signal dict for each crypto pair
        Each dict entry contains a signal
        """
        self.signal_dict = {}

        """Kraken API agent"""
        self.k = None

        """Kraken API call rate manager"""
        self.call_rate_manager = None

    def startup(self):
        """Strategy initialisation"""

        logging.info("BestStratEver startup")

        self.crypto_pair_manager_list = self.get_crypto_pair_manager_list()
        self.k = self.get_kraken_api_instance()
        self.call_rate_manager = self.get_call_rate_manager()

        for cpm in self.crypto_pair_manager_list:
            self.last_processed_update_dt_dict[cpm.pair] = {}
            self.technical_analysis_dict[cpm.pair] = {}
            self.last_technical_analysis_result[cpm.pair] = {}

            for tf in TIME_FRAME_LIST:
                self.last_processed_update_dt_dict[cpm.pair][tf] = None
                self.technical_analysis_dict[cpm.pair][tf] = None
                self.last_technical_analysis_result[cpm.pair][tf] = []
                cpm.add_time_frame(tf)

            self.signal_dict[cpm.pair] = Signal()
            cpm.start_all_time_frame_acq()

    def run_strategy(self):
        """The strategy core"""

        logging.info("BestStratEver run_strategy")

        # Initialise technical analysis
        for cpm in self.crypto_pair_manager_list:
            for tf in TIME_FRAME_LIST:
                self.technical_analysis_dict[cpm.pair][tf] = \
                    TechnicalAnalysis(cpm.get_time_frame(tf).stock_data_manager)

        while True:
            with self.get_lock():
                for cpm in self.crypto_pair_manager_list:
                    for tf in TIME_FRAME_LIST:
                        self._update_technical_analysis(cpm.pair, tf, cpm.get_time_frame(tf).last_update_datetime)

            # compare crypto technical analysis
            for cpm in self.crypto_pair_manager_list:
                self._update_signal_dict(cpm.pair)

            with self.get_lock():
                # self.call_rate_manager.increase_api_call_rate(1)

                # pairs = ",".join([cpm.pair for cpm in self.crypto_pair_manager_list])
                # response = self.k.query_private("Ticker", data={"pair": pairs})
                # response = self.k.query_private("TradesHistory")
                # response = self.k.query_private("Balance")
                # response = self.k.query_private("OpenOrders")
                # response = self.k.query_private("ClosedOrders")

                pass

            time.sleep(10)

    def cleanup(self):
        """Clean strategy execution"""

        logging.info("BestStratEver cleanup")
        for cpm in self.get_crypto_pair_manager_list():
            cpm.stop_all_time_frame_acq()

    def _update_technical_analysis(self, pair, time_frame, last_update_datetime):
        """
        Update technical analysis if needed

        :param pair: Pair to update the technical analysis
        :type pair: str
        :param time_frame: Time frame to update the technical analysis
        :type time_frame: int
        :param last_update_datetime: Last update datetime of the technical analysis for pair and time frame
        :type last_update_datetime: datetime
        """
        if self.last_processed_update_dt_dict[pair][time_frame] != last_update_datetime:
            # Run the analysis
            self.technical_analysis_dict[pair][time_frame].run_analysis()

            # Update the last update datetime for the given pair / time frame
            self.last_processed_update_dt_dict[pair][time_frame] = copy.deepcopy(last_update_datetime)

            # Store the technical analysis result in the last_technical_analysis_result for the given pair / time frame
            technical_analysis_result = copy.deepcopy(self.technical_analysis_dict[pair][time_frame].result)
            self.last_technical_analysis_result[pair][time_frame].append(technical_analysis_result)

            # Keep only the last MAX_TA_TO_STORE technical analysis for the given pair / time frame
            self.last_technical_analysis_result[pair][time_frame] = \
                self.last_technical_analysis_result[pair][time_frame][-MAX_TA_TO_STORE:]

    def _update_signal_dict(self, pair):
        """
        compute and store the signal for the given pair

        :param pair: Pair to compute the signal
        :type pair: str
        """
        first_tf = True

        for tf in TIME_FRAME_LIST:
            for tar in self.last_technical_analysis_result[pair][tf]:
                if isinstance(tar, TechnicalAnalysisResult):  # Only for auto completion
                    continue
                    # TODO determine signal

            first_tf = False
