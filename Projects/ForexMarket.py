# Jakub Kowalczyk @ York College
# V2 | + Trade History | + Time Simulation

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
tradeHistory = []
accountBalance = 10000.000
startBalance = accountBalance
positionType = ""

# Determine current market value of a currency pair
def marketValue(currencyPair: str) -> dict:
    return round(currencyPairs[(currencyPair)], 6)

# Update the market value of a currency pair 
def marketChange(currencyPair: str, Repetitions: int) -> dict:
    for _ in range(1, Repetitions):
        randomSelection = randint(1,2)
        marketChange = uniform(0.001, 0.003)
        if randomSelection == 1:
            currencyPairs[currencyPair] = (currencyPairs[(currencyPair)] + marketChange)
        else:
            currencyPairs[currencyPair] = (currencyPairs[(currencyPair)] - marketChange)

    return round(currencyPairs[(currencyPair)], 6)
    
# View account balance
def viewBalance() -> str:
    lots = accountBalance * 0.01
    return f"""
╔════════════════════════════╗
║ Account Balance: {round(accountBalance, 3)}   
║ Lots available:  {round(lots, 3)}   
║ Total Profit:    {round(accountBalance - startBalance, 3)}      
╚════════════════════════════╝"""

# Buy currency pair
def buyMarket(currencyPair: str) -> dict: 
    global accountBalance
    global holdings
    global buyAmount

    # Type Check
    while True:
        try:
            buyAmount = float(input("\nHow many lots would you like to invest into this trade > "))
            break
        except ValueError:
            print("\nMake sure you input a number")

    # Ensure user has enough money inside their balance
    if buyAmount * 100 > accountBalance:
        return "\nUnable to process transaction. Not enough funds."
    # Remove funds from balance and add trade to wallet.
    accountBalance -= buyAmount * 100
    holdings[currencyPair] = currencyPairs[(currencyPair)]
    holdings["lots"] = buyAmount

    return f"\nentered trade for {buyAmount} lots at position {marketValue(currencyPair)}"

# Sell currency pair
def closePosition(currencyPair: str, tradeType: str) -> dict: 
    global accountBalance
    global holdings
    global currencyPairs
    global buyAmount

    # Determine the trade type
    if tradeType == "buy":
        # Calculate profit in pips for buy position
        pipsGained = round((marketValue(currencyPair) - holdings[currencyPair]), 3)
        lots = holdings["lots"]
        
        # If profit (pips gained) is positive, add to the balance, otherwise subtract
        if pipsGained > 0:
            accountBalance += ((pipsGained * lots * 100) + (buyAmount * 100))
        else:
            accountBalance += ((pipsGained * lots * 100) + (buyAmount * 100))  # pipsGained is already negative for a loss
        
        # Update holdings to reflect the latest market value (position is closed)
        tradeHistory.append(f"{currencyPair}     | [{round(pipsGained * lots * 100, 3)}]")
        del holdings[currencyPair]
        del holdings["lots"]

    elif tradeType == "sell":
        # Calculate profit in pips for sell position
        pipsGained = round((holdings[currencyPair] - marketValue(currencyPair)), 3)
        lots = holdings["lots"]
        
        # If profit (pips gained) is positive, add to the balance, otherwise subtract
        if pipsGained > 0:
            accountBalance -= ((pipsGained * lots * 100) + (buyAmount * 100))
        else:
            accountBalance -= ((pipsGained * lots * 100) + (buyAmount * 100))  # pipsGained is already negative for a loss
        
        # Update holdings to reflect the latest market value (position is closed)
        tradeHistory.append(f"{currencyPair}     | [{round(pipsGained * lots * 100, 3)}]")
        del holdings[currencyPair]
        del holdings["lots"]

    return f"\nPosition closed at position {marketValue(currencyPair)}, TP/TL: {pipsGained * lots * 100}"

