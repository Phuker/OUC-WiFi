#!/usr/bin/env python
# encoding: utf-8
# login ouc-wifi
#
# --once run only once
#

import os
import re
import time
import json
import logging
import sys
import signal

try:
    import requests
except ImportError:
    print 'Missing library: requests'
    print 'Run: pip install requests'
    sys.exit(2)

DEBUG = False
CONFIG_FILE = 'config.json'
TEST_URL = 'http://220.181.57.216/favicon.ico'
WIFI_OFFLINE_FLAG = '10.100.29.2/a79.htm'
WIFI_LOGIN_URL = 'http://10.100.29.2:801/eportal/'
OFFICE_OFFLINE_FLAG = 'http://10.81.2.6'
OFFICE_LOGIN_URL = 'https://yxrz.ouc.edu.cn/a70.htm'
SUCCESS_FLAG = '<!--Dr.COMWebLoginID_3.htm-->'
SLEEP_INTERVAL = 120  # second
ESSID_LIST = ['OUC-WIFI', 'OUC-AUTO']
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/601.2.7 (KHTML, like Gecko) Version/9.0.1 Safari/601.2.7',
    'Connection': 'close',
}

network = 'oucwifi'
requests.packages.urllib3.disable_warnings()

if DEBUG:
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s(%(lineno)d) [%(levelname)s]:%(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        stream=sys.stdout)
else:
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        stream=sys.stdout)

if os.environ.has_key('ALL_PROXY'):
    __ = os.environ['ALL_PROXY']
    PROXIES = {'http': __, 'https': __}
    logging.info('Using proxy: %s', repr(__))
else:
    PROXIES = None

__ = os.path.dirname(os.path.realpath(sys.argv[0]))
if __ != '':
    os.chdir(__)

sess = requests.Session()
sess.proxies = PROXIES
for key in HEADERS:
    sess.headers[key] = HEADERS[key]

if len(sys.argv) == 2 and sys.argv[1] == '--once':
    run_once = True
else:
    run_once = False

droid = None


def get_android_obj():
    global droid
    droid = androidhelper.Android()
    droid.eventRegisterForBroadcast('android.net.conn.CONNECTIVITY_CHANGE')


def generate_config():
    logging.info('Please input your id and password for the first time.')

    while True:
        userid = raw_input('Input id: ').strip()
        password = raw_input('Input password: ')

        if userid.isdigit() and password != '':
            break
        else:
            logging.error('Wrong format')

    config = {'userid': userid, 'password': password}
    json_str = json.dumps(config)
    try:
        with open(CONFIG_FILE, 'w') as f:
            f.write(json_str)
    except Exception, e:
        logging.critical('Error when saving id and password to file %s %s', str(type(e)), str(e))
        sys.exit(1)


def load_config():
    global userid, password
    with open(CONFIG_FILE, 'r') as f:
        json_str = f.read()
    config = json.loads(json_str)

    userid = config['userid']
    password = config['password']


def log_and_toast(info):
    logging.info(info)
    droid.makeToast(info)


# work properly after computer hibernate
def sleep(second):
    start_time = time.time()
    end_time = start_time + second
    small_sleep = 5
    small_sleep_count = int(float(second) / small_sleep)
    left_sleep = float(second) - small_sleep_count * small_sleep

    for i in xrange(small_sleep_count):
        time.sleep(small_sleep)
        if time.time() > end_time:
            return

    time.sleep(left_sleep)


def is_offline():
    global network

    try:
        r = sess.get(TEST_URL, allow_redirects=False, timeout=10)
    except Exception, e:
        logging.debug('Error test offline %s %s', str(type(e)), str(e))
        network = 'oucwifi'
        return True

    if r.status_code == 200:
        if WIFI_OFFLINE_FLAG in r.content:
            network = 'oucwifi'
            return True
        else:
            return False
    elif r.status_code == 302:
        if r.next.url == OFFICE_OFFLINE_FLAG:
            network = 'office'
            return True
        else:
            return False
    else:
        raise Exception('Unknown status code %d when detecting offline' % r.status_code)


