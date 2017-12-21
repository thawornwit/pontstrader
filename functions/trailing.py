#!/usr/bin/env python
    
def trailing(key, secret, pushover_user, pushover_app, pushbullet_token, redis_password):

  import sys, os, json, time, threading, requests, redis
  from datetime import datetime
  from bittrex import bittrex
  from pushover import send_pushover
  from pushbullet import send_pushbullet
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

  global tsl_messages
  global tsl_messages_done

  try:
    tsl_messages
  except NameError:
    tsl_messages = {}
  else:
    pass

  try:
    tsl_messages_done
  except NameError:
    tsl_messages_done = {}
  else:
    pass
  
  white((40 * '-'))
  green('   T R A I L I N G  S T O P  L O S S')
  white((40 * '-'))
  while True:
    status_update = False
    gobuy = False
    try:
      threads = threading.enumerate()
      thread_counter = 0
      for t in threading.enumerate():
        if t.name.startswith('tsl-'):
          thread_counter += 1
      if thread_counter > 0:
        yellow('There are currently {0} active tsl trade(s):'.format(thread_counter))
      else:
        yellow('There are currently no active tsl trades')
      white('Would you like to make another tsl trade, check active trades or check history of your tsl trades?')
      green('1. New trade')
      yellow('2. Active trades')
      yellow('3. History')
      red('4. Back to Main Menu')
      try:
        yes_no = raw_input(Fore.WHITE+'Enter your choice [1-4] : ')
        yes_no = int(yes_no)
        white((30 * '-'))
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
            for k, v in tsl_messages.iteritems():
              trades += 1
              if v.startswith('tsl-'):
                print v
            if trades == 0:
              red('There is currently no tsl trade status available!')
              white((30 * '-'))
            white('Refresh, new trade or back to Main Menu?')
            green('1. Refresh')
            yellow('2. New Trade')
            red('3. Back to Main Menu')
            go_break = False
            try:
              yes_no = raw_input(Fore.WHITE+'Enter your choice [1-3] : ')
              yes_no = int(yes_no)  
              white((30 * '-'))
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
        while True:
          try:
            trades = 0
            for k, v in tsl_messages_done.iteritems():
              trades += 1
              if v.startswith('tsl-'):
                print v
            if trades == 0:
              red('There is currently no tsl trade history available!')
              white((30 * '-'))
            white('Refresh, new trade or back to Main Menu?')
            green('1. Refresh')
            yellow('2. New Trade')
            red('3. Back to Main Menu')
            go_break = False
            try:
              yes_no = raw_input(Fore.WHITE+'Enter your choice [1-3] : ')
              yes_no = int(yes_no)
              white((30 * '-'))
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
      elif yes_no == 4:
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
  
    try:
      value = raw_input(Fore.WHITE+'How much {0}? (excl. fee) : '.format(trade))
      value = float(value)
    except:
      white('\nInvalid number... going back to Main Menu')
      time.sleep(1)
      break
  
    try:
      trailing = raw_input(Fore.WHITE+'Trailing percentage? (without %) : ')
      trailing = float(trailing)
    except:
      white('\nInvalid number... going back to Main Menu')
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
      api = bittrex(key, secret)
      values = r.hmget(market, 'Ask', 'MarketName', 'BaseVolume', 'Volume', 'OpenBuyOrders', 'OpenSellOrders', 'High', 'Low', 'Last', 'Bid')
      available = api.getbalance(trade)
      price = float(values[0])
    except:
      white('API error: Unable to retrieve pricing information... going back to Main Menu')
      time.sleep(1)
      break
    
    if available['Available'] < 0.00100000:
      red('Not enough {0} to make a buy... going back to Main Menu'.format(trade))
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
    white('Proceed?')
    green('1. yes')
    red('2. no')
    try:
      proceed = raw_input(Fore.WHITE+'Enter your choice [1-2] : ')
      proceed = int(proceed)
    except:
      white('\nCancelled... going back to Main Menu')
      time.sleep(1)
      break
    if proceed == 1:
      try:
        values = r.hmget(market, 'Ask', 'Bid')
        ask = float(values[0])
        bid = float(values[1])
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
            values = r.hmget(market, 'Ask', 'Bid')
            ask = float(values[0])
            bid = float(values[1])
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
    def start_thread(market, currency, amount, ask, trailing):
      time.sleep(1)
      global tsl_messages
      thread_name = threading.current_thread().name
      while True:
        try:
          buy = api.buylimit(market, amount, ask)
          time.sleep(0.5)
          buy_uuid = buy['uuid']
          time.sleep(0.5)
          buyorder = api.getorder(uuid=buy_uuid)
          push_send = False
          while buyorder['IsOpen'] == True:
            message = '{0}: Made a buyorder, waiting until it is filled! Remaining: {1:.8f} {2}'.format(thread_name, buyorder['QuantityRemaining'], currency)
            tsl_messages[thread_name] = message
            if push_send == False:
              send_pushover(pushover_user, pushover_app, message)
              send_pushbullet(pushbullet_token, message)
              push_send = True
            buyorder = api.getorder(uuid=buy_uuid)
            time.sleep(10)
          trailing_percentage = float(ask) / 100 * float(trailing)
          trailing_stop_loss = float(ask) - float(trailing_percentage)
          stop_loss_percentage = '-{0:.2f}'.format(trailing)
          buyprice = float(ask)
          lastprice = 0
        except:
          message = '{0}: API error: Was unable to create the buyorder... it was cancelled due to:\n{1}'.format(thread_name, buy)
          tsl_messages[thread_name] = message
          send_pushover(pushover_user, pushover_app, message)
          send_pushbullet(pushbullet_token, message)
          break
        while float(ask) > float(trailing_stop_loss):
          try:
            time.sleep(0.5)
            values = r.hmget(market, 'Ask')
            ask = float(values[0])
          except:
            message = 'Unable to retrieve data from redis.pontstrader.com, trying to recover...'
            tsl_messages[thread_name] = message
          else:
            percentage = 100 * (float(ask) - float(buyprice)) / float(buyprice)
            trailing_percentage = float(ask) / 100 * float(trailing)
            if float(ask) > float(buyprice) and ask != lastprice:
              if float(ask) > lastprice and float(ask) > float(buyprice):
                new_trailing_stop_loss = float(ask) - float(trailing_percentage)
                if float(new_trailing_stop_loss) > float(trailing_stop_loss):
                  trailing_stop_loss = float(ask) - float(trailing_percentage)
                  stop_loss_percentage = 100 * (float(trailing_stop_loss) - float(buyprice)) / float(buyprice)
                  message = '{0}: {1} | Buy price {2:.8f} | Price {3:.8f} | Profit: {4:.2f}% | Stop Loss: {5:.8f} ({6:.2f}%)'.format(thread_name, currency, float(buyprice), float(ask), float(percentage), float(trailing_stop_loss), float(stop_loss_percentage))
                  tsl_messages[thread_name] = message
                else:
                  message = '{0}: {1} | Buy price {2:.8f} | Price {3:.8f} | Profit: {4:.2f}% | Stop Loss: {5:.8f} ({6:.2f}%)'.format(thread_name, currency, float(buyprice), float(ask), float(percentage), float(trailing_stop_loss), float(stop_loss_percentage))
                  tsl_messages[thread_name] = message
              else:
                message = '{0}: {1} | Buy price {2:.8f} | Price {3:.8f} | Profit: {4:.2f}% | Stop Loss: {5:.8f} ({6:.2f}%)'.format(thread_name, currency, float(buyprice), float(ask), float(percentage), float(trailing_stop_loss), float(stop_loss_percentage))
                tsl_messages[thread_name] = message
            elif float(ask) < float(buyprice) and float(ask) != float(lastprice):
              message = '{0}: {1} | Buy price {2:.8f} | Price {3:.8f} | Profit: {4:.2f}% | Stop Loss: {5:.8f} ({6:.2f}%)'.format(thread_name, currency, float(buyprice), float(ask), float(percentage), float(trailing_stop_loss), float(stop_loss_percentage))
              tsl_messages[thread_name] = message
            elif float(ask) == float(buyprice) and float(ask) != float(lastprice):
              pass
            lastprice = float(ask)
        profit_percentage = 100 * (float(trailing_stop_loss) - float(buyprice)) / float(buyprice)
        try:
          sell = api.selllimit(market, amount, trailing_stop_loss)
          sell_uuid = sell['uuid']
          time.sleep(0.5)
          sellorder = api.getorder(uuid=sell_uuid)
          while sellorder['IsOpen'] == True:
            message = '{0}: Stop Loss triggered, waiting until the sell order is completely filled! Remaining: {1:.8f}'.format(thread_name, sellorder['QuantityRemaining'])
            tsl_messages[thread_name] = message
            try:
              sellorder = api.getorder(uuid=sell_uuid)
            except:
              pass
            time.sleep(2)
          message = '{0}: {1} SOLD | Buy price {2:.8f} | Sell price {3:.8f} | Profit {4:.2f}% (excl. fee)'.format(thread_name, currency, buyprice, trailing_stop_loss, profit_percentage)
          del tsl_messages[thread_name]
          tsl_messages_done[thread_name] = message
          send_pushover(pushover_user, pushover_app, message)
          send_pushbullet(pushbullet_token, message)
          break
        except:
          message = '{0}: API error: Was unable to create the sellorder... it was cancelled due to:\n{1}'.format(thread_name, sell)
          del tsl_messages[thread_name]
          tsl_messages_done[thread_name] = message
          send_pushover(pushover_user, pushover_app, message)
          send_pushbullet(pushbullet_token, message)
          break
  
    try:
      datetime = datetime.now().strftime("%d-%m-%Y.%H:%M:%S") 
      threadname = 'tsl-{0}'.format(datetime)
      thread = threading.Thread(name=threadname, target=start_thread,args=(market, currency, amount, ask, trailing))
      thread.daemon = True
      thread.start()
      green('Made a buy order, to check its status go to the Trailing Stop Loss menu again... going back to Main Menu in 2 seconds')
      time.sleep(2)
    except:
      red('Unable to start thread... there is something wrong please contact p0nts!')
