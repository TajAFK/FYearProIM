import unittest  # Import the unittest module for creating and running tests
from unittest.mock import patch, MagicMock  # Import patch and MagicMock for mocking objects and methods
import tkinter as tk  # Import tkinter module for GUI-related components
from billing import BillClass  # Import the BillClass from the billing module


class TestBillClass(unittest.TestCase):
    """Test case class for testing the BillClass."""

    def setUp(self):
        """
        Prepares the environment for tests:
         - Creates a hidden Tkinter window for GUI-related components.
         - Patches tkinter.StringVar to control values in tests.
         - Mocks GUI elements of BillClass to focus on logic, not rendering.
        """
        # Create a hidden Tkinter root window
        self.root = tk.Tk()
        self.root.withdraw()

        # Patch tkinter.StringVar to control its value during tests
        self.p_var_search = patch('tkinter.StringVar')
        self.mock_var_search = self.p_var_search.start()
        # Mock the get method to return a test product name
        self.mock_var_search.return_value.get.return_value = 'Test Product'

        # Mock GUI elements of BillClass to focus on logic, not rendering
        with patch('billing.PhotoImage'), patch('billing.Button'), patch('billing.Label'), patch('billing.Entry'):
            self.bill = BillClass(self.root)

    def tearDown(self):
        """Stops patches and cleans up the Tkinter window."""
        # Stop the patching of StringVar
        self.p_var_search.stop()
        # Destroy the Tkinter root window to clean up after tests
        self.root.destroy()

    @patch('billing.sqlite3.connect')
    def test_add_update_cart(self, mock_connect):
        """
        Tests if an item can be successfully added/updated in the cart when stock is available.
        """
        # Configure test data for adding an item to the cart
        self.bill.var_pid.set('1')  # Set product ID
        self.bill.var_pname.set('Test Product')  # Set product name
        self.bill.var_price.set('10')  # Set product price
        self.bill.var_qty.set('2')  # Set quantity to add
        self.bill.var_stock.set('5')  # Set available stock

        # Call the method to add/update the cart
        self.bill.add_update_cart()
        # Assert that the quantity in the cart list is as expected
        self.assertEqual(self.bill.cart_list[0][3], '2')

    def test_generate_bill_no_items(self):
        """
        Tests if a ValueError is raised when attempting to generate a bill with an empty cart.
        """
        # Set customer name and contact details
        self.bill.var_cname.set('John Doe')
        self.bill.var_contact.set('1234567890')

        # Attempt to generate a bill and expect a ValueError due to an empty cart
        with self.assertRaises(ValueError):
            self.bill.generate_bill()


if __name__ == '__main__':
    unittest.main()  # Run the tests when the script is executed directly
