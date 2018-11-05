import pandas as pd
import math
from entities.IchimokuPoint import IchimokuPoint


class IndicatorComputer(object):
    """Indicator computer"""

    @staticmethod
    def compute_ichimoku(data_line, data_line_cursor, window_1, window_2, window_3):
        """
        Compute ichimoku indicators

        :param data_line: Stock data line
        :type data_line: list
        :param data_line_cursor: Last processed data line entries (no need to return indicators for processed entries)
        :type data_line_cursor: int
        :param window_1: Minimum window (used for tenkan-sen)
        :type window_1: int
        :param window_2: Intermediate window (used for kijun-sen, senkou-span-a, chikou-span)
        :type window_2: int
        :param window_3: Maximum window (used for senkou-span-b)
        :type window_3: int
        :return: ichimoku_point_list
        """
        high_prices = pd.Series([data.high_price for data in data_line])
        low_prices = pd.Series([data.low_price for data in data_line])
        close_prices = pd.Series([data.close_price for data in data_line])

        # Tenkan-sen (Conversion Line): (window_1-period high + window_1-period low)/2))
        period9_high = pd.Series.rolling(high_prices, window=window_1, center=False).max()
        period9_low = pd.Series.rolling(low_prices, window=window_1, center=False).min()
        tenkan_sen = (period9_high + period9_low) / 2
        tenkan_sen_list = tenkan_sen.tolist()

        # Kijun-sen (Base Line): (window_2-period high + window_2-period low)/2))
        period26_high = pd.Series.rolling(high_prices, window=window_2, center=False).max()
        period26_low = pd.Series.rolling(low_prices, window=window_2, center=False).min()
        kijun_sen = (period26_high + period26_low) / 2
        kijun_sen_list = kijun_sen.tolist()

        # Senkou Span A (Leading Span A): (Conversion Line + Base Line)/2))
        senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(window_2)
        senkou_span_a_list = senkou_span_a.tolist()

        # Senkou Span B (Leading Span B): (window_3-period high + window_3-period low)/2))
        period52_high = pd.Series.rolling(high_prices, window=window_3, center=False).max()
        period52_low = pd.Series.rolling(low_prices, window=window_3, center=False).min()
        senkou_span_b = ((period52_high + period52_low) / 2).shift(window_2)
        senkou_span_b_list = senkou_span_b.tolist()

        # The most current closing price plotted window_2 time periods behind (optional)
        chikou_span = close_prices.shift(-window_2)
        chikou_span_list = chikou_span.tolist()

        ichimoku_point_list = []

        for i, data in enumerate(data_line):
            if data.identifier > data_line_cursor:
                i_p_tenkan_sen = tenkan_sen_list[i]
                i_p_kijun_sen = kijun_sen_list[i]
                i_p_senkou_span_a = senkou_span_a_list[i]
                i_p_senkou_span_b = senkou_span_b_list[i]
                i_p_chikou_span = chikou_span_list[i]

                if not math.isnan(i_p_tenkan_sen) \
                        and not math.isnan(i_p_kijun_sen) \
                        and not math.isnan(i_p_senkou_span_a) \
                        and not math.isnan(i_p_senkou_span_b):
                    ichimoku_point_list.append(
                        IchimokuPoint(
                            data.identifier,
                            i_p_tenkan_sen,
                            i_p_kijun_sen,
                            i_p_senkou_span_a,
                            i_p_senkou_span_b,
                            i_p_chikou_span)
                    )
        return ichimoku_point_list
