import json
from datetime import datetime, timedelta

# Load transactions from a file (if it exists) when the program starts
def load_transactions():
    try:
        with open('transactions.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save transactions to a file
def save_transactions(transactions):
    with open('transactions.json', 'w') as file:
        json.dump(transactions, file)

# Calculate the current balance based on the transactions
def calculate_balance(transactions):
    balance = 0
    for transaction in transactions:
        if transaction['type'] == 'deposit':
            balance += transaction['amount']
        elif transaction['type'] == 'withdrawal':
            balance -= transaction['amount']
    return balance

# Function to add a transaction
def add_transaction(transactions):
    print("What type of transaction do you want to add? (deposit/withdrawal)")
    transaction_type = input().strip().lower()
    
    if transaction_type not in ['deposit', 'withdrawal']:
        print("Invalid transaction type. Please enter 'deposit' or 'withdrawal'.")
        return transactions
    
    print("Enter the amount:")
    try:
        amount = float(input().strip())
        if amount <= 0:
            print("Amount must be greater than zero.")
            return transactions
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return transactions
    
    # Add the transaction with the current date
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    transactions.append({
        'type': transaction_type,
        'amount': amount,
        'date': current_date
    })
    
    # Save the updated transactions list
    save_transactions(transactions)
    
    print(f"Transaction of {transaction_type} of {amount} added.")
    return transactions

# Function to view all transactions
def view_transactions(transactions):
    if not transactions:
        print("No transactions available.")
        return
    
    for index, transaction in enumerate(transactions, start=1):
        print(f"{index}. {transaction['type']} of {transaction['amount']} on {transaction['date']}")

# Function to filter transactions based on date
def filter_transactions_by_date(transactions, time_period):
    today = datetime.now()
    
    if time_period == 'today':
        start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
    elif time_period == 'week':
        start_date = today - timedelta(days=today.weekday())  # Start of the current week (Monday)
    elif time_period == 'month':
        start_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)  # Start of the current month
    else:
        return []
    
    filtered_transactions = []
    for transaction in transactions:
        transaction_date = datetime.strptime(transaction['date'], '%Y-%m-%d %H:%M:%S')
        if transaction_date >= start_date:
            filtered_transactions.append(transaction)
    
    return filtered_transactions

# Function to generate a report based on time period
def generate_report(transactions, time_period):
    filtered_transactions = filter_transactions_by_date(transactions, time_period)
    total_spent = sum(t['amount'] for t in filtered_transactions if t['type'] == 'withdrawal')
    
    print(f"Total amount spent {time_period}: {total_spent}")
    
# Main function to run the application
def main():
    transactions = load_transactions()
    
    while True:
        print("\nMain Menu:")
        print("1. Add a transaction")
        print("2. View all transactions")
        print("3. View current balance")
        print("4. Detailed report")
        print("5. Exit")
        
        choice = input("Enter your choice: ").strip()
        
        match choice:
            case '1':
                transactions = add_transaction(transactions)
            case '2':
                 view_transactions(transactions)
            case '3':
                balance = calculate_balance(transactions)
                print(f"Your current balance is: {balance}")
            case '4':
                print("\nDetailed Report Menu:")
                print("1. Total spent today")
                print("2. Total spent this week")
                print("3. Total spent this month")
                print("4. Back to main menu")
            
                report_choice = input("Enter your choice: ").strip()
                match report_choice: 
                    case '1':
                        generate_report(transactions, 'today')
                    case '2':
                        generate_report(transactions, 'week')
                    case '3':
                        generate_report(transactions, 'month')
                    case '4':
                        continue
                    case _:
                        print("Invalid choice. Please try again.")
            case '5':
                print("Exiting application...")
                break
            case _:
                print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")

if __name__ == "__main__":
    main()
