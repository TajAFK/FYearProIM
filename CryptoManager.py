import os
from tkinter import messagebox
from cryptography.fernet import Fernet


class CryptoManagerClass:
    def __init__(self):
        """Initialize the encryption and decryption using Fernet symmetric encryption."""
        self.key = None
        self.cipher = self.load_key_and_initialize_cipher()

    def load_key_and_initialize_cipher(self):
        """
        Loads an existing encryption key from a file, or generates and saves a new key if not present.
        Ensures a Fernet cipher object is always ready for encryption or decryption tasks.
        """
        key_path = 'secret.key'
        if os.path.exists(key_path):
            with open(key_path, 'rb') as key_file:
                self.key = key_file.read()
        else:
            self.key = Fernet.generate_key()
            with open(key_path, 'wb') as key_file:
                key_file.write(self.key)
        return Fernet(self.key)

    def encrypt_data(self, plain_text):
        """
        Encrypts the provided plain text using the initialized cipher object.

        Args:
            plain_text (str): The text data to encrypt.

        Returns:
            str: Encrypted text in UTF-8 encoding or an empty string if an error occurs.
        """
        if plain_text is None or not plain_text.strip():
            return ""
        try:
            return self.cipher.encrypt(plain_text.encode('utf-8')).decode('utf-8')
        except Exception as e:
            messagebox.showerror("Encryption Error", f"Failed to encrypt data: {e}")
            return ""

    def decrypt_data(self, cipher_text):
        """
        Decrypts the provided encrypted text using the initialized cipher object.

        Args:
            cipher_text (str): The encrypted text to be decrypted.

        Returns:
            str: Decrypted text in UTF-8 encoding or an empty string if an error occurs.
        """
        if cipher_text is None or not cipher_text.strip():
            return ""
        try:
            return self.cipher.decrypt(cipher_text.encode('utf-8')).decode('utf-8')
        except Exception as e:
            messagebox.showerror("Decryption Error", f"Failed to decrypt data: {e}")
            return ""


if __name__ == "__main__":
    # Example usage
    crypto_manager = CryptoManagerClass()
    encrypted = crypto_manager.encrypt_data("Hello, world!")
    print("Encrypted:", encrypted)
    decrypted = crypto_manager.decrypt_data(encrypted)
    print("Decrypted:", decrypted)
