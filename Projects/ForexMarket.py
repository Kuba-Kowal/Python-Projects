from random import randint, uniform
from sys import exit
from time import sleep
from os import system

currencyPairs = { 
                "EURUSD": 1.111,
                "GBPJPY": 2.222,
                "AUDCAD": 0.949,
                "NZDUSD": 0.675,
                "USDCHF": 0.892,
                "USDCAD": 1.345,
                "GBPUSD": 1.307,
                "EURGBP": 0.853,
                "AUDJPY": 78.45,
                "EURAUD": 1.590,
                "NZDCAD": 0.911,
                "AUDNZD": 1.065,
                }
holdings = {}
accountBalance = 10000
startBalance = accountBalance
positionType = ""

# Determine current market value of a currency pair
def marketValue(currencyPair: str) -> dict:
    return round(currencyPairs[(currencyPair)], 6)

# Update the market value of a currency pair 
def marketChange(currencyPair: str) -> dict:
    randomSelection = randint(1,2)
    marketChange = uniform(0.001, 0.003)
    if randomSelection == 1:
        currencyPairs[currencyPair] = (currencyPairs[(currencyPair)] + marketChange)
        return round(currencyPairs[(currencyPair)], 6)
    else:
        currencyPairs[currencyPair] = (currencyPairs[(currencyPair)] - marketChange)
        return round(currencyPairs[(currencyPair)], 6)
    
# View account balance
def viewBalance() -> str:
    lots = accountBalance * 0.01
    return f"""
#############################
# Account Balance: {round(accountBalance, 3)} 
# Lots available:  {round(lots, 3)}
# Total Profit:    {round(accountBalance - startBalance, 3)}
#############################"""

# Buy currency pair
def buyMarket(currencyPair: str) -> dict: 
    global accountBalance
    global holdings
    global currencyPairValues
    global buyAmount
    buyAmount = float(input("How many lots would you like to invest into this trade > "))
    if buyAmount * 100 > accountBalance:
        return "\nUnable to process transaction. Not enough funds."
    accountBalance -= buyAmount * 100
    holdings[currencyPair] = currencyPairs[(currencyPair)]
    holdings["lots"] = buyAmount

    return f"\nentered trade for {buyAmount} lots at position {marketValue(currencyPair)}"

# Sell currency pair
def closePosition(currencyPair, tradeType: str) -> dict: 
    global accountBalance
    global holdings
    global currencyPairs
    global buyAmount
    if tradeType == "buy":
        takeProfit = round((marketValue(currencyPair) - holdings[(currencyPair)]) * 10 * (100 * holdings[("lots")]), 3)
        if takeProfit > 0:
            accountBalance += ((buyAmount * 100) * takeProfit)
        else:
            accountBalance -= ((buyAmount * 100) * (takeProfit * -1))
        holdings[currencyPair] = currencyPairs[(currencyPair)]

    elif tradeType == "sell":
        takeProfit = round((holdings[(currencyPair)] - marketValue(currencyPair)) * 10 * (100 * holdings[("lots")]), 3)
        if takeProfit > 0:
            accountBalance += ((buyAmount * 100) * takeProfit)
        else:
            accountBalance -= ((buyAmount * 100) * (takeProfit * -1))
        holdings[currencyPair] = currencyPairs[(currencyPair)]

    return f"\nPosition closed at position {marketValue(currencyPair)}, TP/TL: {takeProfit}"

