#-*- coding=utf-8 -*-
import sys
import getopt
import time
import sqlite3
from MdApiPy import MdApiPy
from TickController import TickController
from Constant import BROKER_ID,INVESTOR_ID,PASSWORD,ADDR_MD,LOGS_DIR,inst_strategy,inst_thread

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def dealZhengZhou(symbol):
    CZCE_INSTRUMENTS = (
        'sr', 
        'sm',
        'sf',
        'ap',
        'cj',
        'cf',
        'ta',
        'ma',
        'rm',
        'oi',
        'fg',
        'zc',
        'cy',
        'ur'
    )
    if symbol[0].isupper():
        inst = symbol.lower()
        # 郑州商品交易所 CZCE TA001 -> ta2001
        # inst = inst[:-3]+'2'+inst[-3:]
        return inst
    return symbol

def start():
    db = sqlite3.connect('futures.db3', check_same_thread = False)
    c = db.execute('SELECT name FROM contract')

    user_md = MdApiPy(instruments=[dealZhengZhou(row[0]) for row in c.fetchall()], broker_id=BROKER_ID, investor_id=INVESTOR_ID, passwd=PASSWORD)
    user_md.Create(LOGS_DIR +"_md")
    user_md.RegisterFront(ADDR_MD)
    user_md.Init()

    _date = '19700101'
    while True:
        time.sleep(60)
        _time = time.strftime('%H%M%S')
        hint_time = time.localtime(time.time())
        if hint_time.tm_min % 15 == 0:
            print ('The main thread is runing, date = %s, time = %s' % (time.strftime('%Y-%m-%d'),time.strftime('%H:%M:%S')))
        if '150000'< _time < '150100' and _date < time.strftime('%Y%m%d'):
            TickController.saveDayBar()
            _date = time.strftime('%Y%m%d')

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error:
            raise Usage("opt error")
        #more code, unchanged
        for opt, value in opts:
            if opt in ("-h", "--help"):
                print ('please input null parameter to run.')
            elif opt in ("-t", "--test"):
                print ('not used, just test.')
        else:
            start()

    except Usage:
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())






