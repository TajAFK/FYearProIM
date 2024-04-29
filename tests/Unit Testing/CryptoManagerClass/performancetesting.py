import unittest
import time
from CryptoManager import CryptoManagerClass

class TestCryptoManagerPerformance(unittest.TestCase):
    def setUp(self):
        """Instantiates a CryptoManagerClass object for testing."""
        self.crypto_manager = CryptoManagerClass()

    def test_large_data_encryption(self):
        """
        Measures encryption time for a large input (1 million characters).

        Notes:
          - This provides a baseline, but performance can vary across machines and encryption settings.
          - Consider adding a performance threshold assertion for more rigorous testing.
        """
        large_data = 'a' * 10**6
        start_time = time.time()
        encrypted_data = self.crypto_manager.encrypt_data(large_data)
        end_time = time.time()

        self.assertTrue(len(encrypted_data) > 0)  # Basic sanity check that encryption worked
        print(f"Encryption time for large data: {end_time - start_time} seconds")

    def test_large_data_decryption(self):
        """
        Measures decryption time for a large input (1 million characters).

        Notes:
          - This provides a baseline, but performance can vary across machines and encryption settings.
          - Consider adding a performance threshold assertion for more rigorous testing.
        """
        large_data = 'a' * 10**6
        encrypted_data = self.crypto_manager.encrypt_data(large_data)
        start_time = time.time()
        decrypted_data = self.crypto_manager.decrypt_data(encrypted_data)
        end_time = time.time()

        self.assertEqual(decrypted_data, large_data)  # Validate that decryption succeeded
        print(f"Decryption time for large data: {end_time - start_time} seconds")

if __name__ == "__main__":
    unittest.main()
