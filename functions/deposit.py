#!/usr/bin/env python

def deposit(key, secret):

  import time, json, sys
  from bittrex import bittrex
  from colors import white, red, green, yellow
  from colorama import Fore, Back, Style, init
  init()

  while True:
    try:
      api = bittrex(key, secret)
    except:
      white('Bittrex API error: {0}'.format(api))
      white('Going back to Main Menu')
      time.sleep(1)
      break

    white((30 * '-'))
    green('   D E P O S I T')
    white((30 * '-'))
    try:
      currency = raw_input(Fore.WHITE+'Currency? (e.g. LTC / NEO / OMG) : ').upper()
    except:
      white('Invalid currency... going back to Main Menu')
      time.sleep(1)
      break
    else:
      try:
        apicall = api.getdepositaddress(currency)
        address = apicall['Address']
        red('WARNING! Bittrex API is crap and does not provide proper addresses on coins that require additional settings such as a tag (XRP) or paymentid (NXT)')
        green('{0} deposit address: {1}'.format(currency, address))
        yellow('Returning to Main Menu in 5 seconds...')
        time.sleep(5)
        break
      except:
        white('Unable to retrieve data from Bittrex... returning to Main Menu')
        time.sleep(1)
        break