# Make Trades
def main():
    global accountBalance
    global tradeType

    currencyChoice = ""
    tradeType = ""
    system("cls")

    while accountBalance > 0:
        try:
            print("""
╔═══════════════════╗
║ 1. View Balance   ║   888    d8P  888     888 888888b.          d8888       88888888888 8888888b.         d8888 8888888b.  8888888888 8888888b.     `8.`888b        ,8' 88888888888888 
║ 2. View Market    ║   888   d8P   888     888 888  "88b        d88888           888     888   Y88b       d88888 888  "Y88b 888        888   Y88b     `8.`888b      ,8'  88888888888888
║ 3. Buy            ║   888  d8P    888     888 888  .88P       d88P888           888     888    888      d88P888 888    888 888        888    888      `8.`888b    ,8'      888  888
║ 4. Sell           ║   888d88K     888     888 8888888K.      d88P 888           888     888   d88P     d88P 888 888    888 8888888    888   d88P       `8.`888b  ,8'       888  888
║ 5. Close Position ║   8888888b    888     888 888  "Y88b    d88P  888           888     8888888P"     d88P  888 888    888 888        8888888P"         `8.`888b,8'        888  888
║ 6. View Holdings  ║   888  Y88b   888     888 888    888   d88P   888           888     888 T88b     d88P   888 888    888 888        888 T88b           `8.`8888'         888  888
║ 7. Trade History  ║   888   Y88b  Y88b. .d88P 888   d88P  d8888888888           888     888  T88b   d8888888888 888  .d88P 888        888  T88b           `8.`88'       88888888888888
║ 8. Time Sim       ║   888    Y88b  "Y88888P"  8888888P"  d88P     888           888     888   T88b d88P     888 8888888P"  8888888888 888   T88b           `8..'        88888888888888                 
╚═╦═════════════════╝
  ║ q. exit
""", end="")
            
            # Menu selection
            menuSelection = input("  ╚═══════════ What would you like to do > ")
            if menuSelection == "1":
                system("cls")
                print(viewBalance())
                print("\npress [enter] to go back", end="")
                input()
                system("cls")

            elif menuSelection == "2":
                system("cls")
                for key in currencyPairs.keys():
                    marketChange(key, 3)
                for key, value in currencyPairs.items():
                    print(f"{key} - {round(value, 3)}")
                print("\npress [enter] to go back", end="")
                input()
                system("cls")

            elif menuSelection == "3":
                system("cls")
                if holdings == {}:
                    while True:
                        # Outputs all the currency pairs available to trade
                        for key, value in currencyPairs.items():
                            print(f"{key} - {round(value, 3)}")
                        currencyChoice = input("\nWhat currency pair would you like to trade ([Enter] to go back.)> ")
                        if currencyChoice in currencyPairs.keys():
                            print(buyMarket(currencyChoice))
                            tradeType = "buy"
                            marketChange(currencyChoice, 5)
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
                        # Outputs all currency pairs
                        for key, value in currencyPairs.items():
                            print(f"{key} - {round(value, 3)}")
                        currencyChoice = input("\nWhat currency pair would you like to trade ([Enter] to go back.)> ")
                        if currencyChoice in currencyPairs.keys():
                            print(buyMarket(currencyChoice))
                            tradeType = "sell"
                            marketChange(currencyChoice, 5)
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
                    tradeType = ""
                    currencyChoice = ""
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
                        print(f"{key} | Value: {round(value, 3)} | ", end="")
                        
                    print("\nPress [Enter] to go back.")
                    input()
                    system("cls")
                else:
                    print("\nNo Holdings.")
                    sleep(2)
                    system("cls")

            elif menuSelection == "7":
                system("cls")
                if tradeHistory != []:
                    print("CURRENCY PAIR - TP/TL\n═══════════════════")
                    for trade in tradeHistory:
                        print(f"   {trade}")
                else:
                    print("\nHistory is empty.")
                print("\nPress [Enter] to go back.", end="")
                input()
                system("cls")

            elif menuSelection == "8":
                while True:
                    system("cls")
                    print("""
    ╔═════════════════╗
    ║ 1 - 5 Minutes   ║
    ║ 2 - 15 Minutes  ║
    ║ 3 - 30 Minutes  ║
    ║ 4 - 1 Hour      ║
    ║ 5 - 2 Hours     ║
    ║ 6 - 4 Hours     ║
    ║ 7 - 12 Hours    ║
    ║ 8 - 24 Hours    ║
    ╚═╦═══════════════╝""")
                    menuSelection = input("      ╚═══════════ What would you like to do [Enter] to go back > ")
                    match menuSelection:
                        case "1":
                            for key in currencyPairs.keys():
                                marketChange(key, 5)
                            print("\nPassing 5 Minutes...")
                            sleep(3)
                        case "2":
                            for key in currencyPairs.keys():
                                marketChange(key, 15)
                            print("\nPassing 15 Minutes...")
                            sleep(3)
                        case "3":
                            for key in currencyPairs.keys():
                                marketChange(key, 30)
                            print("\nPassing 30 Minutes...")
                            sleep(3)    
                        case "4":
                            for key in currencyPairs.keys():
                                marketChange(key, 60)
                            print("\nPassing 1 Hour...")
                            sleep(3)
                        case "5":
                            for key in currencyPairs.keys():
                                marketChange(key, 120)
                            print("\nPassing 2 Hours...")
                            sleep(3)
                        case "6":
                            for key in currencyPairs.keys():
                                marketChange(key, 240)
                            print("\nPassing 4 Hours...")
                            sleep(3)
                        case "7":
                            for key in currencyPairs.keys():
                                marketChange(key, 720)
                            print("\nPassing 12 Hours...")
                            sleep(3)
                        case "8":
                            for key in currencyPairs.keys():
                                marketChange(key, 1440)
                            print("\nPassing 24 Hours...")
                            sleep(3)
                        case "":
                            system("cls")
                            break
                        case _:
                            print("\nInvalid Input")

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
