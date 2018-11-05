from entities.IdentifiedPoint import IdentifiedPoint


class IchimokuPoint(IdentifiedPoint):
    """Ichimoku point"""

    def __init__(self, identifier, tenkan_sen, kijun_sen, senkou_span_a, senkou_span_b, chikou_span):
        """
        Ichimoku point constructor

        :param identifier: Time of the Ichimoku point (in timestamp)
        :type identifier: int
        :param tenkan_sen: Ichimoku tenkan sen value
        :type tenkan_sen: float
        :param kijun_sen: Ichimoku kijun sen value
        :type kijun_sen: float
        :param senkou_span_a: Ichimoku senkou span a value
        :type senkou_span_a: float
        :param senkou_span_b: Ichimoku senkou span b value
        :type senkou_span_b: float
        :param chikou_span: Ichimoku chikou span value
        :type chikou_span: float
        """
        super(IchimokuPoint, self).__init__(identifier)
        self.tenkan_sen = tenkan_sen
        self.kijun_sen = kijun_sen
        self.senkou_span_a = senkou_span_a
        self.senkou_span_b = senkou_span_b
        self.chikou_span = chikou_span

    def __str__(self):
        return "{identifier: %d, tenkan_sen: %f, kijun_sen: %f, senkou_span_a: %f, senkou_span_b: %f, chikou_span: %f}"\
               % (self.identifier, self.tenkan_sen, self.kijun_sen, self.senkou_span_a, self.senkou_span_b,
                  self.chikou_span)
