#!/usr/bin/env python
    
def takeprofit(key, secret, pushover_user, pushover_app, pushbullet_token, redis_password):

  import sys, os, json, time, threading, requests, redis
  from datetime import datetime
  from bittrex import bittrex
  from pushover import send_pushover
  from pushbullet import send_pushbullet
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

  global messages

  try:
    messages
  except NameError:
    messages = {}
  else:
    pass
  
  white((25 * '-'))
  green('   T A K E  P R O F I T')
  white((25 * '-'))
  while True:
    status_update = False
    gobuy = False
    try:
      threads = threading.enumerate()
      thread_counter = 0
      for t in threading.enumerate():
        if t.name.startswith('tp-'):
          thread_counter += 1
      if thread_counter > 0:
        yellow('There are currently {0} active tp trade(s):'.format(thread_counter))
      else:
        yellow('There are currently no active tp trades')
      white('Would you like to make another tp trade or check the status/history of your tp trades?')
      green('1. New trade')
      yellow('2. Status / History')
      red('3. Back to Main Menu')
      try:
        yes_no = raw_input(Fore.WHITE+'Enter your choice [1-3] : ')
        yes_no = int(yes_no)
        white((40 * '-'))
      except:
        white('\nInvalid number... going back to Main Menu')
        time.sleep(1)
        break
      if yes_no == 1:
        pass
      elif yes_no == 2:
        while True:
          try:
            trades = 0
            for k, v in messages.iteritems():
              trades += 1
              if v.startswith('tp-'):
                print v
            if trades == 0:
              red('There is currently no tp trade status/history available!')
              white((40 * '-'))
            white('Refresh, new trade or back to Main Menu?')
            green('1. Refresh')
            yellow('2. New Trade')
            red('3. Back to Main Menu')
            go_break = False
            try:
              yes_no = raw_input(Fore.WHITE+'Enter your choice [1-3] : ')
              yes_no = int(yes_no)  
              white((40 * '-'))
            except:
              go_break = True
              white('\nInvalid number... going back to Main Menu')
              time.sleep(1)
              break
            if yes_no == 1:
              pass
            elif yes_no == 2:
              break
            elif yes_no == 3:
              white('\nOk... going back to Main Menu')
              time.sleep(1)
              break
            else:
              go_break = True
              white('\nInvalid number... going back to Main Menu')
              time.sleep(1)
              break
          except:
            red('\nUnable to retrieve active threads data... going back to Main Menu')
            break
        if yes_no == 3 or go_break == True:
          break
      elif yes_no == 3:
        white('\nOk... going back to Main Menu')
        time.sleep(1)
        break
      else:
        white('\nInvalid number... going back to Main Menu')
        time.sleep(1)
        break
    except:
      red('\nUnable to retrieve active threads... there is something wrong please contact p0nts!')
      break
   
    try:
      market = raw_input(Fore.WHITE+'Market? (e.g. BTC-NEO / ETH-LTC / USDT-OMG) : ')
      market = str(market.upper())
      trade = market.split('-')[0]
      currency = market.split('-')[1]
      check_status = r.exists(market)
      if check_status != True:
        white('Unsupported market... going back to Main Menu')
        time.sleep(1)
        break
    except:
      white('\nInvalid input... going back to Main Menu')
      time.sleep(1)
      break

    if market.startswith('BTC'):
      trade = 'BTC'
    elif market.startswith('ETH'):
      trade = 'ETH'
    elif market.startswith('USDT'):
      trade = 'USDT'
    else:
      white('Unsupported market... going back to Main Menu')
      time.sleep(1)
      break
  
    try:
      value = raw_input(Fore.WHITE+'How much {0}? (excl. fee) : '.format(trade))
      value = float(value)
    except:
      white('\nInvalid number... going back to Main Menu')
      time.sleep(1)
      break
    else:
      try:
        api = bittrex(key, secret)
        available = api.getbalance(trade)
      except:
        red('Unable to retrieve balance information from Bittrex... going back to Main Menu')
        time.sleep(1)
        break
      else:
        if float(value) > float(available['Available']):
          red('You have less {0} balance available than you want to trade with... going back to Main Menu'.format(trade))
          time.sleep(1)
          break

    oneortwotargets = False
    if value < 0.00100000:
      print red('The minimum trade size on Bittrex is 100k sat')
      time.sleep(1)
      break
