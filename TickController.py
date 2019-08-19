#-*- coding:utf-8 -*-

import time
from datetime import datetime
from copy import deepcopy
import os
from FinalLogger import logger
from DatabaseController import DatabaseController
from Constant import TICK_DIR, inst_thread

class TickController():
    inst_current_tick = {}

    def __init__(self):
        pass

    @staticmethod
    def processTick(pDepthMarketData):
        # important !!! otherwise use the same reference
        tick = deepcopy(pDepthMarketData)
        # print(pDepthMarketData)
        #save ticks of every inst
        TickController.inst_current_tick[tick['InstrumentID']] = tick
        TickController.saveTick(tick)

    @staticmethod
    def makeTickFilename(inst):
        return '%s%s.%s' % (TICK_DIR, inst, 'tick')

    @staticmethod
    def saveTick(tick):
        f = open(TickController.makeTickFilename(tick['InstrumentID']), 'a+')
        try:
            f.write('%s,%.2f,%d,%f\n' % (datetime.now(), tick['LastPrice'], tick['Volume'], tick['AveragePrice']))
        except Exception as err:
            print (err)
        f.close()

    @staticmethod
    def saveDayBar():
        for inst in TickController.inst_current_tick.keys():
            tick = TickController.inst_current_tick[inst]
            print(tick)
            DatabaseController.insert_DayBar(tick)
            #update all indicators!!!
            inst_thread[inst].InitIndicator()












