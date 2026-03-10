Project: Secure OOP System
This project is a multi-user dashboard application built with Python and Tkinter. It features a robust SQLite backend, SHA-256 password hashing, and a mandatory 2-factor authentication (2FA) system via email for critical actions like registration and account deletion.

## System Architecture
The application follows a modular Object-Oriented Programming (OOP) design to separate concerns between the user interface, database management, and external services.

1. main.py (The Application Controller)
This is the entry point of the application. It manages the primary application loop, screen transitions, and user session state.

Class: SystemApp

__init__: Initializes the database and UI root.

check_initial_setup: A first-run check that forces the user to configure the system SMTP email and create a "Super Admin."

show_login_screen: Handles user authentication.

show_registration: Coordinates with the Mailer class to verify new users via email before adding them to the database.

show_dashboard: Displays user-specific content and navigation.

show_admin_panel: Provides an administrative interface for managing (deleting or resetting) other users.

2. database.py (Data Persistence)
Handles all direct interactions with the system.db SQLite database.

Class: DatabaseManager

setup_db: Creates the users and settings tables if they don't exist.

hash_pwd: Converts plain-text passwords into SHA-256 hashes for secure storage.

authenticate: Validates credentials by hashing the input and comparing it to the stored hash.

reset_password & delete_user: Administrative and self-service functions for record management.

3. mailer.py (Security & Communication)
Manages the SMTP connection to send 2FA tokens.

Class: Mailer

send_confirmation: Generates a random 6-character alphanumeric token and emails it to the specified recipient using Gmail’s SSL SMTP server.

4. analyser.py (Feature Module)
A UI skeleton module representing the core analytical features of the dashboard.

Class: DataAnalyserModule

build_ui: Dynamically builds the dashboard content based on the user's role (Admin vs. User).

## Setup Instructions
To get the system running with the pre-configured admin credentials, follow these steps:

Clear Old Data: Delete the system.db file if it exists in your directory.

Run the App: Execute python main.py.

Initial Configuration: The system will prompt for "Setup." Use the following credentials from readme.txt:



Create Admin: Set your desired Admin username and password.

Populate Users: Register at least 4 users via the "Create New Account" button to meet the project delivery requirements.