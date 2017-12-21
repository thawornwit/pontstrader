#!/usr/bin/env python
  
def sell(key, secret, redis_password):
  
  import time, json, sys, redis
  from pprint import pprint
  from time import gmtime, strftime
  from bittrex import bittrex
  from colors import white, red, green, yellow
  from colorama import Fore, Back, Style, init
  init()

  try:
    r = redis.Redis(host='redis.pontstrader.com', port=6380, db=0, password=redis_password)
  except:
    white('Unable to connect to redis.pontstrader.com, trying redis2.pontstrader.com...')
    try:
      r = redis.Redis(host='redis2.pontstrader.com', port=6380, db=0, password=redis_password)
    except:
      white('Unable to connect to redis2.pontstrader.com... I am sorry but you can not continue now, please contact p0nts!')
  
  while True:
    try:
      api = bittrex(key, secret)
      currencies = api.getcurrencies()
      markets = api.getmarkets()
    except:
      white('Bittrex API error: {0}'.format(api))
      white('Going back to Main Menu')
      time.sleep(1)
      break
  
    white((30 * '-'))
    green('   S E L L  O R D E R')
    white((30 * '-'))
    try:
      balances = api.getbalances()
      green('Currency\tAvailable')
      number = 0
      list = []
      for coin in balances:
        available = coin["Available"]
        currency = coin["Currency"]
        if available != 0.0 and not None:
          number += 1
          list.append(currency)
          if len(currency) < 5:
            white('{0}. {1}\t\t{2:.8f}'.format(number, currency, available))
          else:
            white('{0}. {1}\t{2:.8f}'.format(number, currency, available))
    except:
      white('Bittrex API error: {0}'.format(balances))
      white('Going back to Main Menu')
      time.sleep(2)
      break
    try:
      choose_num = raw_input(Fore.WHITE+'Enter your choice [1-{0}] (q+enter to return to Main Menu) : '.format(number))
      choose_num = int(choose_num)
    except:
      white('Going back to Main Menu')
      time.sleep(1)
      break
    try:
      choose_num = choose_num - 1
      if choose_num == -1:
        white('Invalid number... going back to Main Menu')
        time.sleep(1)
        break
      green('Starting sell for {0}'.format(list[choose_num]))
      white((30 * '-'))
      white('Market?')
      yellow('1. BTC')
      yellow('2. ETH')
      yellow('3. USDT')
    except:
      white('\nInvalid number... going back to Main Menu')
      time.sleep(1)
      break
    try:
      trade = raw_input(Fore.WHITE+'Enter your choice [1-3] : ')
      trade = int(trade)
    except:
      white('\nInvalid number... going back to Main Menu')
      time.sleep(1)
      break
    if trade == 1:
      trade = 'BTC'
    elif trade == 2:
      trade = 'ETH'
    elif trade == 3:
      trade = 'USDT'
    else:
      white('\nInvalid number... going back to Main Menu')
      time.sleep(1)
      break
    try:
      currency = list[choose_num]
      market = '{0}-{1}'.format(trade, currency)
    except:
      print available
      white('\nGoing back to Main Menu')
      time.sleep(1)
      break
    try:
      values = r.hmget(market, 'Last', 'Bid', 'Ask')
      balance = api.getbalance(currency)
      last = float(values[0])
      bid = float(values[1])
      ask = float(values[2])
      white((30 * '-'))
      white('- Available:\t {0:.8f} {1}'.format(balance['Available'], currency))
      white('- Price (Last):  {0:.8f} {1}'.format(last, trade))
      white('- Price (Bid):\t {0:.8f} {1}'.format(bid, trade))
      white('- Price (Ask):\t {0:.8f} {1}'.format(ask, trade))
    except:
      white('Unable to retrieve data from redis.pontstrader.com')
      white('Going back to Main Menu')
      time.sleep(2)
      break
    for f in currencies:
      if f['Currency'] == currency:
        fee = f['TxFee']
        white('- Fee:\t\t {0:.8f} {1}'.format(fee, currency))
    for m in markets:
      if m['MarketCurrency'] == currency and m['BaseCurrency'] == trade:
        minimum = m['MinTradeSize']
        white('- Minimum ({0}): {1:.8f}'.format(currency, minimum))
    enough = balance['Available'] - fee
    if enough < 0.00000001:
      red('You dont have enough {0} ({1:.8f}) to sell anything!'.format(currency, enough))
      time.sleep(1)
      break
    else:
      green('You have {0:.8f} {1}'.format(balance['Available'], currency))
      white((30 * '-'))
      white('Sellprice?')
      yellow('1. Last ({0:.8f} {1})'.format(last, trade))
      yellow('2. Bid ({0:.8f} {1})'.format(bid, trade))
      yellow('3. Ask ({0:.8f} {1})'.format(ask, trade))
      yellow('4. Custom')
      red('5. Back to Main Menu') 
      try:
        sellprice = raw_input(Fore.WHITE+'Enter your choice [1-5] : ')
        sellprice = int(sellprice)
      except:
        white('\nInvalid number... going back to Main Menu')
        time.sleep(1)
        break
      if sellprice == 1:
        sell_for = last
        white('Selected \'Last\': {0:.8f} {1}'.format(last, trade))
      elif sellprice == 2:
        sell_for = bid
        white('Selected \'Bid\': {0:.8f} {1}'.format(bid, trade))
      elif sellprice == 3:
        sell_for = ask
        white('Selected \'Ask\': {0:.8f} {1}'.format(ask, trade))
      elif sellprice == 4:
        try:
          sell_for = raw_input(Fore.WHITE+'Sellprice? e.g. [0.00000001] : ')
          sell_for = float(sell_for)
          white('Selected \'Custom\': {0:.8f} {1}'.format(sell_for, trade))
        except:
          white('Please provide a proper sellprice! (e.g. {0:.8f})'.format(last))
          white('Going back to Main Menu')
          time.sleep(1)
          break
      elif sellprice == 5:
        break
      else:
        white('\nInvalid number... going back to Main Menu')
        time.sleep(1)
        break
    try:
      amount = raw_input(Fore.WHITE+'Amount? : ')
      amount = float(amount)
    except:
      white('\nInvalid number... going back to Main Menu')
      time.sleep(1)
      break
    white((30 * '-'))
    white('Selling {0:.8f} {1} for {2:.8f} {3} each, Proceed?'.format(amount, currency, sell_for, trade))
    green('1. yes')
    red('2. no (Back to Main Menu)')
    try:
      yes_no = raw_input(Fore.WHITE+'Enter your choice [1-2] : ')
      yes_no = int(yes_no)
    except:
      white('\nInvalid number... going back to Main Menu')
      time.sleep(1)
      break
    if yes_no == 1:
      try:
        apicall = api.selllimit(market, amount, sell_for)
        sell_uuid = apicall['uuid']
        time.sleep(0.5)
        sellorder = api.getorder(uuid=sell_uuid)
        total = amount * sell_for
        green('Added a sell order for {0:.8f} {1} at {2:.8f} {3} each which is {4:.8f} {3} total'.format(amount, currency, sell_for, trade, total))
        white('Checking status in 2 seconds')
        time.sleep(2)
        if sellorder['IsOpen'] == False:
          white('Great! Order is completely filled')
        else:
          white('Order is not filled yet, would you like to wait up to 120 seconds?'.format(amount, sell_for, trade))
          green('1. yes')
          red('2. no (Back to Main Menu)')
          try:
            yes_no = raw_input(Fore.WHITE+'Enter your choice [1-2] : ')
            yes_no = int(yes_no)
          except:
            white('\nInvalid number... going back to Main Menu')
            time.sleep(1)
            break
          if yes_no == 1:
            yellow('Script will automatically return to Main Menu after 120 seconds')
            time_decrease = 120
            if sellorder['IsOpen'] == True:
              while sellorder['IsOpen'] == True:
                if time_decrease <= 0:
                  break
                yellow('Waiting until the sell order is completely filled! Remaining: {0:.8f} ({1} seconds remaining)'.format(sellorder['QuantityRemaining'], time_decrease))
                sellorder = api.getorder(uuid=sell_uuid)
                time.sleep(10)
                time_decrease -= 10
            white('Great! Order is completely filled')
          elif yes_no == 2:
            white('\nOk... going back to Main Menu')
            time.sleep(1)
            break
          else:
            white('\nInvalid number... going back to Main Menu')
            time.sleep(1)
            break
        white('Returning to Main Menu in 2 seconds...')
        time.sleep(2)
        break
      except:
        white('Bittrex API error: {0}'.format(apicall))
        white('Going back to Main Menu')
        time.sleep(2)
        break
    elif yes_no == 2:
      white('\nGoing back to Main Menu')
      time.sleep(1)
      break
    else:
      white('\nInvalid number... going back to Main Menu')
      time.sleep(1)
      break
