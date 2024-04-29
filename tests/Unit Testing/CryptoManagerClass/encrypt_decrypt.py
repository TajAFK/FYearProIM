import unittest
from CryptoManager import CryptoManagerClass

class TestCryptoManagerClass(unittest.TestCase):

    def setUp(self):
        """Instantiates a CryptoManagerClass object for testing."""
        self.crypto_manager = CryptoManagerClass()

    def test_encryption_and_decryption(self):
        """
        Tests the core functionality: encryption followed by decryption
        should result in the original text.
        """
        plaintext = "teststring"
        encrypted = self.crypto_manager.encrypt_data(plaintext)
        decrypted = self.crypto_manager.decrypt_data(encrypted)
        self.assertEqual(plaintext, decrypted, "Decrypted text should match the original plaintext")

    def test_encryption_of_empty_string(self):
        """
        Tests if an empty string is handled correctly by encryption.
        An empty ciphertext is expected for consistency.
        """
        self.assertEqual(self.crypto_manager.encrypt_data(""), "",
                         "Encryption of an empty string should return an empty string")

    def test_decryption_of_empty_string(self):
        """
        Tests if an empty string is handled correctly by decryption.
        An empty plaintext is expected for consistency.
        """
        self.assertEqual(self.crypto_manager.decrypt_data(""), "",
                         "Decryption of an empty string should return an empty string")

    def test_encryption_with_none_input(self):
        """
        Tests how the encryption handles None as input.
        An empty string output ensures robustness.
        """
        self.assertEqual(self.crypto_manager.encrypt_data(None), "", "Encryption of None should return an empty string")

    def test_decryption_with_none_input(self):
        """
        Tests how the decryption handles None as input.
        An empty string output ensures robustness.
        """
        self.assertEqual(self.crypto_manager.decrypt_data(None), "", "Decryption of None should return an empty string")


if __name__ == '__main__':
    unittest.main()
