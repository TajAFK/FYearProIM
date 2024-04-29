import pyautogui
import subprocess
import time
import os
import sys


def open_application():
    """Starts the application."""
    # Define the path to your Python script
    script_path = 'G:\\My Drive\\InventoryManagement\\login.py'  # Ensure this is the correct path

    # Check if the file exists before trying to open it
    if not os.path.exists(script_path):
        print(f"Error: The file '{script_path}' does not exist.")
        sys.exit(1)  # Exit the script if the file does not exist

    # Open the application if the file exists
    subprocess.Popen(['python', script_path])
    time.sleep(5)  # Wait for the app to open


def login(username, password):
    """Performs login actions."""
    # You may need to use pyautogui's locateOnScreen to find elements dynamically if static coordinates don't work
    username_field = (650, 200)  # Mock coordinates for username entry
    password_field = (650, 300)  # Mock coordinates for password entry
    login_button = (700, 400)  # Mock coordinates for the login button

    # Click username field, type username
    pyautogui.click(username_field)
    pyautogui.write(username, interval=0.25)

    # Click password field, type password
    pyautogui.click(password_field)
    pyautogui.write(password, interval=0.25)

    # Click the login button
    pyautogui.click(login_button)


def main():
    open_application()
    login('101', '123456')  # Use valid credentials for testing


if __name__ == "__main__":
    main()
