  #!/usr/bin/env python
  
def balances(key, secret, redis_password):
  
  import time, json, sys, os, redis
  from pprint import pprint
  from time import gmtime, strftime
  from bittrex import bittrex
  from colors import white, red, green, yellow
  from colorama import Fore, Back, Style, init

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
    except:
      white('Bittrex API error: {0}'.format(api))
  
    white((30 * '-'))
    green('   B A L A N C E S')
    white((30 * '-'))
    try:
      get_balances = api.getbalances()
      green('Currency\tBalance\t\t\tAvailable\t\tPending\t\tBTC Value')
      total_btc = 0
      usdt = 0
      for coin in get_balances:
        balance = coin["Balance"]
        if (balance != 0.0 and not None):
          available = coin["Available"]
          currency = coin["Currency"]
          pending = coin["Pending"]
          if currency == 'BTC':
            white('{0}\t\t{1:.8f}\t\t{2:.8f}\t\t{3:.8f}\t{4:.8f}'.format(currency, balance, available, pending, balance))
            last = balance
            total_btc += last
          elif currency == 'USDT':
            white('{0}\t\t{1:.8f}\t\t{2:.8f}\t\t{3:.8f}'.format(currency, balance, available, pending))
            usdt = float(balance)
            last = '0'
          else:
            try:
              market = 'BTC-{0}'.format(currency)
              summary = api.getmarketsummary(market)
              values = r.hmget(market, 'Ask')
              last = float(values[0]) * float(balance)
              total_btc += last
              white('{0}\t\t{1:.8f}\t\t{2:.8f}\t\t{3:.8f}\t{4:.8f}'.format(currency, balance, available, pending, last))
            except:
              white('{0}\t\t{1:.8f}\t\t{2:.8f}\t\t{3:.8f}'.format(currency, balance, available, pending))
      market = 'USDT-BTC'
      summary = api.getmarketsummary(market)
      total_usd = float(summary[0]['Last']) * float(total_btc) + float(usdt)
      yellow('Estimated Value: {0:.8f} BTC / {1:.8f} USD'.format(total_btc, total_usd))
      output = (Fore.YELLOW +'Refresh: r+enter | Return to Main Menu: q+enter : ')
      refresh = raw_input(output)
      refresh = str(refresh)
      if refresh == 'r':
        green('Ok, refreshing in 5 seconds... (to prevent spam)')
        time.sleep(5)
      elif refresh == 'q':
        break
      else:
        white('Invalid input, refreshing in 5 seconds... (to prevent spam)')
        time.sleep(5)
    except:
      white('Bittrex API error')
      white('Going back to Main Menu')
      time.sleep(2)
      break