# Make Trades
def main():
    global accountBalance
    global startBalance
    global tradeType
    currencyChoice = ""
    tradeType = ""
    system("cls")

    while accountBalance > 0:
        try:
            print("""
╔═══════════════════╗
║ 1. View Balance   ║   888    d8P  888     888 888888b.          d8888       88888888888 8888888b.         d8888 8888888b.  8888888888 8888888b.  
║ 2. View Market    ║   888   d8P   888     888 888  "88b        d88888           888     888   Y88b       d88888 888  "Y88b 888        888   Y88b 
║ 3. Buy            ║   888  d8P    888     888 888  .88P       d88P888           888     888    888      d88P888 888    888 888        888    888 
║ 4. Sell           ║   888d88K     888     888 8888888K.      d88P 888           888     888   d88P     d88P 888 888    888 8888888    888   d88P 
║ 5. Close Position ║   8888888b    888     888 888  "Y88b    d88P  888           888     8888888P"     d88P  888 888    888 888        8888888P"  
║ 6. View Holdings  ║   888  Y88b   888     888 888    888   d88P   888           888     888 T88b     d88P   888 888    888 888        888 T88b   
║ q. Exit           ║   888   Y88b  Y88b. .d88P 888   d88P  d8888888888           888     888  T88b   d8888888888 888  .d88P 888        888  T88b  
╚═╦═════════════════╝   888    Y88b  "Y88888P"  8888888P"  d88P     888           888     888   T88b d88P     888 8888888P"  8888888888 888   T88b         
  ║
""", end="")
            
            menuSelection = input("  ╚═══════════ What would you like to do > ")
            if menuSelection == "1":
                system("cls")
                print(viewBalance())
                print("\npress [enter] to go back", end="")
                input()
                system("cls")

            elif menuSelection == "2":
                system("cls")
                for key, value in currencyPairs.items():
                    print(f"{key} - {value}")
                print("\npress [enter] to go back", end="")
                input()
                system("cls")

            elif menuSelection == "3":
                system("cls")
                if holdings == {}:
                    while True:
                        for key, value in currencyPairs.items():
                            print(f"{key} - {value}")
                        currencyChoice = input("\nWhat currency pair would you like to trade ([Enter] to go back.)> ")
                        if currencyChoice in currencyPairs.keys():
                            print(buyMarket(currencyChoice))
                            tradeType = "buy"
                            for _ in range (1, 5):
                                marketChange(currencyChoice)
                            sleep(6)
                            system("cls")
                            break
                        elif currencyChoice == "":
                            system("cls")
                            break
                        else:
                            print("\nNot a valid currency pair.")
                            sleep(1)
                            system("cls")
                else:
                    print("\nIn the current version only one currency pair can be traded at a time.")
                    sleep(2)
                    system("cls")

            elif menuSelection == "4":
                if holdings == {}:
                    system("cls")
                    while True:
                        for key, value in currencyPairs.items():
                            print(f"{key} - {value}")
                        currencyChoice = input("\nWhat currency pair would you like to trade ([Enter] to go back.)> ")
                        if currencyChoice in currencyPairs.keys():
                            print(buyMarket(currencyChoice))
                            tradeType = "sell"
                            for _ in range (1, 5):
                                marketChange(currencyChoice)
                            sleep(3)
                            system("cls")
                            break
                        elif currencyChoice == "":
                            system("cls")
                            break
                        else:
                            print("\nNot a valid currency pair.")
                            sleep(1)
                            system("cls")
                else:
                    print("\nIn the current version only one currency pair can be traded at a time.")
                    sleep(2)
                    system("cls")

            elif menuSelection == "5":
                if currencyChoice in currencyPairs.keys():
                    print(closePosition(currencyChoice, tradeType))
                    sleep(2)
                    system("cls")
                else:
                    print("\nNo valid trade available to be closed.")
                    sleep(2)
                    system("cls")
            elif menuSelection == "6":
                if holdings != {}:
                    system("cls")
                    for key, value in holdings.items():
                        print(f"{key} | Value: {value} | ", end="")
                        
                    print("\nPress [Enter] to go back.")
                    input()
                    system("cls")
                else:
                    print("\nNo Holdings.")
                    sleep(2)
                    system("cls")
            elif menuSelection.lower() == "q":
                print("\nHit any key to exit...")
                input()
                exit()
            else:
                print("\nInvalid option.")
                sleep(2)
                system("cls")

        except KeyboardInterrupt:
            print("\nHit any key to exit...")
            input()
            exit()

    print("\nYou ran out of money. Please re-deposit.")
    sleep(3)
    exit()

main()