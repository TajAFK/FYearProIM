import pyautogui  # PyAutoGUI is a Python module used for programmatically controlling the mouse and keyboard.
import subprocess  # Subprocess is a module used to run new applications or programs through Python code.
import time  # Time module is used for various time-related functions.
import os  # OS module provides a way to interact with the operating system.
import sys  # Sys module provides access to some variables used or maintained by the interpreter and to functions that interact with the interpreter.

def open_application():
    """Starts the application by running the specified Python script."""
    # Define the path to your Python script
    script_path = 'G:\\My Drive\\InventoryManagement\\login.py'  # Ensure this is the correct path to your script

    # Check if the file exists before trying to open it
    if not os.path.exists(script_path):
        # Print an error message if the file does not exist
        print(f"Error: The file '{script_path}' does not exist.")
        # Exit the script if the file does not exist to avoid further errors
        sys.exit(1)

    # Open the application by running the script in a new process
    subprocess.Popen(['python', script_path])
    # Wait for 5 seconds to ensure the application has enough time to open
    time.sleep(5)

def login(username, password):
    """Performs login actions by automating the input of username and password."""
    # Define the screen coordinates for the username, password fields, and the login button
    # You may need to use pyautogui's locateOnScreen to find elements dynamically if static coordinates don't work
    username_field = (650, 200)  # Example coordinates for username entry
    password_field = (650, 300)  # Example coordinates for password entry
    login_button = (700, 400)  # Example coordinates for the login button

    # Click the username field and type the username
    pyautogui.click(username_field)
    pyautogui.write(username, interval=0.25)  # Type with a slight delay between keystrokes

    # Click the password field and type the password
    pyautogui.click(password_field)
    pyautogui.write(password, interval=0.25)  # Type with a slight delay between keystrokes

    # Click the login button to submit the login form
    pyautogui.click(login_button)

def main():
    """Main function to start the application and perform the login."""
    open_application()  # Open the application
    login('101', '123456')  # Perform login with provided credentials

# Ensure the script runs only if it is executed directly (not imported as a module)
if __name__ == "__main__":
    main()
