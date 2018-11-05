# Botsicote

The bot that execute trading strategies with kraken api

## Instalation

`pip install requirement.txt`

Add your kraken key in the `kraken.key` file.

Edit the crypto pairs you want to trade and other config info such as your kraken tier level and the strategy you want to execute in the `config/BotsicoteConfig.py` file. 

## Trading

Create your strategy in the strategy folder or reuse the existing (BestStratEver) one. The BestStratEver only do computing tasks with technical indicators to try determining sell or buy signals.

You can use krakenex examples to send trading orders. See [krakenex official documentation](`https://github.com/veox/python3-krakenex`)


I'm not responsible for any money losses using this bot. I guarantee that it will not do anything else that what you ask him to do in your strategy.

## Run the bot

Run `botsicote/botsicote.py` and try to make it a good trading partner

Enjoy !
