import requests
import os 
import json
import time

expense_file = "expense.json"

def load_expense(expense_file):
    if os.path.exists(expense_file):
        with open(expense_file,"r") as file :
            return json.load(file)

def save_expense(expense_file):
    with open(expense_file,"w") as file:
        json.dump(expense,file,indent=5)

def add_expense(expense_file):
    expense=load_expense()
    new_expense={
        "ID" : len(expense)+1,
        "description" : description,
        "category":"",
        "time":time.ctime(time.time())
        "amount":amount,
    }
