import os
import logging
import threading
import krakenex
from config.BotsicoteConfig import BotsicoteConfig
from tools.LoggingConfig import init_logger
from CryptoPairManager import CryptoPairManager
from KrakenAPICallRateManager import KrakenAPICallRateManager


if __name__ == '__main__':

    # ------------ #
    # LOGGER SETUP
    # ------------ #
    conf = BotsicoteConfig()
    log_level = conf.get("LOG_LEVEL")
    log_location = os.path.join(conf.get("BOTSICOTE.PATH"), conf.get("BOTSICOTE.LOG_DIRECTORY"))
    app_name = conf.get("BOTSICOTE.APP_NAME")
    app_version = conf.get("BOTSICOTE.VERSION")

    init_logger(log_level, log_location, app_name)

    logging.info("---------------")
    logging.info("%s V%s" % (app_name, app_version))
    logging.info("---------------")

    # ------------ #
    # API SETUP
    # ------------ #
    k = krakenex.API()
    k.load_key("kraken.key")
    call_rate_manager = KrakenAPICallRateManager(conf.get("KRAKEN.TIER_LEVEL"))

    lock = threading.Lock()

    # ---------------------------- #
    # CREATING CRYPTO PAIR MANAGER
    # ---------------------------- #
    crypto_pair_manager_list = []

    for crypto in conf.get("MANAGED_CRYPTO"):
        cpm = CryptoPairManager(crypto["NAME"], crypto["CURRENCY"], k, call_rate_manager, lock, crypto["PAIR_NAME"])
        crypto_pair_manager_list.append(cpm)

    # ------------------ #
    # LAUNCHING STRATEGY
    # ------------------ #
    try:
        strategy = conf.get("STRATEGY")
        strategy.set_crypto_pair_manager_list(crypto_pair_manager_list)
        strategy.set_lock(lock)
        strategy.set_kraken_api_instance(k)
        strategy.set_call_rate_manager(call_rate_manager)
        call_rate_manager.start()
        strategy.run()
    except KeyboardInterrupt:
        logging.info("/!\ Keyboard interruption: Stopping %s V%s" % (app_name, app_version))
    finally:
        call_rate_manager.stop()
