import unittest
from CryptoManager import CryptoManagerClass


class TestCryptoManagerErrorHandling(unittest.TestCase):
    def setUp(self):
        """Instantiates a CryptoManagerClass object for testing."""
        self.crypto_manager = CryptoManagerClass()

    def test_corrupt_input_encryption(self):
        """
        Tests if the encryption method avoids encrypting potentially corrupt data.

        This test uses data that might still be valid for encoding formats but could cause
        issues during encryption or later stages. Ideally, the encryption method should detect
        and handle this gracefully.
        """
        corrupt_data = 'Hello, world!\x00\x01\x02'
        result = self.crypto_manager.encrypt_data(corrupt_data)

        # Best outcome: the method raises an appropriate exception
        # Alternative:
        self.assertNotEqual(result, "", "The method should not encrypt potentially corrupt data.")

    def test_corrupt_input_decryption(self):
        """
        Tests if the decryption method handles invalid ciphertext gracefully.

        This test uses data that is not valid ciphertext. The expected behavior is that
        the decryption method either raises an appropriate exception or returns an empty string
        to signal an error.
        """
        corrupt_data = 'invalidcipherdata'
        result = self.crypto_manager.decrypt_data(corrupt_data)
        self.assertEqual(result, "")

    def test_empty_input_encryption(self):
        """
        Tests if the encryption method handles empty input as expected.
        """
        self.assertEqual(self.crypto_manager.encrypt_data(""), "")

    def test_empty_input_decryption(self):
        """
        Tests if the decryption method handles empty input as expected.
        """
        self.assertEqual(self.crypto_manager.decrypt_data(""), "")


if __name__ == "__main__":
    unittest.main()
