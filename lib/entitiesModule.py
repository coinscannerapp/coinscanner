#!/usr/bin/python
# Filename: entitiesModule.py
from lib import utilModule as util
from lib import constants
from decimal import Decimal
import datetime

class KlineData(object):
    def __init__(self, symbol, **params):
        self._symbol = symbol
        self._openTime = util.ms2date(params["OpenTime"])
        self._openPrice = Decimal(params["OpenPrice"])
        self._highPrice = Decimal(params["HighPrice"])
        self._lowPrice = Decimal(params["LowPrice"])
        self._closePrice = Decimal(params["ClosePrice"])
        self._volume = params["Volume"]
        self._closeTime = util.ms2date(params["CloseTime"])
        self._quoteAssetVolume = params["QuoteAssetVol"]
        self._numberOfTrades = params["NumberOfTrades"]
        
        

    def openTime(self, t = None): 
        if t: self._openTime = t 
        return self._openTime
    def closeTime(self, t = None): 
        if t: self._closeTime = t 
        return self._closeTime
    def openPrice(self, t = None): 
        if t: self._openPrice = t 
        return self._openPrice
    def closePrice(self):
        return self._closePrice
    def highPrice(self, t = None): 
        if t: self._highPrice = t 
        return self._highPrice
    def lowPrice(self, t = None): 
        if t: self._lowPrice = t 
        return self._lowPrice
    def volume(self, t = None): 
        if t: self._volume = t 
        return self._volumen
    def priceDiff(self): 
        self._priceDiff = self._closePrice - self._openPrice
        return self._priceDiff
    def isGreen(self):
        self._isGreen = True if self.priceDiff() > 0 else False
        return self._isGreen
    def __str__(self):
        # return f'{symbol} start time: {self._openTime}, close time: {self._closeTime}, highest price: {self._highPrice}, lowest price: {self._lowPrice}'
        return f'{self._symbol} start time: {self._openTime}, close time: {self._closeTime}, price difference: {self.priceDiff()} isGreen: {self.isGreen()}'

class PriceMove(object): # This should probably be a super type of the Kline class so that the plus operator could be overloaded to add pricemoves to each other. 
    def __init__(self, lowPrice = 0, highPrice = 0, startPrice = 0, endPrice = 0, startTime = 0, endTime = 0):
        self._startPrice = startPrice
        self._endPrice = endPrice
        self._lowPrice = lowPrice
        self._highPrice = highPrice
        self._startTime = startTime
        self._endTime = endTime
    def startTime(self):
        return self._startTime
    def startPrice(self):
        return self._startPrice
    def endTime(self):
        return self._endTime
    def endPrice(self):
        return self._endPrice
    def highPrice(self):
        return self._highPrice
    def lowPrice(self):
        return self._lowPrice
    def priceDiff(self):
        self._priceDiff = self._endPrice - self._startPrice 
        return self._priceDiff

    def percentDiff(self):
        if(self.startPrice()!=0):
            self._percentDiff = self.priceDiff()/self.startPrice()*100
            # print(f'percentDiff: priceDiff={self._priceDiff} and startPrice = {self._startPrice}')
        else:
            self._percentDiff = 0
        return round(self._percentDiff, 2)

    def durationSecs(self):
        self._timeDiff = self._endTime - self._startTime
        seconds = round(self._timeDiff.total_seconds(),0)
        return seconds
    def durationHours(self):
        return self.durationSecs()/(60*60)

    def isGreen(self):
        self._isGreen = True if self.priceDiff() > 0 else False
        return self._isGreen
    
    def isPowerMove(self):
        return self.isPowerDrop() or self.isPowerRaise()
    def isPowerDrop(self):
        return self.durationHours() < constants.MAX_DURATION and self.percentDiff() < constants.MIN_PRICE_DIFF*-1
    def isPowerRaise(self):
        return (self.durationHours() < constants.MAX_DURATION and self.percentDiff() > constants.MIN_PRICE_DIFF)
        # return self.durationHours() < constants.MAX_DURATION
        # return self.percentDiff() > constants.MIN_PRICE_DIFF
    
    def createBase(self, other):
        if self.isPowerRaise() and other.isPowerDrop():
            if self.hoursAppart(other) <= constants.MAX_HOURS_APPART:
                return PriceMove(
                    lowPrice=other.lowPrice(), 
                    highPrice=self.highPrice(), 
                    startPrice=other.startPrice(), 
                    endPrice=self.endPrice(), 
                    startTime=other.startTime(), 
                    endTime=self.endTime())
                

    def hoursAppart(self, other):
        return round(datetime.timedelta.total_seconds(self.startTime() - other.endTime())/(60*60), 0)

    def addKline(self, k): # returns bool to tell if adding the kline strengthend the priceMove or reverse
        # print(f'Just into Add Kline: priceDiff={self.priceDiff()} and startPrice = {self._startPrice}')
        if self.isFirstKline():
            self._startTime = k.openTime()
            self._startPrice = k.openPrice()
            self._endTime = k.closeTime()
            self._endPrice = k.closePrice()
            self._lowPrice = k.lowPrice() 
            self._highPrice = k.highPrice()
        # Is the kline good to incorporate?
        if self.klineIsSameDirection(k) and self.klineImpact(k) > constants.MAX_ALLOWED_NEG_IMPACT : # negative impact comes as a negative number
            self._endTime = k.closeTime()
            self._endPrice = k.closePrice()
            self._endTime = k.closeTime()
            self._endPrice = k.closePrice()
            self._lowPrice = k.lowPrice() if k.lowPrice() < self.lowPrice() else self.lowPrice()
            self._highPrice = k.highPrice() if k.highPrice() > self.highPrice() else self.highPrice()
            return True
        else:
            return False
        
    def klineIsSameDirection(self, k):
        if self.priceDiff() == 0.0:
            return True
        if (k.isGreen() and self.isGreen()):
            return True
        if not k.isGreen():
            if not self.isGreen():
                return True
        return False

    def isFirstKline(self):
        if self._startPrice == 0: 
            return True
        return False

    def klineImpact(self, kline):
        klineDiff = kline.priceDiff()
        thisDiff = self.priceDiff()
        percentageImpact = 0 if thisDiff == 0 else round(klineDiff/thisDiff*100, 2)
        return percentageImpact
    def __add__(self, other): # overloading the + operator (to be able to add klines value differences to each other)
        startTime = self.startTime() if self.startTime() < other.startTime() else other.startTime()
        endTime = self.endTime() if self.endTime() > other.endTime() else other.endTime()
        startPrice = self.startPrice() if self.startTime() < other.startTime() else other.startPrice()
        endPrice = other.endPrice() if self.startTime() < other.startTime() else other.endPrice()
        lowPrice = self.lowPrice() if self.lowPrice() < other.lowPrice() else other.lowPrice()
        highPrice = self.highPrice() if self.highPrice() > other.highPrice() else other.highPrice()

        return PriceMove(lowPrice=lowPrice, highPrice=highPrice, startPrice=startPrice, endPrice=endPrice, startTime=startTime, endTime=endTime)
# end of module: entitiesModule.py
