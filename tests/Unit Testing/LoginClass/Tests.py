import os
import unittest
import sqlite3
import uuid
from tkinter import Tk
from unittest.mock import patch
from login import LoginSystem, CryptoManagerClass


class TestLoginSystem(unittest.TestCase):

    def setUp(self):
        # Create a test database and setup necessary test data
        self.test_db = 'test.db'
        with sqlite3.connect(self.test_db) as con:
            con.execute("DELETE FROM employee")  # Delete any existing rows
            con.execute("CREATE TABLE IF NOT EXISTS employee (eid TEXT PRIMARY KEY, name TEXT, email TEXT, pass TEXT)")
            con.execute("INSERT INTO employee (eid, name, email, pass) VALUES (?, ?, ?, ?)",
                        (str(uuid.uuid4()), 'Jane Doe', 'jane.doe@test.com',
                         CryptoManagerClass().encrypt_data('valid_password')))

    def tearDown(self):
        # Remove the test database
        if self.test_db:
            os.remove(self.test_db)

    @patch('login.LoginSystem.send_email')
    def test_forget_password_success(self, mock_send_email):
        mock_send_email.return_value = 's'  # Simulate successful email sending

        root = Tk()  # Create a Tkinter root window
        login_system = LoginSystem(root)  # Initialize your LoginSystem (assuming you need a root window)

        # Call and initiate the password reset process
        login_system.employee_id.set('1001')
        login_system.forget_window()

        # Simulate entering the correct OTP generated within the send_email function
        login_system.var_otp.set('123456')
        login_system.validate_otp()

        # Simulate updating the password
        login_system.var_new_pass.set('new_strong_password')
        login_system.var_conf_pass.set('new_strong_password')
        login_system.update_password()

        # Assert the password was changed
        with sqlite3.connect(self.test_db) as con:
            cur = con.cursor()
            cur.execute("SELECT pass FROM employee WHERE eid='1001'")
            encrypted_password = cur.fetchone()[0]
            decrypted_password = CryptoManagerClass().decrypt_data(encrypted_password)
            self.assertEqual(decrypted_password, 'new_strong_password')

    def test_login_success(self):
        login_system = LoginSystem(...)  # Initialize your LoginSystem

        login_system.employee_id.set('1001')
        login_system.password.set('valid_password')
        login_system.login()

        # Replace this with assertions based on how your program indicates successful login
        self.assertTrue(login_system.logged_in)  # Assuming you have a 'logged_in' flag somewhere

    def test_login_failure_invalid_password(self):
        login_system = LoginSystem(...)

        login_system.employee_id.set('1001')
        login_system.password.set('incorrect_password')
        login_system.login()

        # Assert login failed
        self.assertFalse(login_system.logged_in)  # Assuming you have a 'logged_in' flag

    # ... Add more tests for check_admin_user, create_admin_window, etc.
    # ... Be sure to test encryption/decryption within the relevant tests


if __name__ == '__main__':
    unittest.main()
