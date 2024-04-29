import unittest
import threading
from CryptoManager import CryptoManagerClass


class TestCryptoManagerConcurrency(unittest.TestCase):
    def setUp(self):
        """Instantiates a CryptoManagerClass object for testing."""
        self.crypto_manager = CryptoManagerClass()

    def thread_routine_encrypt_decrypt(self, plain_text, results, index):
        """
        Encrypts and decrypts data within a thread, storing the result.

        Args:
          plain_text: The original plaintext data.
          results: A list to store the success/failure status of the operation.
          index: The index within the results list where this thread's result should be stored.
        """
        encrypted = self.crypto_manager.encrypt_data(plain_text)
        decrypted = self.crypto_manager.decrypt_data(encrypted)
        results[index] = decrypted == plain_text

    def test_concurrent_encryption_decryption(self):
        """
        Tests if encryption and decryption work correctly under concurrent conditions.

        This test does the following:
          1. Launches multiple threads, each encrypting and decrypting the same data.
          2. Stores results indicating if the decrypted data matches the original plaintext.
          3. Asserts that all thread operations were successful.
        """
        threads = []
        results = [False] * 10  # List to track results of each thread

        for i in range(10):
            thread = threading.Thread(target=self.thread_routine_encrypt_decrypt, args=("Test data", results, i))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()  # Wait for all threads to finish

        self.assertTrue(all(results))  # Assert all threads were successful


if __name__ == "__main__":
    unittest.main()
