import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from billing import BillClass


class TestBillClass(unittest.TestCase):
    def setUp(self):
        """
        Prepares the environment for tests:
         - Creates a hidden Tkinter window for GUI-related components.
         - Patches tkinter.StringVar to control values in tests.
         - Mocks GUI elements of BillClass to focus on logic, not rendering.
        """
        self.root = tk.Tk()
        self.root.withdraw()

        self.p_var_search = patch('tkinter.StringVar')
        self.mock_var_search = self.p_var_search.start()
        self.mock_var_search.return_value.get.return_value = 'Test Product'

        with patch('billing.PhotoImage'), patch('billing.Button'), patch('billing.Label'), patch('billing.Entry'):
            self.bill = BillClass(self.root)

    def tearDown(self):
        """Stops patches and cleans up the Tkinter window."""
        self.p_var_search.stop()
        self.root.destroy()

    @patch('billing.sqlite3.connect')
    def test_add_update_cart(self, mock_connect):
        """
        Tests if an item can be successfully added/updated in the cart when stock is available.
        """
        # Configure test data
        self.bill.var_pid.set('1')
        self.bill.var_pname.set('Test Product')
        self.bill.var_price.set('10')
        self.bill.var_qty.set('2')
        self.bill.var_stock.set('5')

        self.bill.add_update_cart()
        self.assertEqual(self.bill.cart_list[0][3], '2')

    def test_generate_bill_no_items(self):
        """
        Tests if a ValueError is raised when attempting to generate a bill with an empty cart.
        """
        self.bill.var_cname.set('John Doe')
        self.bill.var_contact.set('1234567890')
        with self.assertRaises(ValueError):
            self.bill.generate_bill()


if __name__ == '__main__':
    unittest.main()
