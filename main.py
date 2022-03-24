from time import sleep
import os
import threading
import json
from websocket import create_connection


class prices:
    Running = 1

    class binance:
        BTC = 0
        ETH = 0

    class cryptoCom:
        BTC = 0
        ETH = 0


class URLs:
    class binance:
        BTC = "wss://stream.binance.com:9443/ws/btcusdt@trade"
        ETH = "wss://stream.binance.com:9443/ws/ethusdt@trade"

    class cryptoCom:
        BASE = "wss://stream.crypto.com/v2/market"

        reqBTC = "{\"method\": \"subscribe\", \"params\": { \"channels\": [\"trade.BTC_USDT\"] } }"
        reqETH = "{\"method\": \"subscribe\", \"params\": { \"channels\": [\"trade.ETH_USDT\"] } }"


def initConnection(url):
    webSockTemp = create_connection(url, timeout=5)
    sleep(0.5)
    print(" -Logged In- " + str(url))
    return webSockTemp


# !!!!!!!!!!!!!        USE        IF != None
def getPrice(a):
    result1 = json.loads(a.recv())
    try:
        return result1["p"]
    except KeyError:
        try:
            return result1["result"]["data"][0]['p']
        except KeyError:
            return


def getAll(a):
    result1 = json.loads(a.recv())
    return result1


def subscribeStream(socket, request):
    socket.send(request)
    sleep(1)
    getAll(socket)
    print("Subscribe Successful")


def workerThread(sock, optiune):
    print("Started Thread: " + str(optiune))
    if optiune == 1:
        while prices.Running == 1:
            temp = getPrice(sock)
            if temp != None:
                prices.binance.BTC = temp
    if optiune == 2:
        while prices.Running == 1:
            temp = getPrice(sock)
            if temp != None:
                prices.binance.ETH = temp
    if optiune == 3:
        while prices.Running == 1:
            temp = getPrice(sock)
            if temp != None:
                prices.cryptoCom.BTC = temp
    if optiune == 4:
        while prices.Running == 1:
            temp = getPrice(sock)
            if temp != None:
                prices.cryptoCom.ETH = temp
    sock.close()
    print("Stopped " + str(optiune))


sock1 = initConnection(URLs.binance.BTC)
sock2 = initConnection(URLs.binance.ETH)
sock3 = initConnection(URLs.cryptoCom.BASE)
sock4 = initConnection(URLs.cryptoCom.BASE)

subscribeStream(sock3, URLs.cryptoCom.reqBTC)
subscribeStream(sock4, URLs.cryptoCom.reqETH)

thread1 = threading.Thread(target=workerThread, args=(sock1, 1,))
thread2 = threading.Thread(target=workerThread, args=(sock2, 2,))
thread3 = threading.Thread(target=workerThread, args=(sock3, 3,))
thread4 = threading.Thread(target=workerThread, args=(sock4, 4,))

thread1.start()
thread2.start()
thread3.start()
thread4.start()

sleep(5)

while True:
    bBTC = float(prices.binance.BTC)
    bETH = float(prices.binance.ETH)
    cBTC = float(prices.cryptoCom.BTC)
    cETH = float(prices.cryptoCom.ETH)

    diffBTC = bBTC - cBTC
    precBTC = diffBTC / bBTC * 100

    diffETH = bETH - cETH
    precETH = diffETH / bETH * 100

    print(str(bBTC) + " " + str(bBTC - cBTC) + " " + str(cBTC))

prices.Running = 0

sleep(5)
