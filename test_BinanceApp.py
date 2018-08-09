import binanceApp
from datetime import datetime
from lib import entitiesModule as entities 
kline1 = entities.KlineData(
    symbol = 'BTCUSDT',
    OpenTime= 1527480000000,
    OpenPrice = '7000.00000000',
    HighPrice = '7400.00000000',
    LowPrice = '7000.00000000',
    ClosePrice = '7400.00000000',
    Volume = '1763.2933430',
    CloseTime = 1527483599999,
    QuoteAssetVol = '12944855.34880205',
    NumberOfTrades = 15272,
)
kline2 = entities.KlineData(
    symbol = 'BTCUSDT',
    OpenTime= 1527483600000,
    OpenPrice = '7400.00000000',
    HighPrice = '7800.00000000',
    LowPrice = '7300.00000000',
    ClosePrice = '7800.00000000',
    Volume = '1763.2933430',
    CloseTime = 1527487199999,
    QuoteAssetVol = '12944855.34880205',
    NumberOfTrades = 15272,
)
kline3 = entities.KlineData(
    symbol = 'BTCUSDT',
    OpenTime= 1527487200000,
    OpenPrice = '7800.00000000', 
    HighPrice = '7500.00000000',
    LowPrice = '7300.00000000',
    ClosePrice = '7500.00000000', #low 7500 fall -300
    Volume = '1763.2933430',
    CloseTime = 1527490799999,
    QuoteAssetVol = '12944855.34880205',
    NumberOfTrades = 15272,
)
kline4 = entities.KlineData(
    symbol = 'BTCUSDT',
    OpenTime= 1527490800000,
    OpenPrice = '7500.00000000', 
    HighPrice = '7500.00000000',
    LowPrice = '6700.00000000',
    ClosePrice = '6800.00000000', #low -1000, fall -700
    Volume = '1763.2933430',
    CloseTime = 1527494399999,
    QuoteAssetVol = '12944855.34880205',
    NumberOfTrades = 15272,
)
kline5 = entities.KlineData(
    symbol = 'BTCUSDT',
    OpenTime= 1527494400000,
    OpenPrice = '6800.00000000', 
    HighPrice = '7100.00000000',
    LowPrice = '6800.00000000',
    ClosePrice = '7100.00000000', 
    Volume = '1763.2933430',
    CloseTime = 1527497999999,
    QuoteAssetVol = '12944855.34880205',
    NumberOfTrades = 15272,
)
kline6 = entities.KlineData(
    symbol = 'BTCUSDT',
    OpenTime= 1527498000000,
    OpenPrice = '7100.00000000', 
    HighPrice = '7100.00000000',
    LowPrice = '7100.00000000',
    ClosePrice = '7100.00000000', 
    Volume = '1763.2933430',
    CloseTime = 15275015999999,
    QuoteAssetVol = '12944855.34880205',
    NumberOfTrades = 15272,
)
kline7= entities.KlineData(
    symbol = 'BTCUSDT',
    OpenTime= 1527501600000,
    OpenPrice = '7100.00000000', 
    HighPrice = '8100.00000000',
    LowPrice = '7100.00000000',
    ClosePrice = '8000.00000000', 
    Volume = '1763.2933430',
    CloseTime = 1527501959999,
    QuoteAssetVol = '12944855.34880205',
    NumberOfTrades = 15272,
)


def test_IsFirstKline():
    priceMove = entities.PriceMove()
    result = priceMove.isFirstKline()
    expected = True
    assert expected == result 

def test_NotFirstKline():
    priceMove = entities.PriceMove()
    priceMove.addKline(kline1)
    result = priceMove.isFirstKline()
    expected = False
    assert expected == result

def test_PriceDiff():
    priceMove = entities.PriceMove()
    priceMove.addKline(kline1)
    priceMove.addKline(kline2)
    result = priceMove.priceDiff()
    expected = 800
    assert expected == result

def test_PriceDiffNegative():
    priceMove = entities.PriceMove()
    priceMove.addKline(kline3)
    priceMove.addKline(kline4)
    result = priceMove.priceDiff()
    expected = -1000
    assert expected == result

def test_PercentDiff():
    priceMove = entities.PriceMove()
    priceMove.addKline(kline1)
    priceMove.addKline(kline2)
    result = priceMove.percentDiff()
    expected = 11.43
    assert expected == float(result)

def test_PercentDiffNegative():
    priceMove = entities.PriceMove()
    priceMove.addKline(kline3)
    priceMove.addKline(kline4)
    result = priceMove.percentDiff()
    expected = -12.82
    assert expected == float(result)

