from strategies.best_strat_ever.SignalTypeEnum import SignalTypeEnum


class Signal(object):
    """Signal"""

    def __init__(self, signal_type=SignalTypeEnum.DO_NOTHING, signal_power=0):
        """
        Signal constructor

        :param signal_type: Type of the signal
        :type signal_type: SignalType
        :param signal_power: The power of the signal between 0 and 10
        :type signal_power: int
        """
        self.signal_type = signal_type
        self.signal_power = signal_power
