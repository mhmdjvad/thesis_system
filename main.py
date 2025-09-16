import getpass
from pathlib import Path
from data_handler import load_json
from user_auth import authenticate_user
from menus import student_menu
from menus import supervisor_menu
from menus import reviewer_menu
from initial_setup import initialize_defaults

def main_menu():
    """Main entry point for CLI. Handles login and routing to role-specific menus."""
    initialize_defaults()
    print("=== Thesis Management System (CLI) ===")
    while True:
        print("\n1) Login\n0) Exit")
        ch = input("Choice: ").strip()
        if ch == "1":
            user_id = input("User ID: ").strip()
            password = getpass.getpass("Password: ")
            user = authenticate_user(user_id, password)
            if not user:
                print("Login failed.")
                continue
            print(f"Welcome {user['name']} ({user['id']}).")
            user_type = user.get("type")
            if user_type == "student":
                student_menu(user)
            elif user_type == "supervisor":
                supervisor_menu(user)
            elif user_type == "reviewer":
                reviewer_menu(user)
            else:
                print("Unknown user type.")
        elif ch == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main_menu()