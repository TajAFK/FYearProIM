import unittest
from unittest.mock import patch, MagicMock
from tkinter import Tk, PhotoImage
from billing import BillClass

class TestBillClassExceptionHandling(unittest.TestCase):
    def setUp(self):
        """Set up a Tkinter root window and the BillClass instance."""
        self.root = Tk()
        self.root.withdraw()  # Hide the Tkinter GUI since we are not testing GUI components

    def tearDown(self):
        """Destroy the Tkinter root window after each test."""
        self.root.destroy()

    @patch('billing.PhotoImage', return_value=MagicMock(spec=PhotoImage))
    def test_init(self, mock_photoimage):
        """Test that the BillClass initializes correctly with mocked PhotoImage."""
        bill = BillClass(self.root)
        self.assertIsInstance(bill, BillClass)

    @patch('billing.BillClass.save_bill_to_database')
    def test_save_bill_database_error(self, mock_save_bill):
        """Test if errors during saving a bill to the database are handled."""
        # Configure the mock to raise an Exception when trying to save a bill
        mock_save_bill.side_effect = Exception("Database save failed")

        # Set necessary variables to simulate a ready-to-save state
        self.bill.var_cname.set("John Doe")
        self.bill.var_contact.set("123456789")
        self.bill.cart_list = [['1', 'Product', '10.00', '2', '20']]

        # Attempt to generate a bill, expecting an exception due to the mocked save error
        with self.assertRaises(Exception):
            self.bill.generate_bill()

    @patch('billing.BillClass.bill_top')
    def test_corrupt_data_handling(self, mock_bill_top):
        """Test handling of corrupted data when generating the bill top."""
        # Simulate a scenario where bill_top method encounters corrupted data
        mock_bill_top.side_effect = ValueError("Corrupted data encountered")

        # Simulate a ready state to generate a bill
        self.bill.var_cname.set("Jane Doe")
        self.bill.var_contact.set("987654321")
        self.bill.cart_list = [['1', 'Widget', '15.00', '3', '30']]

        # Expect the ValueError to be raised when trying to generate a bill
        with self.assertRaises(ValueError):
            self.bill.generate_bill()

if __name__ == '__main__':
    unittest.main()
