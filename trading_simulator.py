import random
import json
import os
import requests

def get_real_bitcoin_price():
    url = "https://api.coinbase.com/v2/prices/BTC-EUR/spot"
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()
    return float(data["data"]["amount"])

cash = 1000
bitcoin = 0
price = 50000

average_price = 50000
market_trend = 0
day = 0
trading_fee = 0.0025

starting_balance = 1000
history = []
price_history = [50000]

if os.path.exists("save.json"):
    with open("save.json", "r") as file:
        data = json.load(file)

    cash = data["cash"]
    bitcoin = data["bitcoin"]
    price = data["price"]
    day = data["day"]
    market_trend = data["market_trend"]
    history = data["history"]
    price_history = data["price_history"]

    print("Save loaded.")

else:
    print("New game started.")

while True:
    print("1. Show portfolio")
    print("2. Buy Bitcoin")
    print("3. Sell Bitcoin")
    print("4. Load Bitcoin price")
    print("5. Show Profit/Loss")
    print("6. Transaction History")
    print("7. Exit")
    print("8. Next Day")
    print("9. Show Price History")
    print("10. Delete Save")
    print("11. Simulate Multiple Days")
    print("12. Show Statistics")
    print("13. Reset Game")

    choice = input("Choose an option: ")

    if choice == "1":
        total_value = cash + bitcoin * price
        print(f"\nCash: €{cash}")
        print(f"Bitcoin: {bitcoin:.3f}")
        print(f"Bitcoin price: €{price}")
        print(f"Total portfolio value: €{total_value}")

    elif choice == "2":
        amount = float(input("How many euros do you want to spend? ").replace(",", "."))

        if amount > cash:
            print("You do not have enough cash.")
        else:
            fee = amount * trading_fee
            amount_after_fee = amount - fee

            bitcoin_bought = amount_after_fee / price
            bitcoin += bitcoin_bought
            cash -= amount

            print(f"Fee paid: €{fee:.2f}")
            print(f"You bought {bitcoin_bought:.3f} BTC.")

    elif choice == "3":
        amount = float(input("How much Bitcoin do you want to sell? ").replace(",", "."))

        if amount > bitcoin:
            print("You do not have enough Bitcoin.")
        else:
            sale_value = amount * price
            fee = sale_value * trading_fee

            cash += sale_value - fee
            bitcoin -= amount

            history.append(f"SELL {amount:.6f} BTC at €{price}")

            print(f"Fee paid: €{fee:.2f}")
            print(f"You sold {amount:.3f} BTC.")

    elif choice == "4":
            price = get_real_bitcoin_price()
            price_history.append(price)

            print(f"Real Bitcoin price loaded: €{price:.2f}")

    elif choice == "5":
        current_value = cash + bitcoin * price
        profit = current_value - starting_balance
        return_percentage = (profit / starting_balance) * 100

        print(f"\nStarting balance: €{starting_balance}")
        print(f"Current portfolio value: €{current_value:.2f}")
        print(f"Profit/Loss: €{profit:.2f}")
        print(f"Return: {return_percentage:.2f}%")
        
    elif choice == "6":
        print("\nTransaction History")

        if len(history) == 0:
            print("No transactions yet.")
        else:
            for transaction in history:
                print(transaction)

    elif choice == "7":
        data = {
            "cash": cash,
            "bitcoin": bitcoin,
            "price": price,
            "day": day,
            "market_trend": market_trend,
            "history": history,
            "price_history": price_history
        }

        with open("save.json", "w") as file:
            json.dump(data, file)

        print("Game saved.")
        print("Goodbye.")
        break

    elif choice == "8":
        day += 1

        # Trend verandert langzaam
        market_trend = market_trend * 0.99 + random.uniform(-0.001, 0.001)

        # Volatiliteit: normale dagelijkse schommeling
        volatility = 0.025

        change = market_trend + random.uniform(-volatility, volatility)

        price = price * (1 + change)

        # Voorkom negatieve of extreem lage prijs
        price = max(1000, price)

        price_history.append(price)

        print(f"\nDay {day}")
        print(f"New Bitcoin price: €{price:.2f}")
        print(f"Market trend: {market_trend:.2%}")
        print(f"Daily change: {change:.2%}")

    elif choice == "9":
        print("\nPrice History")

        for i, p in enumerate(price_history):
            print(f"Day {i}: €{p:.2f}")

    elif choice == "10":
        if os.path.exists("save.json"):
            os.remove("save.json")
            print("Save deleted.")

        else:
            print("No save found.")

    elif choice == "11":
        days_to_simulate = int(input("How many days? "))

        for _ in range(days_to_simulate):
            day += 1

            market_trend = market_trend * 0.99 + random.uniform(-0.001, 0.001)

            volatility = 0.025

            change = market_trend + random.uniform(-volatility, volatility)

            price = price * (1 + change)

            price = max(1000, price)

            price_history.append(price)

        print(f"Simulated {days_to_simulate} days.")
        print(f"Current day: {day}")
        print(f"Current price: €{price:.2f}")

    elif choice == "12":
        average = sum(price_history) / len(price_history)

        print("\n=== Statistics ===")
        print(f"Current day: {day}")
        print(f"Current BTC price: €{price:.2f}")
        print(f"Highest price: €{max(price_history):.2f}")
        print(f"Lowest price: €{min(price_history):.2f}")
        print(f"Average price: €{average:.2f}")
        print(f"Recorded prices: {len(price_history)}")
        print(f"Transactions: {len(history)}")

    elif choice == "13":
        cash = 1000
        bitcoin = 0
        price = 50000
        day = 0
        market_trend = 0

        history = []
        price_history = [50000]

        if os.path.exists("save.json"):
            os.remove("save.json")

        print("Game reset.")

    else:
        print("Invalid option.")