#    elif value >= 0.00200000:
#      print green('You are trading more than or equal to 200k satoshi, which means you are eligible to use multiple sell targets due to Bittrex new policy of 100k satoshi minimum per trade.')
#      print green(' - One sell target = sell 100% at .. satoshi')
#      print green(' - Two sell targets = sell 50% at .. satoshi, and the other 50% at x satoshi')
#      print white((40 * '-'))
#      print yellow('Would you like to use 2 sell targets or just one?')
#      print green('1. yes, two')
#      print yellow('2. no, just one')
#      print red('3. Return to Main Menu')
#      try:
#        oneortwo = raw_input(Fore.WHITE+'Enter your choice [1-3] : ')
#        oneortwo = int(oneortwo)
#      except:
#        white('\nCancelled... going back to Main Menu')
#        time.sleep(1)
#        break
#      if oneortwo == 1:
#        oneortwotargets = True
#      elif oneortwo == 2:
#        pass
#      elif oneortwo == 3:
#        white('Ok... going back to Main Menu')
#        time.sleep(1)
#        break
#      else:
#        white('\nInvalid number... going back to Main Menu')
#        time.sleep(1)
#        break
    else:
      yellow('You are trading with less than 200k satoshi, which means you are not eligible to use multiple sell targets due to Bittrex new policy of 100k satoshi per trade minimum, so we will stick with one.')

    try:
      values = r.hmget(market, 'Ask', 'MarketName', 'BaseVolume', 'Volume', 'OpenBuyOrders', 'OpenSellOrders', 'High', 'Low', 'Last', 'Bid')
    except:
      white('API error: Unable to retrieve pricing information for redis.pontstrader.com... going back to Main Menu')
      time.sleep(1)
      break

    white((40 * '-'))
    green('   M A R K E T  I N F O R M A T I O N')
    white((40 * '-'))
    yellow('- Market:           {0}'.format(market))
    yellow('- Volume:           {0:.8f}'.format(float(values[2])))
    yellow('- 24H volume:       {0:.8f}'.format(float(values[3])))
    yellow('- Open buy orders:  {0}'.format(values[4]))
    yellow('- Open sell orders: {0}'.format(values[5]))
    yellow('- 24H high:         {0:.8f}'.format(float(values[6])))
    yellow('- 24H low:          {0:.8f}'.format(float(values[7])))
    yellow('- Last:             {0:.8f}'.format(float(values[8])))
    yellow('- Ask:              {0:.8f}'.format(float(values[0])))
    yellow('- Bid:              {0:.8f}'.format(float(values[9])))
    white((40 * '-'))

    if oneortwotargets == True:
      pass
