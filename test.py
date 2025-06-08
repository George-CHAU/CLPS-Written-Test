from banking import BankingSystem

bank = BankingSystem()
account1 = bank.create_account("Alice", 1000.0)
account2 = bank.create_account("Bob", 500.0)

bank.deposit(account1.account_id, 200.0)
bank.withdraw(account2.account_id, 100.0)
bank.transfer(account1.account_id, account2.account_id, 300.0)

bank.save_to_csv()  