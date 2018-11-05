import pandas as pd
from StockDataManager import StockDataManager
from entities.Color import Color
from entities.Trend import Trend
from entities.CandlestickFigure import CandlestickShapeEnum
from strategies.best_strat_ever.TechnicalAnalysisResult import TechnicalAnalysisResult


class TechnicalAnalysis(object):
    """Technical analysis"""

    def __init__(self, stock_data_manager):
        """
        Technical analysis constructor

        :param stock_data_manager: Indicator manager to analyse
        :type stock_data_manager: StockDataManager
        """
        self._s_d_m = stock_data_manager
        self.result = TechnicalAnalysisResult()

    def run_analysis(self):
        """Run the analysis"""

        sma_10_series = self._s_d_m.stock_indicators["close_10_sma"]
        sma_21_series = self._s_d_m.stock_indicators["close_21_sma"]
        ema_10_series = self._s_d_m.stock_indicators["close_10_ema"]
        ema_21_series = self._s_d_m.stock_indicators["close_21_ema"]
        average_reference_series = self._s_d_m.stock_indicators["close_2_sma"]
        macdh_series = self._s_d_m.stock_indicators["macdh"]
        rsi_series = self._s_d_m.stock_indicators["rsi_14"]
        stock_data = self._s_d_m.stock_data_list

        self.result.sma_10_signal, self.result.sma_10_signal_power = \
            TechnicalAnalysis._analyse_average(sma_10_series, average_reference_series)
        self.result.sma_21_signal, self.result.sma_21_signal_power = \
            TechnicalAnalysis._analyse_average(sma_21_series, average_reference_series)
        self.result.ema_10_signal, self.result.ema_10_signal_power = \
            TechnicalAnalysis._analyse_average(ema_10_series, average_reference_series)
        self.result.ema_21_signal, self.result.ema_21_signal_power = \
            TechnicalAnalysis._analyse_average(ema_21_series, average_reference_series)
        self.result.macd_signal, self.result.macd_signal_power = \
            TechnicalAnalysis._analyse_macd(macdh_series, average_reference_series)
        self.result.rsi_signal, self.result.rsi_signal_power = TechnicalAnalysis._analyse_rsi(rsi_series, 35, 65)
        self.result.last_candlestick_figure = TechnicalAnalysis._determinate_candlestick_figure(stock_data)
        self.result.trend = TechnicalAnalysis._determinate_trend(stock_data)
        self.result.stock_price = stock_data[-1].close_price

        # TODO bollinger bands and ichimoku
        pass

    @staticmethod
    def _analyse_average(average_series, reference_series):
        """
        Compare and analyse an average series with a reference series

        :param average_series: Series to compare
        :type average_series: pd.Series
        :param reference_series: Reference series to be compared with
        :type reference_series: pd.Series
        :return: A tuple containing the signal and the signal power
        :rtype: tuple
        """
        # Positive equals buy signal, negative equals sell signal
        # The higher the percentage is, the more powerful the signal is
        difference_series = ((reference_series - average_series) / reference_series) * 100
        last_difference_list = difference_series.tolist()[-10:]

        result = 0
        for i in range(1, 10):
            if last_difference_list[i-1] < 0 < last_difference_list[i]:  # Buy signal
                result += (i + 1) ** 2
            elif last_difference_list[i] < 0 < last_difference_list[i-1]:  # Sell signal
                result -= (i + 1) ** 2
            else:  # No change of signal type
                if abs(last_difference_list[i]) < 0.2:  # If we are close enought from a potential signal change
                    if abs(last_difference_list[i-1]) - abs(last_difference_list[i]) > 0:
                        result += ((i + 1) ** 2) / 3 * (-1) if last_difference_list[i] > 0 else ((i + 1) ** 2) / 3
                    else:
                        result += 1 if last_difference_list[i] > 0 else -1
                else:
                    result += 1 if last_difference_list[i] > 0 else -1

        average_signal = 0

        if result > 100 or result < -100:
            average_power = 10
        else:
            average_power = (abs(result) * 10 / 100)

        average_signal = 1 if result > 0 else average_signal
        average_signal = -1 if result < 0 else average_signal

        return average_signal, average_power

    @staticmethod
    def _analyse_macd(macd_series, reference_series):
        """
        Analyse MACD series

        :param macd_series: The MACD series to be analysed
        :type macd_series: pd.Series
        :param reference_series: Reference series to be compared with
        :type reference_series: pd.Series
        :return: A tuple containing the signal and the signal power
        :rtype: tuple
        """

        last_macd_value_list = ((macd_series / reference_series) * 100).tolist()[-10:]

        result = 0
        for i in range(1, 10):
            if last_macd_value_list[i - 1] < 0 < last_macd_value_list[i]:  # Buy signal
                result += (i + 1) ** 2
            elif last_macd_value_list[i] < 0 < last_macd_value_list[i - 1]:  # Sell signal
                result -= (i + 1) ** 2
            else:  # No change of signal type
                if abs(last_macd_value_list[i]) < 0.1:  # If we are close enought from a potential signal change
                    if abs(last_macd_value_list[i - 1]) - abs(last_macd_value_list[i]) > 0:
                        result += ((i + 1) ** 2) / 3 * (-1) if last_macd_value_list[i] > 0 else ((i + 1) ** 2) / 3
                    else:
                        result += 1 if last_macd_value_list[i] > 0 else -1
                else:
                    result += 1 if last_macd_value_list[i] > 0 else -1

        macd_signal = 0

        if result > 100 or result < -100:
            macd_power = 10
        else:
            macd_power = (abs(result) * 10 / 100)

        macd_signal = 1 if result > 0 else macd_signal
        macd_signal = -1 if result < 0 else macd_signal

        return macd_signal, macd_power

    @staticmethod
    def _analyse_rsi(rsi_series, min_value, max_value):
        """
        Analyse rsi series

        :param rsi_series: The overbought series to be analysed
        :type rsi_series: pd.Series
        :param min_value: Min value before a market is considered oversold
        :type min_value: float
        :param max_value: Max value before a market is considered overbought
        :type max_value: float
        :return: A tuple containing the signal and the signal power
        :rtype: tuple
        """
        last_overbought_value_list = rsi_series.tolist()[-10:]

        result = 0
        for i in range(10):
            if last_overbought_value_list[i] < min_value:  # Buy signal
                result += (i + 1) ** 2
            elif last_overbought_value_list[i] > max_value:  # Sell signal
                result -= (i + 1) ** 2
            else:
                result /= 1.5

        overbought_signal = 0

        if result > 200 or result < -200:
            overbought_power = 10
        else:
            overbought_power = (abs(result) * 10 / 200)

        overbought_signal = 1 if result > 0 else overbought_signal
        overbought_signal = -1 if result < 0 else overbought_signal

        return overbought_signal, overbought_power

    @staticmethod
    def _determinate_candlestick_figure(stock_data_list):
        """
        Determinate which candlestick figure the last candlestick is

        :param stock_data_list: The stock data list
        :type stock_data_list: list[StockDataPoint]
        :return: The candlestick figure the last candlestick is
        :rtype: CandlestickShapeEnum
        """
        if stock_data_list[-1].is_hammer_or_hanging_man():
            return CandlestickShapeEnum.HAMMER_OR_HANGING_MAN
        if stock_data_list[-1].is_reversed_hammer_or_falling_star():
            return CandlestickShapeEnum.REVERSED_HAMMER_OR_FALLING_STAR
        if stock_data_list[-1].is_a_swallowing(stock_data_list[-2]):
            return CandlestickShapeEnum.SWALLOWING
        if stock_data_list[-1].is_an_harami(stock_data_list[-2]):
            return CandlestickShapeEnum.HARAMI
        return CandlestickShapeEnum.UNDEFINED

    @staticmethod
    def _determinate_trend(stock_data_list):
        """
        Determine the trend

        :param stock_data_list: The stock data list
        :type stock_data_list: list[StockDataPoint]
        :return: The trend
        ;:rtype: Trend
        """
        last_stock_data_list = stock_data_list[-10:]
        result = 0

        for i in range(10):
            coef = abs(last_stock_data_list[i].open_price - last_stock_data_list[i].close_price) / \
                   last_stock_data_list[i].close_price * 100
            result += (i + 1) * 2 * coef if last_stock_data_list[i].get_color() is Color.GREEN \
                else ((i + 1) * 2) * (-1) * coef

        if result > 20:
            return Trend.UP
        if result < -20:
            return Trend.DOWN
        return Trend.UNDEFINED
