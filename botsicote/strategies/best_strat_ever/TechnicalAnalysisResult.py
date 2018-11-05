class TechnicalAnalysisResult(object):
    """Technical analysis result"""

    def __init__(self):
        # Negative signal value means sell signal, positive value means buy signal. Value goes from -10 to 10
        self.sma_10_signal = 0
        self.sma_10_signal_power = 0
        self.sma_21_signal = 0
        self.sma_21_signal_power = 0
        self.ema_10_signal = 0
        self.ema_10_signal_power = 0
        self.ema_21_signal = 0
        self.ema_21_signal_power = 0
        self.macd_signal = 0
        self.macd_signal_power = 0
        self.rsi_signal = 0
        self.rsi_signal_power = 0
        self.stock_price = 0
        self.last_candlestick_figure = None
        self.trend = None
