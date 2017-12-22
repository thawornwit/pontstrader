#!/usr/bin/env python

def menu(apikey, apisecret, pushover_user, pushover_app, pushbullet_token, redis_password):

  import sys
  import time
  import threading
  import os
  from buy import buy
  from sell import sell
  from buysell import buysell
  from balances import balances
  from orderbook import orderbook
  from watch import watch
  from withdraw import withdraw
  from deposit import deposit
  from arbitrage import arbitrage
  from trailing import trailing
  from takeprofit import takeprofit
  from stoplosstakeprofit import stoplosstakeprofit
  from trailingtakeprofit import trailingtakeprofit
  from colors import white, red, green, yellow
  from colorama import Fore, Back, Style, init
  init()

  while True:
    white((30 * '-'))
    green('P O N T S T R A D E R . C O M')
    white((30 * '-'))
    yellow('1. Buy')
    yellow('2. Sell')
    yellow('3. Buy and Sell')
    yellow('4. Balances')
    yellow('5. Orderbook')
    yellow('6. Watch coin')
    yellow('7. Withdraw')
    yellow('8. Deposit')
    yellow('9. Arbitrage')
    yellow('10. Trailing Stop Loss (24/7)')
    yellow('11. Take Profit (BETA + 24/7)')
    yellow('12. Stop Loss + Take Profit (BETA + 24/7)')
    yellow('13. Trailing + Take Profit (BETA + 24/7)')
    red('14. Exit')
    white((30 * '-'))

    try:
      choice = raw_input(Fore.WHITE +'Enter your choice [1-14] : ')
      choice = int(choice)
    except:
      red('Invalid number. Try again...')

    # BUY
    if choice == 1:
      buy(apikey, apisecret, redis_password)

    # SELL
    elif choice == 2:
      sell(apikey, apisecret, redis_password)

    # BUY AND SELL
    elif choice == 3:
      buysell(apikey, apisecret, redis_password)

    # SHOW WALLETS
    elif choice == 4:
      balances(apikey, apisecret, redis_password)

    # OPEN ORDERS
    elif choice == 5:
      orderbook(apikey, apisecret, redis_password)

    # WATCH
    elif choice == 6:
      watch(apikey, apisecret, redis_password)

    # WITHDRAW
    elif choice == 7:
      withdraw(apikey, apisecret)

    # DEPOSIT
    elif choice == 8:
      deposit(apikey, apisecret)

    # ARBITRAGE
    elif choice == 9:
      arbitrage(redis_password)

    # TRAILING
    elif choice == 10:
      trailing(apikey, apisecret, pushover_user, pushover_app, pushbullet_token, redis_password)

    # TAKE PROFIT
    elif choice == 11:
      takeprofit(apikey, apisecret, pushover_user, pushover_app, pushbullet_token, redis_password)

    # STOP LOSS TAKE PROFIT
    elif choice == 12:
      stoplosstakeprofit(apikey, apisecret, pushover_user, pushover_app, pushbullet_token, redis_password)

    # TRAILING TAKE PROFIT
    elif choice == 13:
      trailingtakeprofit(apikey, apisecret, pushover_user, pushover_app, pushbullet_token, redis_password)

    # EXIT
    elif choice == 14:
      count = threading.activeCount()
      if count > 1:
        threads = threading.enumerate()
        thread_counter = 0
        for t in threading.enumerate():
          if 'arbitrage' in t.name:
            pass
          elif 'Main' in t.name:
            pass
          else:
            thread_counter += 1
        if thread_counter > 0:
          yellow('WARNING: There are currently {0} active trade(s), are you sure you want to exit?'.format(thread_counter))
          green('1. yes')
          red('2. no')
          try:
            yes_no = raw_input(Fore.WHITE+'Enter your choice [1-2] : ')
            yes_no = int(yes_no)
          except:
            white('Invalid number... going back to Main Menu')
          if yes_no == 1:
            white('Exiting...')
            sys.exit()
          elif yes_no == 2:
            white('Good... going back to Main Menu')
          else:
            white('Invalid number... going back to Main Menu')
        else:
          white('Exiting...')
          sys.exit()
      else:
        white('Exiting...')
        sys.exit()

    # ELSE EXIT
    else:
      white('Invalid number. Try again...')
