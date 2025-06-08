import unittest
import os
from banking import BankingSystem, BankAccount


class TestBankingSystem(unittest.TestCase):
    def setUp(self):
        self.bank = BankingSystem()
        self.test_file = "test_bank_data.csv"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_create_account(self):
        account = self.bank.create_account("John Doe", 100.0)
        self.assertEqual(account.name, "John Doe")
        self.assertEqual(account.balance, 100.0)
        self.assertEqual(account.account_id, "1")

    def test_deposit(self):
        account = self.bank.create_account("John Doe")
        self.assertTrue(self.bank.deposit(account.account_id, 50.0))
        self.assertEqual(account.balance, 50.0)
        self.assertFalse(self.bank.deposit(account.account_id, -10.0))
        self.assertEqual(account.balance, 50.0)

    def test_withdraw(self):
        account = self.bank.create_account("John Doe", 100.0)
        self.assertTrue(self.bank.withdraw(account.account_id, 50.0))
        self.assertEqual(account.balance, 50.0)
        self.assertFalse(self.bank.withdraw(account.account_id, 60.0))
        self.assertEqual(account.balance, 50.0)
        self.assertFalse(self.bank.withdraw(account.account_id, -10.0))
        self.assertEqual(account.balance, 50.0)

    def test_transfer(self):
        account1 = self.bank.create_account("John Doe", 100.0)
        account2 = self.bank.create_account("Jane Smith", 50.0)

        self.assertTrue(self.bank.transfer(account1.account_id, account2.account_id, 30.0))
        self.assertEqual(account1.balance, 70.0)
        self.assertEqual(account2.balance, 80.0)

        self.assertFalse(self.bank.transfer(account1.account_id, account2.account_id, 80.0))
        self.assertEqual(account1.balance, 70.0)
        self.assertEqual(account2.balance, 80.0)

        self.assertFalse(self.bank.transfer("nonexistent", account2.account_id, 10.0))
        self.assertFalse(self.bank.transfer(account1.account_id, "nonexistent", 10.0))

    def test_save_and_load(self):
        account1 = self.bank.create_account("John Doe", 100.0)
        account2 = self.bank.create_account("Jane Smith", 50.0)

        self.assertTrue(self.bank.save_to_csv(self.test_file))

        new_bank = BankingSystem()
        self.assertTrue(new_bank.load_from_csv(self.test_file))

        loaded_account1 = new_bank.get_account(account1.account_id)
        loaded_account2 = new_bank.get_account(account2.account_id)

        self.assertEqual(loaded_account1.name, account1.name)
        self.assertEqual(loaded_account1.balance, account1.balance)
        self.assertEqual(loaded_account2.name, account2.name)
        self.assertEqual(loaded_account2.balance, account2.balance)

    def test_load_nonexistent_file(self):
        new_bank = BankingSystem()
        self.assertFalse(new_bank.load_from_csv("nonexistent_file.csv"))


if __name__ == "__main__":
    unittest.main()