def test_PriceDiffSeveral():
    priceMove = entities.PriceMove()
    priceMove.addKline(kline1)
    priceMove.addKline(kline2)
    priceMove.addKline(kline3)
    # priceMove.addKline(kline4)
    result = priceMove.priceDiff()
    expected = 800 # third kline is not added since its going in opposite direction
    assert expected == result

def test_SameDirection():
    priceMove = entities.PriceMove()
    priceMove.addKline(kline1)
    result = priceMove.klineIsSameDirection(kline2)
    expected = True
    assert expected == result

def test_NotSameDirection():
    priceMove = entities.PriceMove()
    priceMove.addKline(kline1)
    priceMove.addKline(kline2)
    result = priceMove.klineIsSameDirection(kline3)
    expected = False
    assert expected == result

# def test_NotSameDirTwice():
#     priceMove = entities.PriceMove()
#     priceMove.addKline(kline1)
#     priceMove.addKline(kline2)
#     priceMove.addKline(kline3)
#     result = priceMove.klineIsSameDirection(kline4) #Should be false since changes from positive
#     expected = False
#     assert expected == result
#     priceMove.addKline(kline4)
#     result = priceMove.klineIsSameDirection(kline5) #After kline4 the priceMove is overall negative
#     assert expected == result

def test_Impact():
    priceMove = entities.PriceMove()
    priceMove.addKline(kline1)
    result = priceMove.klineImpact(kline2)
    expected = 100
    assert expected == result

def test_NegativeImpact():
    priceMove = entities.PriceMove()
    priceMove.addKline(kline1)
    priceMove.addKline(kline2)
    result = priceMove.klineImpact(kline3)
    expected = -37.5
    assert expected == float(result)
def test_durationSecs():
    priceMove = entities.PriceMove()
    priceMove.addKline(kline1)
    priceMove.addKline(kline2)
    result = priceMove.durationSecs()
    # expected = datetime.timedelta(hours=1, minutes=59, seconds=59, milliseconds=999) #when returning datetime.timedelta
    expected = 60*60*2 # 2 hours
    assert expected == result
def test_durationHours():
    priceMove = entities.PriceMove()
    priceMove.addKline(kline1)
    priceMove.addKline(kline2)
    result = priceMove.durationHours()
    expected = 2
    assert expected == result
def test_overloadedPlusOperator():
    priceMove1 = entities.PriceMove()
    priceMove1.addKline(kline1)
    priceMove1.addKline(kline2)
    priceMove2 = entities.PriceMove()
    priceMove2.addKline(kline3)
    priceMove2.addKline(kline4)
    combined = priceMove1 + priceMove2
    result = combined.durationHours()
    expected = 4
    # assert expected == result
    assert combined.startPrice() == 7000
    assert combined.endPrice() == 6800
    assert datetime.fromtimestamp(1527480000000/1000) == combined.startTime()
    assert datetime.fromtimestamp(1527494399999/1000) == combined.endTime()
    assert combined.lowPrice() == 6700
    assert combined.highPrice() == 7800
def test_isPowerMove():
    priceMove = entities.PriceMove()
    priceMove.addKline(kline1)
    priceMove.addKline(kline2)
    result = priceMove.isPowerMove()
    expected = True
    assert expected == result

def test_notPowerMove():
    priceMove = entities.PriceMove()
    priceMove.addKline(kline5)
    priceMove.addKline(kline6)
    result = priceMove.isPowerMove()
    expected = False
    assert expected == result

def test_hoursAppart():
    priceMove1 = entities.PriceMove()
    priceMove2 = entities.PriceMove()
    priceMove1.addKline(kline1)
    priceMove2.addKline(kline3)
    result = priceMove2.hoursAppart(priceMove1)
    expected = 1
    assert expected == result

def test_isPowerRaise():
    priceMove1 = entities.PriceMove()
    priceMove1.addKline(kline5)
    priceMove1.addKline(kline6) 
    priceMove1.addKline(kline7) #Now its a powerraise
    assert priceMove1.startPrice() == 6800.0
    assert priceMove1.endPrice() == 8000.0
    assert priceMove1.percentDiff() > 10
    assert priceMove1.durationHours() < 5
    assert priceMove1.isPowerRaise() == True

def test_createBase():
    priceMove1 = entities.PriceMove()
    priceMove2 = entities.PriceMove()
    priceMove1.addKline(kline3)
    priceMove1.addKline(kline4) #Now its a powerdrop
    priceMove2.addKline(kline5)
    priceMove2.addKline(kline6) 
    priceMove2.addKline(kline7) #Now its a powerraise
    base = priceMove2.createBase(priceMove1)
    assert priceMove2.isPowerRaise() == True
    assert priceMove1.isPowerDrop() == True
    assert base != None




