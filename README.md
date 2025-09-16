# Thesis Management System (CLI)

This project is a simple command-line interface (CLI) for managing the thesis process among students, supervisors, and reviewers.

## 1. Project Summary

**Objective**: This project aims to implement a CLI-based thesis management system. It allows three types of users (students, supervisors, and reviewers) to manage thesis-related tasks, including submitting thesis requests, tracking status, scheduling defenses, and recording scores.

**Overall Functionality**:
The program starts with a main menu where users can log in. All program data is stored in JSON files, which include information about users, courses, requests, theses, and defenses. Each user is routed to a specific menu based on their role. Students can request a thesis and track its status. Supervisors can approve or reject student requests and schedule defenses. Reviewers can submit defense scores. The program uses a simple logic to manage these processes, such as checking course capacity and the number of theses assigned to a supervisor.

## 2. Requirements

- **Python Version**: Python 3.x
- **Libraries and Packages**:
  - `bcrypt`: For password hashing. This library must be installed using `pip install bcrypt`.

## 3. Project Structure

The project has been refactored into a modular structure for better readability and maintainability.

- **`main.py`**: The entry point of the application.
- **`data_handler.py`**: Handles loading and saving JSON data files.
- **`user_auth.py`**: Manages user authentication and password hashing.
- **`initial_setup.py`**: Creates default data files if they do not exist.
- **`menus.py`**: Contains the menu functions for different user roles.
- **`data/`**: A folder for storing JSON data files.

## 4. Classes and Functions

- `main_menu()`: The main function that displays the login menu and routes the user.
- `initialize_defaults()`: Creates default data files if they are missing.
- `load_json()` / `save_json()`: Helper functions for reading and writing JSON files.
- `hash_password(password)`: Uses the `bcrypt` library to hash a password.
- `check_password(password, hashed_password)`: Compares an entered password to its hashed version.

## 5. Implementation Details

**Password Hashing**: To enhance security, user passwords are no longer stored as plain text. Instead, they are hashed using the **`bcrypt`** algorithm. `bcrypt` is a strong hashing algorithm designed for secure password storage. It uses a random "salt" to prevent dictionary and rainbow table attacks. When a user logs in, the entered password is hashed and compared to the hashed version stored in the `users.json` file.
users pass : pass123

teacher pass : drpass 

reviewer pass: revpass 

Due to possible problems on the library's side, the password hashing system may not work properly. In this case, change the passwords manually.

## 6. How to Run the Program

1.  Save the files with the folder structure described above.
2.  Install the `bcrypt` library: `pip install bcrypt`
3.  Open a terminal and navigate to the project's root folder (`proj`).
4.  Run the application using the command: `python main.py` or `python3 main.py` 

## 7. Sample Output

=== Thesis Management System (CLI) ===

Login

Exit
Choice: 1
User ID: S1001
Password (input hidden): ************
Welcome Ali Rezaei (S1001).

--- Student Menu ---

Request a Thesis

View Request Status

...

