import unittest  # Import the unittest module for creating and running tests
from CryptoManager import CryptoManagerClass  # Import the CryptoManagerClass from the CryptoManager module

class TestCryptoManagerClass(unittest.TestCase):
    """Test case class for testing the CryptoManagerClass."""

    def setUp(self):
        """Instantiates a CryptoManagerClass object for testing."""
        # Create an instance of CryptoManagerClass for use in all tests
        self.crypto_manager = CryptoManagerClass()

    def test_encryption_and_decryption(self):
        """
        Tests the core functionality: encryption followed by decryption
        should result in the original text.
        """
        plaintext = "teststring"  # Define a sample plaintext string
        encrypted = self.crypto_manager.encrypt_data(plaintext)  # Encrypt the plaintext
        decrypted = self.crypto_manager.decrypt_data(encrypted)  # Decrypt the encrypted text
        # Assert that the decrypted text matches the original plaintext
        self.assertEqual(plaintext, decrypted, "Decrypted text should match the original plaintext")

    def test_encryption_of_empty_string(self):
        """
        Tests if an empty string is handled correctly by encryption.
        An empty ciphertext is expected for consistency.
        """
        # Assert that encrypting an empty string returns an empty string
        self.assertEqual(self.crypto_manager.encrypt_data(""), "",
                         "Encryption of an empty string should return an empty string")

    def test_decryption_of_empty_string(self):
        """
        Tests if an empty string is handled correctly by decryption.
        An empty plaintext is expected for consistency.
        """
        # Assert that decrypting an empty string returns an empty string
        self.assertEqual(self.crypto_manager.decrypt_data(""), "",
                         "Decryption of an empty string should return an empty string")

    def test_encryption_with_none_input(self):
        """
        Tests how the encryption handles None as input.
        An empty string output ensures robustness.
        """
        # Assert that encrypting None returns an empty string
        self.assertEqual(self.crypto_manager.encrypt_data(None), "", "Encryption of None should return an empty string")

    def test_decryption_with_none_input(self):
        """
        Tests how the decryption handles None as input.
        An empty string output ensures robustness.
        """
        # Assert that decrypting None returns an empty string
        self.assertEqual(self.crypto_manager.decrypt_data(None), "", "Decryption of None should return an empty string")


if __name__ == '__main__':
    unittest.main()  # Run the tests when the script is executed directly
