from lib import getDataModule as getData
from lib import utilModule as util 
from lib import entitiesModule as entities
from lib import constants
# external
from binance.client import Client
import json

# key = constants.KEY
# secret = constants.SECRET
# symbol = constants.SYMBOL
# start = constants.START
# end = constants.END

KLINE_INTERVAL = Client.KLINE_INTERVAL_1HOUR
client = Client(constants.KEY, constants.SECRET) # create the Binance client, no need for api key to just read data

def main():
    klines = getData.get_historical_klines(client, constants.SYMBOL, KLINE_INTERVAL, constants.START, constants.END)
    klinelist = populateKlineList(klines)
    # listOfMoves = populatePriceMoveList(klinelist)
    # for move in listOfMoves:
    #     if move.percentDiff() < -10:
    #         print(f'{move.startTime()} has {move.percentDiff()}% drop in {move.durationHours()} hours')
    #     elif move.percentDiff() > 10:
    #         print(f'{move.startTime()} has {move.percentDiff()}% raise in {move.durationHours()} hours')
    
    print(f'LENGTH OF LIST {len(klinelist)}')
    # listOfBases = createBases(klinelist)
    # print(f'LENGTH OF BASES LIST {len(listOfBases)}')
    # for base in listOfBases:
    #     print(f'BASE: {base.startTime()}')
    # util.writeList2File(klinelist, KLINE_INTERVAL)
    powerMoves = filterPowerMoves(populatePriceMoveList(klinelist))
    print(f'LENGTH OF LIST {len(powerMoves)}')

    
def populateKlineList(klines):
        klinelist = []
        for kline in klines:
            klineObj = entities.KlineData(
                symbol = constants.SYMBOL,
                OpenTime= kline[0],
                OpenPrice = kline[1],
                HighPrice = kline[2],
                LowPrice = kline[3],
                ClosePrice = kline[4],
                Volume = kline[5],
                CloseTime = kline[6],
                QuoteAssetVol = kline[7],
                NumberOfTrades = kline[8],
            )
            klinelist.append(klineObj)
        return klinelist

def populatePriceMoveList(klinelist):
    listOfMoves = list()
    priceMove = entities.PriceMove()
    for k in klinelist:
        if not priceMove.addKline(k): #if addKline returns false its time to start a new PriceMove
            listOfMoves.append(priceMove)
            priceMove = entities.PriceMove()
            priceMove.addKline(k)
    return listOfMoves

def filterPowerMoves(listOfMoves):
    powerMoves = list()
    for m in listOfMoves:
        if m.isPowerMove():
            print('POWER MOOOOOOOVE')
            powerMoves.append(m)
    return powerMoves



def createBases(klinelist):
    listOfBases = list()
    priceMove = entities.PriceMove()
    lastPowerMove = None
    for k in klinelist:
        if not priceMove.addKline(k): #if addKline returns false its time to start a new PriceMove
            if priceMove.isPowerMove():
                print('POWERMOVE')
                if lastPowerMove != None:
                    print('NOT None')
                    base = priceMove.createBase(lastPowerMove)
                    if(base != None):
                        listOfBases.append(base)
                lastPowerMove = priceMove
                priceMove = entities.PriceMove()
                priceMove.addKline(k)
    return listOfBases
            

if __name__ == '__main__': main()
