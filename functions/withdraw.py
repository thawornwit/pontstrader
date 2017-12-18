#!/usr/bin/env python
  
def withdraw(key, secret):
  
  import time, json, sys
  from pprint import pprint
  from time import gmtime, strftime
  from bittrex import bittrex
  from colors import white, red, green, yellow
  from colorama import Fore, Back, Style, init
  init()
  
  while True:
    try:
      api = bittrex(key, secret)
      currencies = api.getcurrencies()
    except:
      white('Bittrex API error: {0}'.format(api))
  
    white((30 * '-'))
    green('   W I T H D R A W')
    white((30 * '-'))
    yellow('NOTE: Make sure Withdraw is allowed for this API key')
    white((30 * '-'))
    try:
      balances = api.getbalances()
      green('Currency\tAvailable')
      number = 0
      list = []
      for coin in balances:
        available = coin["Available"]
        currency = coin["Currency"]
        if available != 0.0:
          number += 1
          list.append(currency)
          if len(currency) > 4:
            white('{0}. {1}\t{2:.8f}'.format(number, currency, available))
          else:
            white('{0}. {1}\t\t{2:.8f}'.format(number, currency, available))
    except:
      white('Bittrex API error: {0}'.format(balances))
      white('Going back to Main Menu')
      time.sleep(2)
    try:
      choose_num = raw_input(Fore.WHITE+'Enter your choice [1-{0}] : '.format(number))
      choose_num = int(choose_num)
    except:
      white('\nInvalid number... going back to Main Menu')
      time.sleep(1)
      break
    try:
      choose_num = choose_num - 1
      if choose_num == -1:
        white('Invalid number... going back to Main Menu')
        time.sleep(1)
        break
      for f in currencies:
        if f['Currency'] == list[choose_num]:
          fee = f['TxFee']
      green('Starting withdraw for {0}'.format(list[choose_num]))
      white((30 * '-'))
      balance = api.getbalance(list[choose_num])
      available = balance["Available"]
      white('Available: {0} {1}'.format(available, list[choose_num]))
      white('Fee:       {0} {1}'.format(fee, list[choose_num]))
      yellow('Fee will be calculated at the end, you may just withdraw the full amount.')
      white((30 * '-'))
    except:
      white('\nInvalid number... going back to Main Menu')
      time.sleep(1)
      break
    try:
      quantity = raw_input(Fore.WHITE+'Quantity? : ')
      quantity = float(quantity)
    except:
      white('\nInvalid number... going back to Main Menu')
      time.sleep(1)
      break
    if quantity > available:
      white('You can\'t withdraw more than available. Cancelled...')
      time.sleep(1)
      break
    try:
      address = raw_input(Fore.WHITE+'Withdraw Address? : ')
      address = str(address)
    except:
      white('Invalid input. Cancelled...')
      time.sleep(1)
      break
    try:
      paymentid = raw_input(Fore.WHITE+'Payment ID?' + Fore.YELLOW +' (If not required, leave empty)' + Fore.WHITE +' : ')
      paymentid = str(paymentid)
    except:
      white('Invalid input. Cancelled...')
      time.sleep(1)
      break
    white((30 * '-'))
    yellow('BITTREX NOTE: Please verify your withdrawal address. We cannot refund an incorrect withdrawal.')
    white((30 * '-'))
    if len(paymentid) > 0:
      green('You are about to withdraw {0:.8f} {1} to {2} with Payment ID {3}, is this correct?'.format(quantity, list[choose_num], address, paymentid))
    else:
      green('You are about to withdraw {0:.8f} {1} to {2}, is this correct?'.format(quantity, list[choose_num], address))
    green('1. yes')
    red('2. no (Back to Main Menu)')
    white((30 * '-'))
    try:
      yes_no = raw_input(Fore.WHITE+'Enter your choice [1-2] : ')
      yes_no = int(yes_no)
    except:
      white('\nInvalid number... going back to Main Menu')
      time.sleep(1)
      break
    if yes_no == 1:
      try:
        if len(paymentid) > 0:
          apicall = api.withdraw(currency=list[choose_num], quantity=quantity, address=address, paymentid=paymentid)
        else:
          apicall = api.withdraw(currency=list[choose_num], quantity=quantity, address=address)
        print apicall['uuid']
        after_fee = quantity - fee
        if len(paymentid) > 0:
          green('Added a withdraw order for {0:.8f} {1} towards {2} with Payment ID {3} (incl. bittrex fee)'.format(after_fee, list[choose_num], address, paymentid))
        else:
          green('Added a withdraw order for {0:.8f} {1} towards {2} (incl. bittrex fee)'.format(after_fee, list[choose_num], address))
        white('Returning to Main Menu in 5 seconds...')
        time.sleep(5)
        break
      except:
        white('Bittrex API error: {0}'.format(apicall))
        white('Going back to Main Menu')
        time.sleep(2)
        break
    elif yes_no == 2:
      white('\nCancelled... going back to Main Menu')
      time.sleep(1)
      break
    else:
      white('\nInvalid number... going back to Main Menu')
      time.sleep(1)
      break
