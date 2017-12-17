#!/usr/bin/python2.7

import sys
import json
import os
from functions import *
import signal
import time

def sigint_handler(signum, frame):
  print 'Stop pressing CTRL+C!'

signal.signal(signal.SIGINT, sigint_handler)

if len(sys.argv) == 2:
  if sys.argv[1] == 'version':
    print 'Version: pontstrader-v3.2'
    sys.exit()
  else:
    print 'Unsupported argument, supported arguments are: version'
    print 'e.g. {0} version'.format(sys.argv[0])
    sys.exit()

try:
  import requests
except ImportError:
  print 'python-requests is not installed, please check the docs!'
  print 'https://github.com/p0nt/pontstrader'
  sys.exit()

try:
  from colorama import Fore, Back, Style, init
except ImportError:
  print 'python-colorama is not installed, please check the docs!'
  print 'https://github.com/p0nt/pontstrader'
  sys.exit()

try:
  import redis
except ImportError:
  print 'redis is not installed, please check the docs!'
  print 'https://github.com/p0nt/pontstrader'
  sys.exit()

config_json = (os.path.dirname(os.path.realpath(__file__))) + '/settings.json'
file_exists = os.path.isfile(config_json)

if not file_exists:
  yellow('It seems that you are running this script for the first time')
  yellow('or')
  yellow('If you\'ve upgraded to v3.2, you can copy/paste data from config.json and remove afterwards')
  try:
    yellow('Step 1: Bittrex API')
    bittrex_key = raw_input(Fore.WHITE+'Enter your Bittrex API key : ')
    bittrex_key = str(bittrex_key)
    bittrex_secret = raw_input(Fore.WHITE+'Enter your Bittrex API Secret : ')
    bittrex_secret = str(bittrex_secret)
    yellow('Step 2: Push notifications')
    yellow('Pushover/Pushbullet allows you to recieve push notifications on your phone for the Trailing Stop feature and future features.')
    white('Would you like to enable Pushover or Pushbullet?')
    white('1. Pushover')
    white('2. Pushbullet')
    white('3. No')
    white('4. Exit')
    push = raw_input(Fore.WHITE+'Enter your choice [1-4] : ')
    push = int(push)
    pushover_user = 'disabled'
    pushover_app = 'disabled'
    pushbullet_token = 'disabled'
    if push == 1:
      pushover_user = raw_input(Fore.WHITE+'Enter your Pushover user key : ')
      pushover_user = str(pushover_user)
      pushover_app = raw_input(Fore.WHITE+'Enter the Pushover app key : ')
      pushover_app = str(pushover_app)
    elif push == 2:
      pushbullet_token = raw_input(Fore.WHITE+'Enter your Pushbullet Access Token : o.')
      pushbullet_token = str(pushbullet_token) 
      pushbullet_token = 'o.{0}'.format(pushbullet_token)
    elif push == 3:
      white('OK... disabling push notifiations! (remove config.json if you want to re-run the wizard)')
      pushover_user = 'disabled'
      pushover_app = 'disabled'
      pushbullet_token = 'disabled'
    elif push == 4:
      red('Cancelled... unable to finish setup, please try again!')
      sys.exit()
    else:
      white('Wrong number... disabling push notifications for now! (remove config.json if you want to re-run the wizard)')
      pushover_user = 'disabled'
      pushover_app = 'disabled'
      pushbullet_token = 'disabled'
    yellow('Step 3: Redis Connection')
    yellow('Redis a key value database which you have to connect to to make this script work')
    redis_password = raw_input(Fore.WHITE+'Enter the Redis password : ')
    redis_password = str(redis_password)
  except:
    red('Cancelled... unable to finish setup, please try again!')
    sys.exit()
  data = { 'bittrex_key' : bittrex_key, 'bittrex_secret' : bittrex_secret, 'pushover_user' : pushover_user, 'pushover_app' : pushover_app, 'pushbullet_token' : pushbullet_token, 'redis_password' : redis_password }
  with open(config_json, 'w') as outfile:
    json.dump(data, outfile)
    outfile.close()
  with open(config_json, 'r') as data_file:
    data = json.load(data_file)
    apikey = str(data['bittrex_key'])
    apisecret = str(data['bittrex_secret'])
    pushover_user = str(data['pushover_user'])
    pushover_app = str(data['pushover_app'])
    pushbullet_token = str(data['pushbullet_token'])
    redis_password = str(data['redis_password'])
  green('Setup is done, you can now use pontstrader')
  time.sleep(2)

with open(config_json, 'r') as data_file:
  data = json.load(data_file)
  apikey = str(data['bittrex_key'])
  apisecret = str(data['bittrex_secret'])
  pushover_user = str(data['pushover_user'])
  pushover_app = str(data['pushover_app'])
  pushbullet_token = str(data['pushbullet_token'])
  redis_password = str(data['redis_password'])

menu(apikey, apisecret, pushover_user, pushover_app, pushbullet_token, redis_password)
