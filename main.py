# TODO-1 Make necessary imports
from imagecodecs import NoneError
from time import sleep
from menu import MENU

ON = True

resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}

actions = {
    "buy": 0,
    "refill": 1,
    "report": 2,
    "exit": 3
}

# TODO-2 Add a function that reports the quantity of ingredients
def report():
    print("Your resources are:\n")
    print(f"Water: {resources['water']} mL")
    print(f"Milk: {resources['milk']} mL")
    print(f"Coffee: {resources['coffee']} mL")


# TODO-3 Add the function that fills the ingredients with a predetermined quantity
def fill(water_q: int, milk_q: int, coffee_q: int):
    resources["water"] += water_q
    resources["milk"] += milk_q
    resources["coffee"] += coffee_q
    report()


# TODO-4 Add a function that lets the user choose how much of each ingredient is added to the machine and then fill it
def fill_quantity():
    water_q = int(input("How many mL of water do you wish to add to the machine? "))
    milk_q = int(input("How many mL of milk do you wish to add to the machine? "))
    coffee_q = int(input("How many mL of coffee do you wish to add to the machine? "))
    if any([water_q < 0, milk_q < 0, coffee_q < 0]):   # Evaluates if any of the fill quantities is negative
        print("Cannot fill resources with negative volumes.")
    else:
        fill(water_q, milk_q, coffee_q)


# TODO-12 Add a function that uses the resources
def use_resources(beverage):
    for ingredient in MENU[beverage]["ingredients"]:
        resources[ingredient] -= MENU[beverage]["ingredients"][ingredient]


# TODO-5 Add function to check if there are enough resources for the chosen beverage
def check_resources(beverage: str):
    enough = True
    for resource in MENU[beverage]["ingredients"]:
        if MENU[beverage]["ingredients"][resource] > resources[resource]:
            enough = False

    if not enough:
        print(f"There aren't enough resources for {beverage}.")
        report()
        print("You need:")
        for resource in MENU[beverage]["ingredients"]:
            print(f"{resource}: {MENU[beverage]['ingredients'][resource]} mL")
    return enough


# TODO-6 Add a function that takes money and returns the sum amount
def count_money(balance):
    penny_q = int(input("How many dimes? "))
    nickel_q = int(input("How many nickels? "))
    dime_q = int(input("How many pennies? "))
    quarter_q = int(input("How many quarters? "))
    balance += 1 * penny_q + 5 * nickel_q + 10 * dime_q + 50 * quarter_q
    print(f"Your balance is ${float(balance)/100}")   # If decimal number formatting is required, use {float(balance)/100:.2f}
    return balance


# TODO-7 Add a function that compares the balance to the beverage price and tells if it is enough or not
def is_balance_enough(beverage: str, balance: int):
    enough = True
    cost = MENU[beverage]["cost"]
    if balance/100 < cost:
        enough = False
    return enough


# TODO-8 Add a function that checks whether a valid beverage has been picked
def beverage_exists(beverage: str):
    if beverage not in MENU:
        raise NoneError
    else:
        pass


# TODO-9 Add a function that validates the selected beverage
def select_beverage():
    beverage = input("Please choose beverage: (espresso/latte/cappuccino) ").lower()
    try:
        beverage_exists(beverage)
        return beverage
    except NoneError:
        print("Invalid selection.")
        select_beverage()


# TODO-10 Add a function that lets the user select the action do make and validates it
def initiate_action():
    action = input("Please choose action: (buy/refill/report) ").lower()
    try:
        if action in actions:
            return actions[action]
        else: raise NoneError
    except NoneError:
        print("Invalid action.")
        initiate_action()


# TODO-11 Add a function that brews the beverage
def brew(beverage):
    if beverage == "espresso":
        print("Brewing your espresso ☕")
        use_resources(beverage)
    elif beverage == "latte":
        use_resources(beverage)
        print("Brewing your latte 🍵")
    else:
        use_resources(beverage)
        print("Brewing your cappuccino 🥤")

    print("brrrrrrrrrrrr~~~~~~")
    sleep(4)
    print("Done!")



selected_action = 0
selected_beverage = ""
final_balance = 0
still_want_beverage = True

while ON:
    selected_action = initiate_action()
    if selected_action == 0:
        selected_beverage = select_beverage()

        if check_resources(selected_beverage):
            final_balance = count_money(final_balance)

            while still_want_beverage:
                if is_balance_enough(selected_beverage, final_balance):
                    brew(selected_beverage)
                    final_balance -= MENU[selected_beverage]["cost"]
                    print(f"Your balance is {final_balance}")
                    still_want_beverage = False

                else:
                    print(f"There isn't enough money for a {selected_beverage}. Your balance is ${final_balance/100}. The {selected_beverage} costs ${MENU[selected_beverage]['cost']}")
                    money_choice = input("Do you want to add more money? Type [y] for yes or [n] for no: ").lower()
                    if money_choice == "y":
                        final_balance = count_money(final_balance)
                    else:
                        print("Take your money back please.")
                        final_balance = 0
                        still_want_beverage = False

    elif selected_action == 1:
        fill_quantity()
    elif selected_action == 2:
        report()
    elif selected_action == 3:
        ON = False

