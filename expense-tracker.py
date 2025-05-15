from tabulate import tabulate
import os 
import json
import time
import argparse
from datetime import datetime


expense_file = "expense.json"

def load_expense():
    if os.path.exists(expense_file):
        with open(expense_file,"r") as file :
            return json.load(file)
    return []

def save_expense(expense):
    with open(expense_file,"w") as file:
        json.dump(expense,file,indent=5)

def add_expense(description,amount):
    expense=load_expense()
    new_expense={
        "ID" : len(expense)+1,
        "description" : description,
        #"category":"",
        "added_time":time.ctime(time.time()),
        "amount":amount
    }
    print(f"Expense added successfully (ID: {new_expense['ID']})")
    expense.append(new_expense)
    save_expense(expense)

def update_expense(ID,new_description,new_amount):
    expense = load_expense()
    for exp in expense:
        if exp["ID"] == ID:
            exp["description"] = new_description
            exp["amount"] = new_amount
            #exp["updated_time"] == time.ctime(time.time())
            print(f"Expense updated successfully (ID: {ID})")
    save_expense(expense)

def delete_expense(ID):
    expense = load_expense()
    expense = [exp for exp in expense if exp["ID"]!= ID]
    save_expense(expense)
    print(f"Expense deleted sucessfully (ID: {ID}) ")

def view_expense():
    expense=load_expense()
    expense_data = []
    for exp in expense:
        expense_data.append([
            exp.get("ID","N/A"),
            exp.get("added_time","N/A"),
            exp.get("description","N/A"),
            exp.get("amount","N/A")
        ])
    headers=["ID","Date","Description","Amount"]

    print(tabulate(expense_data,headers=headers,tablefmt="plain"))

def summary_of_expense(month=None):
    expense = load_expense()
    if month != None:
        expense= [exp for exp in expense if (datetime.strptime(exp["added_time"],"%a %b %d %H:%M:%S %Y")).strftime("%B") == month]
        total = sum((exp["amount"]) for exp in expense)
        print(f"Total expenses for {month}: ${total}")
    
    else:
        total = sum((exp["amount"]) for exp in expense)
        print(f"Total expenses : ${total}")


def main():
    parser = argparse.ArgumentParser(description="Expense Tracker")
    subparsers= parser.add_subparsers(dest="command")

    parser_add = subparsers.add_parser("add", help="Add a new expense")
    parser_add.add_argument("--description",type=str,required=True,help="Description of the Expense")
    parser_add.add_argument("--amount",type=int,required=True,help="Amount of the Expenditure")

    parser_add = subparsers.add_parser("update", help="Update a existing expense")
    parser_add.add_argument("--ID",type=int,required=True,help="ID of the expense")
    parser_add.add_argument("--description",type=str,required = True,help="Desciption of the expense")
    parser_add.add_argument("--amount",type=str,required=True,help="Amount of the expenditure")
    
    parser_add = subparsers.add_parser("delete", help="Delete a existing expense")
    parser_add.add_argument("--ID",type=int,required=True,help="ID of the expense")

    parser_add = subparsers.add_parser("list", help="List  all expense ")
    

    parser_add = subparsers.add_parser("summary", help="Total of all the expenses or filter by month")
    parser_add.add_argument("--month",type=str,required = False,help="Filter expense my that month")
    
    args = parser.parse_args()

    if args.command == "add":
        add_expense(args.description,args.amount)
    if args.command == "update":
        update_expense(args.ID,args.description,args.amount)
    if args.command == "delete":
        delete_expense(args.ID)
    if args.command == "list":
        view_expense()
    if args.command == "summary":
        summary_of_expense(args.month)

    
if __name__ == "__main__":
    main()