def login():
    if network == 'oucwifi':
        url = WIFI_LOGIN_URL
        params = {'c': 'ACSetting', 'a': 'Login'}
        data = {
            'DDDDD': ',1,' + userid,
            'upass': password,
            'R1': '0',
            'R2': "",
            'R6': '0',
            'para': '00',
            '0MKKey': '123456',
            'buttonClicked': '',
            'redirect_url': '',
            'err_flag': '',
            'username': '',
            'password': '',
            'user': '',
        }
    elif network == 'office':
        url = OFFICE_LOGIN_URL
        params = {}
        data = {
            'DDDDD': userid,
            'upass': password,
            'R1': '0',
            'R2': "",
            'R6': '0',
            'para': '00',
            '0MKKey': '123456',
            'buttonClicked': '',
            'redirect_url': '',
            'err_flag': '',
            'username': '',
            'password': '',
            'user': '',
            'R7': '0',
        }
    else:
        raise Exception('Unknown network type: %s' % repr(network))

    try:
        r = sess.post(url, params=params, data=data, timeout=4, verify=False)
    except Exception as e:
        logging.error('Network error %s', str(type(e)))
        return False

    if SUCCESS_FLAG in r.content:
        return True
    else:
        return False


def android_wait_wifi(timeout):
    while True:
        try:
            eventResult = droid.eventWait(timeout * 1000)  # block until timeout (micro second)
        except Exception as e:
            get_android_obj()
            log_and_toast('Android API error')
            logging.error('%s %s', str(type(e)), str(e))
            time.sleep(3)
            continue

        # no event, timeout
        if eventResult.result == None:
            wifiInfo = droid.wifiGetConnectionInfo().result
            if wifiInfo[u'network_id'] != -1 and wifiInfo[u'ssid'] in [u'"' + item + u'"' for item in ESSID_LIST]:
                return
        else:    # there was an event
            data = eventResult.result['data']
            data = json.loads(data)
            info = data['networkInfo']

            if info.startswith('[type: MOBILE'):
                if 'CONNECTED/CONNECTED' in info:
                    log_and_toast('Mobile network')
            elif info.startswith('[type: WIFI'):
                if 'CONNECTED/CONNECTED' in info:
                    ssid = droid.wifiGetConnectionInfo().result[u'ssid']
                    ssid = json.loads(ssid)
                    log_and_toast('Connected to: ' + ssid.encode('utf-8'))
                    if ssid in ESSID_LIST:
                        return
            elif info.startswith('[type: VPN'):
                if 'CONNECTED/CONNECTED' in info:
                    log_and_toast('VPN')
            else:
                log_and_toast('Other network')


def main_android():
    logging.info('OUC-WiFi.py on Android')
    while True:
        android_wait_wifi(SLEEP_INTERVAL)
        if droid.wifiGetConnectionInfo().result[u'ssid'] not in [u'"' + item + u'"' for item in ESSID_LIST]:
            logging.info('Not using %s', repr(ESSID_LIST))
        else:
            if is_offline():
                log_and_toast('Offline, logging in...')
                if login():
                    log_and_toast('Login successfully')
                else:
                    log_and_toast('Login failed')
            else:
                logging.info('Online')

        if run_once:
            return


def main_pc():
    logging.info('OUC-WiFi auto login program on PC')
    while True:
        if is_offline():
            logging.info('You are offline. Logging in...')
            if login():
                logging.info('Login successfully')
            else:
                logging.info('Login failed')
        else:
            logging.info('Online')

        if run_once:
            return
        else:
            sleep(SLEEP_INTERVAL)


def exit_handler(signum, frame):
    print ''
    logging.info('Exiting')
    sys.exit(0)


if __name__ == '__main__':
    if not os.path.isfile(CONFIG_FILE):
        generate_config()

    load_config()

    signal.signal(signal.SIGTERM, exit_handler)
    signal.signal(signal.SIGINT, exit_handler)

    try:
        import androidhelper
        get_android_obj()
        main_android()
    except ImportError:
        main_pc()
    except Exception as e:
        logging.exception('Error: %s %s', str(type(e)), str(e))
        logging.info('Exiting')
        sys.exit(1)
