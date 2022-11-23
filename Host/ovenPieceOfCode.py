import time, sys
from fhict_cb_01.CustomPymata4 import CustomPymata4
from datetime import datetime
import app

pinRedLed,pinGreenLed,pinBlueLed,pinYellowLed=4,5,6,7
pinLedList=[pinRedLed,pinGreenLed,pinBlueLed,pinYellowLed]
pinBuzzer=3

pizzaList = []
orderToTry = []

timeMagherita = 10
timePepperoni = 8
timeProsciutto = 9
timeQuattro = 6
timeStar = 14
timeNino = 12
timeMarinara = 9
timeBurger = 10
timeExotic = 9
totalTime = 0

busyCooking = False

def setup():
    global board
    board = CustomPymata4(com_port = "COM4")
    board.displayOn()

setup()

for i in range(3,8):
    board.set_pin_mode_digital_output(i)

    def pizzaCooking(Pizza):
        if Pizza=="Margherita":
            remainingTime=timeMagherita
        elif Pizza=="Pepperoni":
            remainingTime=timePepperoni
        elif Pizza=="Prosciutto E Funghi":
            remainingTime=timeProsciutto
        elif Pizza=="Quattro Stagioni":
            remainingTime=timeQuattro
        elif Pizza=="Star Carlos":
            remainingTime=timeStar
        elif Pizza=="Nino Bellisimo":
            remainingTime=timeNino
        elif Pizza=="Marinara":
            remainingTime=timeMarinara
        elif Pizza=="Luigi's Burger Pizza":
            remainingTime=timeBurger
        elif Pizza=="Luigi's Exotic Pizza":
            remainingTime=timeExotic
        ovenWork(remainingTime)

def checkTime():
    global totalTime
    totalTime = 0

    length = len(orderToTry[0])

    for i in range(length):
        #print(orderToTry[0][i])
    
        if orderToTry[0][i]=="Margherita":
            totalTime= totalTime + timeMagherita
        if orderToTry[0][i]=="Pepperoni":
            totalTime= totalTime + timePepperoni
        if orderToTry[0][i]=="Prosciutto E Funghi":
            totalTime= totalTime + timeProsciutto
        if orderToTry[0][i]=="Quattro Stagioni":
            totalTime= totalTime + timeQuattro
        if orderToTry[0][i]=="Star Carlos":
            totalTime= totalTime + timeStar
        if orderToTry[0][i]=="Nino Bellisimo":
            totalTime= totalTime + timeNino
        if orderToTry[0][i]=="Marinara":
            totalTime= totalTime + timeMarinara
        if orderToTry[0][i]=="Luigi's Burger Pizza":
            totalTime= totalTime + timeBurger
        if orderToTry[0][i]=="Luigi's Exotic Pizza":
            totalTime= totalTime + timeExotic
    app.receiveTime(totalTime)
    #print(totalTime)

def ovenWork(remainingTime):
    for pinLed in pinLedList:
        board.digital_write(pinLed, 1)
    for i in range(remainingTime):
        board.displayShow(remainingTime-i)
        if (remainingTime-i)<3*remainingTime/4:
            board.digital_write(pinYellowLed, 0)
        if (remainingTime-i)<remainingTime/2:
            board.digital_write(pinBlueLed, 0)
        if (remainingTime-i)<remainingTime/4:
            board.digital_write(pinGreenLed, 0)
        time.sleep(1)
    board.digital_write(pinRedLed, 0)
    board.displayShow(0)
    for i in range(3):
        for k in range(2):
            board.digital_write(pinGreenLed, 1)
            board.digital_write(pinBuzzer,1)
            time.sleep(0.1)
            board.digital_write(pinGreenLed, 0)
            board.digital_write(pinBuzzer,0)
            time.sleep(0.2)
        time.sleep(2)
    

def preparation(orderList):
    #print(orderList)
    if orderList==[]:
        print("No order for now")
        #check for more pizzas
    else:
        nextOrder=orderList[0]
        #print(orderList[0])
        for numPizza in range(0,len(nextOrder)):
            #print(numPizza)
            pizza=(nextOrder[numPizza])
            pizzaCooking(pizza)
            time.sleep(5)
            #print(pizza)
        del orderList[0]
        app.removeOrders()
        #print(orderList)
        preparation(orderToTry)

def siteStuff(value):
    global busyCooking


    orderToTry.append(value[0])
    #print(orderToTry)
    #print(orderToTry[0])
    #print(orderToTry[0][0])

    checkTime()

    if busyCooking == False:
        busyCooking = True
        preparation(orderToTry)
    else:
        print("Order added, can't cook now")
    
    #for i in orderToTry:
     #   print(i)