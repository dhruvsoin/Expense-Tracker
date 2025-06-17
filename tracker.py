import csv
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

FILENAME = "expenses.csv"

def add_expense():
    date = input("Enter date (YYYY-MM-DD): ")
    category = input("Enter category (e.g., Food, Transport, etc.): ")
    amount = input("Enter amount: ")
    description = input("Enter description (optional): ")

    with open(FILENAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, description])
    print("Expense added successfully.\n")

def view_summary():
    try:
        df = pd.read_csv(FILENAME, names=["Date", "Category", "Amount", "Description"])
        df["Amount"] = pd.to_numeric(df["Amount"], errors='coerce')
        df["Date"] = pd.to_datetime(df["Date"], errors='coerce')

        if df.empty or df["Amount"].isnull().all():
            print("No valid expense data found.\n")
            return

        print("\n--- Expense Summary by Category ---")
        print(df.groupby("Category")["Amount"].sum())

        print("\n--- Monthly Total Expenses ---")
        df["Month"] = df["Date"].dt.to_period("M")
        print(df.groupby("Month")["Amount"].sum())

        print("\n")
    except FileNotFoundError:
        print("No expenses recorded yet.\n")

def show_graph():
    try:
        df = pd.read_csv(FILENAME, names=["Date", "Category", "Amount", "Description"])
        df["Amount"] = pd.to_numeric(df["Amount"], errors='coerce')
        df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
        df["Month"] = df["Date"].dt.to_period("M").astype(str)

        if df.empty or df["Amount"].isnull().all():
            print("No valid data to plot.\n")
            return

        monthly_expenses = df.groupby("Month")["Amount"].sum()

        plt.figure(figsize=(10, 5))
        monthly_expenses.plot(kind='line', marker='o')
        plt.title("Monthly Expense Graph")
        plt.xlabel("Month")
        plt.ylabel("Total Amount Spent")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("screenshot-graph.png")
        plt.show()
    except FileNotFoundError:
        print("Expense file not found.\n")

def main():
    while True:
        print("========== Personal Expense Tracker ==========")
        print("1. Add New Expense")
        print("2. View Expense Summary")
        print("3. Show Expense Graph")
        print("4. Exit")
        choice = input("Enter your choice (1–4): ")

        if choice == '1':
            add_expense()
        elif choice == '2':
            view_summary()
        elif choice == '3':
            show_graph()
        elif choice == '4':
            print("Exiting the Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.\n")

if __name__ == "__main__":
    main()
