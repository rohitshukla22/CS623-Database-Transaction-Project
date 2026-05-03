import psycopg2
from typing import List, Tuple

# ==========================================
# DATABASE CONNECTION SETUP
# ==========================================
DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5433"
}

# ==========================================
# TRANSACTION DEFINITIONS
# ==========================================
TRANSACTIONS = {
    1: {
        "name": "Delete Product p1",
        "description": "The product p1 is deleted from Product and Stock.",
        "queries": [
            "DELETE FROM Product WHERE prod = 'p1';"
        ]
    },
    2: {
        "name": "Delete Depot d1",
        "description": "The depot d1 is deleted from Depot and Stock.",
        "queries": [
            "DELETE FROM Depot WHERE dep = 'd1';"
        ]
    },
    3: {
        "name": "Rename Product p1 to pp1",
        "description": "The product p1 changes its name to pp1 in Product and Stock.",
        "queries": [
            "UPDATE Product SET prod = 'pp1' WHERE prod = 'p1';",
            "SELECT * FROM Product;"
        ]
    },
    4: {
        "name": "Rename Depot d1 to dd1",
        "description": "The depot d1 changes its name to dd1 in Depot and Stock.",
        "queries": [
            "UPDATE Depot SET dep = 'dd1' WHERE dep = 'd1';"
        ]
    },
    5: {
        "name": "Add new Product and Stock",
        "description": "We add a product (p100, cd, 5) in Product and (p100, d2, 50) in Stock.",
        "queries": [
            "INSERT INTO Product (prod, pname, price) VALUES ('p100', 'cd', 5);",
            "INSERT INTO Stock (prod, dep, quantity) VALUES ('p100', 'd2', 50);"
        ]
    },
    6: {
        "name": "Add new Depot and Stock",
        "description": "We add a depot (d100, Chicago, 100) in Depot and (p1, d100, 100) in Stock.",
        "queries": [
            "INSERT INTO Depot (dep, addr, volume) VALUES ('d100', 'Chicago', 100);",
            "INSERT INTO Stock (prod, dep, quantity) VALUES ('p1', 'd100', 100);"
        ]
    }
}

# ==========================================
# USER INTERFACE FUNCTIONS
# ==========================================

def print_header():
    """Print application header"""
    print("\n" + "="*60)
    print("  DATABASE TRANSACTION EXECUTION SYSTEM")
    print("="*60 + "\n")

def get_user_name() -> str:
    """Get user name from available options"""
    print("Please select a user:")
    print("-" * 40)
    print("1. Rohit Shukla")
    print("2. Tae Kown")
    print("-" * 40)
    
    while True:
        choice = input("\nEnter your choice (1 or 2): ").strip()
        if choice == "1":
            return "Rohit Shukla"
        elif choice == "2":
            return "Tae Kown"
        else:
            print("Invalid choice. Please enter 1 or 2.")

def display_transactions():
    """Display all available transactions"""
    print("\n" + "="*60)
    print("AVAILABLE TRANSACTIONS")
    print("="*60 + "\n")
    
    for trans_id, details in TRANSACTIONS.items():
        print(f"Transaction {trans_id}: {details['name']}")
        print(f"   Description: {details['description']}")
        print()

def get_user_selections() -> List[int]:
    """Get 2 transaction selections from user"""
    selected = []
    print("\n" + "="*60)
    print("SELECT YOUR TRANSACTIONS")
    print("="*60)
    print("\nYou must select exactly 2 transactions to execute.\n")
    
    for selection_num in range(1, 3):
        while True:
            try:
                choice = input(f"Enter transaction number for selection {selection_num} (1-6): ").strip()
                trans_id = int(choice)
                
                if trans_id not in TRANSACTIONS:
                    print("Invalid transaction number. Please enter a number between 1 and 6.")
                    continue
                
                if trans_id in selected:
                    print("You already selected this transaction. Please choose a different one.")
                    continue
                
                selected.append(trans_id)
                print(f"✓ Selected: Transaction {trans_id} - {TRANSACTIONS[trans_id]['name']}\n")
                break
                
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 6.")
    
    return selected

def confirm_selections(user_name: str, selected_trans: List[int]) -> bool:
    """Display selected transactions and ask for confirmation"""
    print("\n" + "="*60)
    print("TRANSACTION SUMMARY")
    print("="*60)
    print(f"\nUser: {user_name}")
    print(f"Selected Transactions:\n")
    
    for idx, trans_id in enumerate(selected_trans, 1):
        print(f"  {idx}. Transaction {trans_id}: {TRANSACTIONS[trans_id]['name']}")
        print(f"     {TRANSACTIONS[trans_id]['description']}\n")
    
    while True:
        confirm = input("Do you want to execute these transactions? (yes/no): ").strip().lower()
        if confirm in ["yes", "y"]:
            return True
        elif confirm in ["no", "n"]:
            return False
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def execute_selected_transactions(user_name: str, selected_trans: List[int]):
    """Execute the selected transactions"""
    try:
        # Establish the connection
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        print("\n" + "="*60)
        print("EXECUTION LOG")
        print("="*60)
        print(f"\nConnected to PostgreSQL successfully.")
        print(f"User: {user_name}")
        print(f"Executing {len(selected_trans)} transaction(s)...\n")

        execution_results = []

        for trans_id in selected_trans:
            transaction = TRANSACTIONS[trans_id]
            print(f"\n--- Transaction {trans_id}: {transaction['name']} ---")
            
            try:
                print(f"Description: {transaction['description']}")
                print("Executing queries:")
                
                for query in transaction['queries']:
                    print(f"  ► {query}")
                    cur.execute(query)
                
                conn.commit()
                print(f"✓ Transaction {trans_id} Committed Successfully.\n")
                execution_results.append((trans_id, True, None))
                
            except Exception as e:
                conn.rollback()
                error_msg = f"Transaction {trans_id} Failed (Rolled Back): {e}"
                print(f"✗ {error_msg}\n")
                execution_results.append((trans_id, False, str(e)))

        # Print execution summary
        print("\n" + "="*60)
        print("EXECUTION SUMMARY")
        print("="*60)
        print(f"\nUser: {user_name}\n")
        
        success_count = 0
        for trans_id, success, error in execution_results:
            status = "✓ SUCCESS" if success else "✗ FAILED"
            print(f"Transaction {trans_id}: {TRANSACTIONS[trans_id]['name']} - {status}")
            if error:
                print(f"  Error: {error}")
            success_count += 1 if success else 0
        
        print(f"\nTotal: {success_count}/{len(selected_trans)} transactions executed successfully.\n")

    except Exception as connection_error:
        print(f"✗ Database connection failed: {connection_error}")
    
    finally:
        # Clean up connections
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()
            print("="*60)
            print("Database connection closed.")
            print("="*60 + "\n")

def main():
    """Main program flow"""
    print_header()
    
    # Get user name
    user_name = get_user_name()
    print(f"\n✓ Welcome, {user_name}!\n")
    
    # Display all transactions
    display_transactions()
    
    # Get user selections
    selected_transactions = get_user_selections()
    
    # Confirm selections
    if confirm_selections(user_name, selected_transactions):
        # Execute selected transactions
        execute_selected_transactions(user_name, selected_transactions)
    else:
        print("\n✗ Execution cancelled. No transactions were executed.\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Program interrupted by user.\n")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}\n")