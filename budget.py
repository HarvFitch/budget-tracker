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

    for expense in expenses:
        total += expense.cost
    #budget breakdown
    category_breakdown = {}
    for category in allowed_categories:
        category_total = 0
        for expense in expenses:
            if expense.category == category:
                category_total += expense.cost
        if(category_total >0):
            category_breakdown[category] = category_total

    summary_dict = {
        "monthly budget": budget,
        "total expenditure": total,
        "remaining budget": budget - total,
        "category breakdown": category_breakdown
    }
    return summary_dict
        
def checkMax(expenses, newExpense, budget):
    total = 0
    for expense in expenses:
        total += expense.cost
    difference = budget - total

    if difference  - newExpense >= 0:
        return True
    else:
        return False

def inputBudget(new_budget_value):

    if(new_budget_value <= 0):
        raise ValueError("Budget cannot be zero")

    budget = new_budget_value 
    return budget

def addSpending(expenses, budget, allowed_categories, spending, specificItem, spendingType): 
        if not checkMax(expenses, spending, budget):
            raise ValueError("Budget Exceeded")
    
        if(spendingType not in allowed_categories):
            raise ValueError(f"Invalid expenditure type. Must be one of: {allowed_categories}")

        new_expense = Expenditure(spendingType, spending, specificItem)
        expenses.append(new_expense)
        return{"success": True, "message": "Item added succesfully"}
                
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
        return {"status": "sucess", "message": "file saved"}

def fileOpen(expenses, budget):
    try: 
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            budget = data["budget"]
            expenses = []
            for items in data["expenses"]:
                new_obj = Expenditure(items["category"], items["cost"], items["item"])
                expenses.append(new_obj)
            return{
                "budget": budget,
                "expenses": expenses
            }
    except FileNotFoundError:
        return {"budget": 0.0, "expenses": []}
