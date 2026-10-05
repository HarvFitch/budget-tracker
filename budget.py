import json

ALLOWED_CATEGORIES = ["food","vehicle","house","utilities","leisure"]
DATA_FILE = "expenditure_data.json"
expenses = []
budget = 0

class Expenditure:
    def __init__(self, category, cost, itemType):
        self.category = category
        self.cost = cost
        self.itemType = itemType

    
def show_summary(expenses, budget, allowed_categories):
    total = 0

    while True:
        breakdown = input("Would you like a full breakdown of your expenditure? (yes/no)").lower()
        if (breakdown == "yes"):
            advanced_summary(expenses)
            break
        elif (breakdown == "no"):
            for expense in expenses:
                total += expense.cost
            print(f"Monthly Budget: £{budget:.2f}")
            print(f"Total expenditure: £{total:.2f}")
            difference = budget - total
            print(f"You have £{difference:.2f} left of your monthly budget")

            #budget breakdown
            for category in allowed_categories:
                category_total = 0
                for expense in expenses:
                    if expense.category == category:
                        category_total += expense.cost
                if(category_total >0):
                    print(f"{category}: £{category_total:.2f}")
            return
        else: 
            print("That is not an option, please review the options")

def advanced_summary(expenses):
    for eachCategory in ALLOWED_CATEGORIES:
        itemCount = 0
        categoryItems = []
        for expense in expenses:
            if expense.category == eachCategory:
                itemCount += 1
                categoryItems.append(f"{expense.itemType}~ £{expense.cost}")
        if itemCount > 0:
            print(f"\n{eachCategory}:")
            for item in categoryItems:
                print(item)       
        
def checkMax(expenses, newExpense, budget):
    total = 0
    for expense in expenses:
        total += expense.cost
    difference = budget - total

    if difference  - newExpense >= 0:
        return True
    else:
        return False

def inputBudget():
    while True:
        try:
            user = float(input("What is your budget? "))
        except ValueError:
            print("You must enter a number!")
        else:
            if(user <=0 ):
                print("Budget cannot be 0")
            else:
                budget = user
                return budget

def addSpending(expenses, budget, allowed_categories):
        itemAdded = False
        while not itemAdded:
            try:
                spending = float(input("Enter expenditure: "))
            except ValueError:
                print("you must enter a number!")
            else:
                if checkMax(expenses, spending, budget):
                    while True:
                        specificItem = input("Enter the name of the expense: ")
                        spendingType = input("Enter the expenditure type (pick from either food, vehicle, house, utilities or leisure)").lower()
                        if(spendingType in allowed_categories):
                            new_expense = Expenditure(spendingType, spending, specificItem)
                            expenses.append(new_expense)
                            itemAdded = True
                            break
                        else:
                            print("Invalid category, choose from the provided options!")
                else:
                    print("Budget Exceded!!")

def fileSave(expenses, budget):
    expenseDictionary = {
        "budget":budget,
        "expenses": []
    }

    for expense in expenses:
        tempdict = {"category": expense.category, "item": expense.itemType, "cost": expense.cost}
        expenseDictionary["expenses"].append(tempdict)

    with open(DATA_FILE, "w") as f:
        json.dump(expenseDictionary, f, indent=4)

def fileOpen(expenses, budget):
    while True:
        previousUser = input("Do you have a saved file? (yes/no)").lower()
        if(previousUser == "yes"):
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                budget = data["budget"]
                expenses = []
                for items in data["expenses"]:
                    new_obj = Expenditure(items["category"], items["cost"], items["item"])
                    expenses.append(new_obj)
                return budget, expenses
        
        elif (previousUser == "no"):
            budget = inputBudget()
            return budget, []
        else:
            print("That's not an option, please check optiions! ")

budget, expenses = fileOpen(budget, expenses)

while True:
    options = input("Would you like to add to or view your monthly expenditure (type add or view), else, type quit: ").lower()
    if(options == "quit"):
        fileSave(expenses, budget)
        break
    elif(options == "add"):
        addSpending(expenses, budget, ALLOWED_CATEGORIES)

    elif(options == "view"):
        show_summary(expenses, budget, ALLOWED_CATEGORIES)

    else:
        print("That is not an option, please review the options")
print("Welldone for tracking your expenditure!")