#      try:
#        target1 = raw_input(Fore.WHITE+'Target 1? 50% of the trade value will be sold here [eg. 0.00436] : ')
#        target1 = float(target1)
#      except:
#        white('\nInvalid number... going back to Main Menu')
#        time.sleep(1)
#        break
#
#      try:
#        target2 = raw_input(Fore.WHIT+'Target 2? 50% of the trade value will be sold here [eg. 0.00436] : ')
#        target2 = float(target2)
#      except:
#        white('\nInvalid number... going back to Main Menu')
#        time.sleep(1)
#        break
#      white((40 * '-'))
#      green('   B U Y  I N F O R M A T I O N')
#      yellow('- Buyprice:               {0:.8f}'.format(float(values[0])))
#      yellow('- Target 1:               {0:.8f}'.format(float(target1)))
#      yellow('- Target 2:               {0:.8f}'.format(float(target2)))
#      yellow('Because the price could have changed during your input, the buyprice may differ a little from the above prices!')
    else:
      try:
        target = raw_input(Fore.WHITE+'Target? 100% of the trade value will be sold here [eg. 0.00436] : ')
        target = float(target)
      except:
        white('\nInvalid number... going back to Main Menu')
        time.sleep(1)
        break
      white((40 * '-'))
      green('   B U Y  I N F O R M A T I O N')
      yellow('- Buyprice:               {0:.8f}'.format(float(values[0])))
      yellow('- Target:                 {0:.8f}'.format(float(target)))
      white((40 * '-'))
      yellow('Because the price could have changed during your input, the buyprice may differ a little from the above prices!')
    
    white((40 * '-'))
    white('Proceed?')
    green('1. yes')
    red('2. no, return to Main Menu')
    try:
      proceed = raw_input(Fore.WHITE+'Enter your choice [1-2] : ')
      proceed = int(proceed)
    except:
      white('\nCancelled... going back to Main Menu')
      time.sleep(1)
      break
    if proceed == 1:
      try:
        values = r.hmget(market, 'Ask')
        ask = float(values[0])
        amount = float(value) / float(ask)
        orderbook = api.getorderbook(market, type='sell')
        orderbook_rate = orderbook[0]['Rate']
        orderbook_quantity = orderbook[0]['Quantity']
        if float(amount) < float(orderbook_quantity):
          gobuy = True
          break
        else:
          while float(amount) > float(orderbook_quantity):
            time.sleep(1)
            orderbook = api.getorderbook(market, type='sell')
            orderbook_rate = orderbook[0]['Rate']
            orderbook_quantity = orderbook[0]['Quantity']
            values = r.hmget(market, 'Ask')
            ask = float(values[0])
            amount = float(value) / float(ask)
            yellow('Waiting for the volume to rise on lowest Ask to buy all for the same price.')
          gobuy = True
          break
      except:
        white('API error: Unable to create a buyorder... going back to Main Menu')
        time.sleep(1)
        break
    elif proceed == 2:
      white('Ok... going back to Main Menu')
      time.sleep(1)
      break
    else:
      white('\nInvalid number... going back to Main Menu')
      time.sleep(1)
      break

  if gobuy == True:
    def start_thread_single(market, currency, amount, ask, target):
      time.sleep(1)
      global messages
      thread_name = threading.current_thread().name
      done = False
      while True:
        values = r.hmget(market, 'Ask')
        ask = float(values[0])
        try:
          buy = api.buylimit(market, amount, ask)
        except:
          message = 'Bittrex API error, unable to buy: {0}'.format(buy)
          messages[thread_name] = message
          send_pushover(pushover_user, pushover_app, message)
          send_pushbullet(pushbullet_token, message)
          break
        else:
          time.sleep(0.5)
          buy_uuid = buy['uuid']
          time.sleep(0.5)
          push_send = False
          try:
            buyorder = api.getorder(uuid=buy_uuid)
          except:
            message = 'Bittrex API error, unable to check the buyorder: {0}'.format(buyorder)
            messages[thread_name] = message
          else:
            time.sleep(0.5)
            if buyorder['IsOpen'] == True:
              while buyorder['IsOpen'] == True:
                message = '{0}: Made a buyorder, waiting until it is filled! Remaining: {1:.8f} {2}'.format(thread_name, buyorder['QuantityRemaining'], currency)
                messages[thread_name] = message
                if push_send == False:
                  try:
                    send_pushover(pushover_user, pushover_app, message)
                    send_pushbullet(pushbullet_token, message)
                    push_send = True
                  except:
                    message = 'Unable to send push notification with the buyorder status'
                    messages[thread_name] = message
                try:
                  buyorder = api.getorder(uuid=buy_uuid)
                except:
                  message = 'Bittrex API error, unable to check the buyorder: {0}'.format(buyorder)
                  messages[thread_name] = message
                  pass
                time.sleep(10)
              buyprice = float(ask)
              lastprice = 0
          while True:
            try:
              time.sleep(0.5)
              values = r.hmget(market, 'Ask')
              ask = float(values[0])
            except:
              message = 'Unable to retrieve data from redis.pontstrader.com, trying to recover...'
              messages[thread_name] = message
            else:
              profit_percentage = 100 * (float(ask) - float(buyprice)) / float(buyprice)
              if float(ask) >= float(target):
                try:
                  sell = api.selllimit(market, amount, target)
                  sell_uuid = sell['uuid']
                  time.sleep(0.5)
                  sellorder = api.getorder(uuid=sell_uuid)
                  while sellorder['IsOpen'] == True:
                    message = '{0}: Sell target triggered, waiting until the sell order is completely filled! Remaining: {1:.8f}'.format(thread_name, sellorder['QuantityRemaining'])
                    messages[thread_name] = message
                    try:
                      sellorder = api.getorder(uuid=sell_uuid)
                    except:
                      pass
                    time.sleep(2)
                  message = '{0}: {1} SOLD (Target) | Buy price {2:.8f} | Sell price {3:.8f} | Profit {4:.2f}% (excl. fee)'.format(thread_name, currency, buyprice, target, profit_percentage)
                  messages[thread_name] = message
                  send_pushover(pushover_user, pushover_app, message)
                  send_pushbullet(pushbullet_token, message)
                  done = True
                  break
                except:
                  message = '{0}: API error: Was unable to create the sellorder... it was cancelled due to:\n{1}'.format(thread_name, sell)
                  messages[thread_name] = message
                  send_pushover(pushover_user, pushover_app, message)
                  send_pushbullet(pushbullet_token, message)
                  done = True
                  break
              else:
                message = '{0}: {1} | Buy price {2:.8f} | Price {3:.8f} | Target: {4:.8f} | Profit {5:.2f}% (excl. fee)'.format(thread_name, currency, buyprice, ask, target, profit_percentage)
                messages[thread_name] = message
        if done == True:
          break
    try:
      datetime = datetime.now().strftime("%d-%m-%Y.%H:%M:%S")
      threadname = 'tp-{0}'.format(datetime)
      if oneortwotargets == True:
        thread = threading.Thread(name=threadname, target=start_thread,args=(market, currency, amount, ask, target1, target2))
      else:
        thread = threading.Thread(name=threadname, target=start_thread_single,args=(market, currency, amount, ask, target))
      thread.daemon = True
      thread.start()
      green('Made a buy order, to check its status go to the Stop Loss Take Profit menu again... going back to Main Menu in 2 seconds')
      time.sleep(2)
    except:
      red('Unable to start thread... there is something wrong please contact p0nts!')
