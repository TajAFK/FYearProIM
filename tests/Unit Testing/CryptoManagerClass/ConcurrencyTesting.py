import unittest  # Import the unittest module for creating and running tests
import threading  # Import threading module for concurrent execution
from CryptoManager import CryptoManagerClass  # Import the CryptoManagerClass from the CryptoManager module


class TestCryptoManagerConcurrency(unittest.TestCase):
    """Test case class for testing concurrency in CryptoManagerClass."""

    def setUp(self):
        """Instantiates a CryptoManagerClass object for testing."""
        # Create an instance of CryptoManagerClass
        self.crypto_manager = CryptoManagerClass()

    def thread_routine_encrypt_decrypt(self, plain_text, results, index):
        """
        Encrypts and decrypts data within a thread, storing the result.

        Args:
          plain_text: The original plaintext data.
          results: A list to store the success/failure status of the operation.
          index: The index within the results list where this thread's result should be stored.
        """
        # Encrypt the plaintext data
        encrypted = self.crypto_manager.encrypt_data(plain_text)
        # Decrypt the encrypted data
        decrypted = self.crypto_manager.decrypt_data(encrypted)
        # Store the result of the comparison (True if successful, False otherwise)
        results[index] = decrypted == plain_text

    def test_concurrent_encryption_decryption(self):
        """
        Tests if encryption and decryption work correctly under concurrent conditions.

        This test does the following:
          1. Launches multiple threads, each encrypting and decrypting the same data.
          2. Stores results indicating if the decrypted data matches the original plaintext.
          3. Asserts that all thread operations were successful.
        """
        threads = []  # List to hold all the threads
        results = [False] * 10  # List to track results of each thread (initially all set to False)

        # Create and start 10 threads
        for i in range(10):
            thread = threading.Thread(target=self.thread_routine_encrypt_decrypt, args=("Test data", results, i))
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        # Assert that all threads were successful
        self.assertTrue(all(results))


if __name__ == "__main__":
    unittest.main()  # Run the tests when the script is executed directly
