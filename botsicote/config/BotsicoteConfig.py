from tools.ConfigFile import ConfigFile
from strategies.best_strat_ever.BestStratEver import BestStratEver


class BotsicoteConfig(ConfigFile):

    _BOTSICOTE_CONFIG = {
        "LOG_LEVEL": "DEBUG",  # DEBUG, INFO, WARNING, ERROR, CRITICAL
        "BOTSICOTE": {
            "PATH": "~/PycharmProjects/Botsicote/botsicote",
            "LOG_DIRECTORY": "logs",
            "APP_NAME": "Botsicote",
            "VERSION": "1.0"
        },
        "KRAKEN": {
            "TIER_LEVEL": 2
        },
        "MANAGED_CRYPTO": [
            {"NAME": "XBT", "CURRENCY": "EUR", "PAIR_NAME": None},
            {"NAME": "XRP", "CURRENCY": "EUR", "PAIR_NAME": None},
            {"NAME": "BCH", "CURRENCY": "EUR", "PAIR_NAME": "BCHEUR"},
            {"NAME": "ETC", "CURRENCY": "EUR", "PAIR_NAME": None},
            {"NAME": "ETH", "CURRENCY": "EUR", "PAIR_NAME": None},
            {"NAME": "LTC", "CURRENCY": "EUR", "PAIR_NAME": None},
            {"NAME": "DASH", "CURRENCY": "EUR", "PAIR_NAME": "DASHEUR"},
            {"NAME": "XMR", "CURRENCY": "EUR", "PAIR_NAME": None}
        ],
        "STRATEGY": BestStratEver()
    }

    def __init__(self):
        super(BotsicoteConfig, self).__init__(BotsicoteConfig._BOTSICOTE_CONFIG)
