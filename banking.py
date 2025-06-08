import csv
import os
from typing import List, Dict, Optional

class BankAccount:
    def __init__(self, account_id: str, name: str, balance: float = 0.0):
        self.account_id = account_id
        self.name = name
        self.balance = balance

    def deposit(self, amount: float) -> bool:
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount: float) -> bool:
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def __str__(self):
        return f"Account(ID: {self.account_id}, Name: {self.name}, Balance: ${self.balance:.2f})"


class BankingSystem:
    def __init__(self):
        self.accounts: Dict[str, BankAccount] = {}

    def create_account(self, name: str, initial_balance: float = 0.0) -> BankAccount:
        account_id = str(len(self.accounts) + 1)
        account = BankAccount(account_id, name, initial_balance)
        self.accounts[account_id] = account
        return account

    def get_account(self, account_id: str) -> Optional[BankAccount]:
        return self.accounts.get(account_id)

    def deposit(self, account_id: str, amount: float) -> bool:
        account = self.get_account(account_id)
        if account:
            return account.deposit(amount)
        return False

    def withdraw(self, account_id: str, amount: float) -> bool:
        account = self.get_account(account_id)
        if account:
            return account.withdraw(amount)
        return False

    def transfer(self, from_account_id: str, to_account_id: str, amount: float) -> bool:
        from_account = self.get_account(from_account_id)
        to_account = self.get_account(to_account_id)

        if not from_account or not to_account:
            return False

        if from_account.withdraw(amount):
            return to_account.deposit(amount)
        return False

    def save_to_csv(self, filename: str = "bank_data.csv") -> bool:
        try:
            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["account_id", "name", "balance"])
                for account in self.accounts.values():
                    writer.writerow([account.account_id, account.name, account.balance])
            return True
        except Exception as e:
            print(f"Error saving to CSV: {e}")
            return False

    def load_from_csv(self, filename: str = "bank_data.csv") -> bool:
        if not os.path.exists(filename):
            return False

        try:
            with open(filename, mode='r') as file:
                reader = csv.DictReader(file)
                self.accounts.clear()
                for row in reader:
                    account_id = row["account_id"]
                    name = row["name"]
                    balance = float(row["balance"])
                    self.accounts[account_id] = BankAccount(account_id, name, balance)
            return True
        except Exception as e:
            print(f"Error loading from CSV: {e}")
            return False

    def __str__(self):
        return "\n".join(str(account) for account in self.accounts.values())