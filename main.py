"""
Personal Finance Tracking CLI-APP
OOP, CSV
Made By Arsh

"""

import os
import csv
from datetime import date

HEADER_DATA = ["TYPE", "DATE", "DESCRIPTION", "AMOUNT"]
FILENAME = "database.csv"


class Transaction:
    def __init__(self, date: str, description: str, type: str, amount: int):
        self.date = date
        self.description = description
        self.type = type
        self.amount = amount

    def get_list(self):
        return [self.type, self.date, self.description, self.amount]


class DataStorage:
    def __init__(self, filename=FILENAME):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(HEADER_DATA)

    def save_transaction(self, transaction: Transaction):
        with open(self.filename, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(transaction.get_list())
        print("Transaction saved successfully.")

    def show_all(self):
        with open(self.filename, "r") as f:
            reader = csv.reader(f)
            next(reader)
            rows = [row for row in reader if row]

        if not rows:
            print("No transactions found.")
            return

        print("\nTRANSACTIONS\n")
        print(f"{'TYPE':<8} {'DATE':<12} {'DESCRIPTION':<20} {'AMOUNT':>10}")
        print("-" * 54)
        for row in rows:
            print(f"{row[0]:<8} {row[1]:<12} {row[2]:<20} {'₹' + row[3]:>10}")

    def show_statistics(self):
        debit = 0
        credit = 0

        with open(self.filename, "r") as f:
            reader = csv.reader(f)
            next(reader)
            rows = [row for row in reader if row]

        if not rows:
            print("No data available.")
            return

        for row in rows:
            amount = int(row[3])
            if row[0] == "D":
                debit += amount
            elif row[0] == "C":
                credit += amount

        print("\nSTATISTICS\n")
        print(f"{'Credit'}: {'₹' + str(credit)}")
        print(f"{'Debit'}: {'₹' + str(debit)}")
        print(f"{'Balance'}: {'₹' + str(credit - debit)}")


def get_transaction_input(type: str) -> Transaction:
    description = input("Enter description: ").strip()
    while not description:
        print("Description cannot be empty.")
        description = input("Enter description: ").strip()

    while True:
        try:
            amount = int(input("Enter amount: ₹").strip())
            if amount <= 0:
                print("Amount must be a positive number.")
            else:
                break
        except ValueError:
            print("Invalid amount. Please enter a whole number.")

    return Transaction(
        date=str(date.today()),
        description=description,
        type=type,
        amount=amount,
    )


def menu():
    print("\nPersonal Finance Tracker\n")
    options = [
        (1, "Add Credit"),
        (2, "Add Debit"),
        (3, "Show All Transactions"),
        (4, "Show Statistics"),
        (5, "Exit"),
    ]
    for code, command in options:
        print(f"{code} {command}")


def main():
    storage = DataStorage()

    while True:
        menu()
        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            t = get_transaction_input("C")
            storage.save_transaction(t)
        elif choice == "2":
            t = get_transaction_input("D")
            storage.save_transaction(t)
        elif choice == "3":
            storage.show_all()
        elif choice == "4":
            storage.show_statistics()
        elif choice == "5":
            print("\nThank you for using Personal Finance Tracker.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
