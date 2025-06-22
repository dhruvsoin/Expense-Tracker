import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

FILE_NAME = "expenses.csv"

def manage_expenses():
    if not os.path.exists(FILE_NAME):
        df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
    else:
        df = pd.read_csv(FILE_NAME)

    while True:
        print("\nWhat would you like to do?")
        print("1. Add Expense")
        print("2. Edit Expense")
        print("3. Delete Expense")
        print("4. View Current Expenses")
        print("5. Go Back to Main Menu")

        choice = input("Enter your choice (1–5): ")

        if choice == '1':
            # Add
            date = input("Enter the date (YYYY-MM-DD): ")
            category = input("Enter the category (e.g., Food, Rent): ")
            amount = float(input("Enter the amount: "))
            description = input("Enter a description (optional): ")

            new_expense = pd.DataFrame({
                "Date": [date],
                "Category": [category],
                "Amount": [amount],
                "Description": [description]
            })

            df = pd.concat([df, new_expense], ignore_index=True)
            print("Expense added.")

        elif choice == '2':
            # Edit
            if df.empty:
                print("No expenses to edit.")
                continue

            print("Current Expenses:")
            df_with_id = df.reset_index()
            print(df_with_id.to_string(index=False))
            try:
                idx = int(input("Enter the ID of the expense to edit: "))
                if idx in df_with_id['index'].values:
                    date = input("Enter the new date (YYYY-MM-DD): ")
                    category = input("Enter the new category: ")
                    amount = float(input("Enter the new amount: "))
                    description = input("Enter the new description (optional): ")

                    df.loc[idx] = [date, category, amount, description]
                    print("Expense updated.")
                else:
                    print("Invalid ID.")
            except ValueError:
                print("Please enter a valid number.")

        elif choice == '3':
            # Delete
            if df.empty:
                print("No expenses to delete.")
                continue

            print("Current Expenses:")
            df_with_id = df.reset_index()
            print(df_with_id.to_string(index=False))
            try:
                idx = int(input("Enter the ID of the expense to delete: "))
                if idx in df_with_id['index'].values:
                    df = df.drop(index=idx).reset_index(drop=True)
                    print("Expense deleted.")
                else:
                    print("Invalid ID.")
            except ValueError:
                print("Please enter a valid number.")

        elif choice == '4':
            if df.empty:
                print("No expenses recorded yet.")
            else:
                print("\nCurrent Expenses:")
                print(df.reset_index().to_string(index=False))

        elif choice == '5':
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

        # Save after every change
        df.to_csv(FILE_NAME, index=False)


def show_summary():
    if not os.path.exists(FILE_NAME):
        print("No expenses recorded yet.")
        return

    df = pd.read_csv(FILE_NAME)
    if df.empty:
        print("No expenses recorded yet.")
        return

    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])

    df['Month'] = df['Date'].dt.to_period("M")
    summary = df.groupby(['Month', 'Category'])['Amount'].sum().unstack().fillna(0)

    print("\nExpense Summary (Monthly Breakdown):")
    print(summary.round(2))


def show_graphs():
    if not os.path.exists(FILE_NAME):
        print("No expenses recorded yet.")
        return

    df = pd.read_csv(FILE_NAME)
    if df.empty:
        print("No expenses recorded yet.")
        return

    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])

    # Line graph - Monthly expenses
    df['Month'] = df['Date'].dt.to_period("M")
    monthly_summary = df.groupby('Month')['Amount'].sum()

    plt.figure(figsize=(12, 5))

    # Line Chart
    plt.subplot(1, 2, 1)
    monthly_summary.plot(kind='line', marker='o', title='Monthly Expenses')
    plt.xlabel("Month")
    plt.ylabel("Amount")
    plt.grid(True)

    # Pie Chart
    plt.subplot(1, 2, 2)
    category_totals = df.groupby('Category')['Amount'].sum()
    category_totals.plot(kind='pie', autopct='%1.1f%%', startangle=90)
    plt.title("Category-wise Spending")
    plt.ylabel("")

    plt.tight_layout()
    plt.show()


def main():
    while True:
        print("\n--- Personal Expense Tracker ---")
        print("1. Manage Expenses (Add/Edit/Delete)")
        print("2. View Expense Summary")
        print("3. View Expense Graphs (Monthly + Category)")
        print("4. Exit")

        choice = input("Enter your choice (1–4): ")

        if choice == '1':
            manage_expenses()
        elif choice == '2':
            show_summary()
        elif choice == '3':
            show_graphs()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
