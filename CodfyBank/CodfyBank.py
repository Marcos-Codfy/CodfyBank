import os
import getpass
from time import sleep
import Customer

# GLOBAL VARIABLES
valid_login = False
user = Customer.Customer()

# FUNCTIONS
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def register_pix_key(response):
    """Registers a new Pix key with validation for CPF, Phone, CNPJ, or E-mail."""
    if response != "yes":
        print("Operation cancelled.")
        sleep(2)
        return

    while True:
        clear_screen()
        print("PIX Key Registration")
        print("=======================")
        print("Available types:")
        print("1 – CPF")
        print("2 – Phone")
        print("3 – CNPJ")
        print("4 – E-mail")
        type_input = input("Choose the key type (1|2|3|4): ").strip()

        if type_input == "1":
            key_type = "cpf"
        elif type_input == "2":
            key_type = "phone"
        elif type_input == "3":
            key_type = "cnpj"
        elif type_input == "4":
            key_type = "email"
        else:
            print("\nInvalid type option. Please try again.")
            sleep(2)
            continue

        key_value = input(f"\nEnter your key ({key_type}): ").strip()

        # Normalize and validate
        if key_type in ("cpf", "phone", "cnpj"):
            digits = "".join(filter(str.isdigit, key_value))
            length = len(digits)
            if (
                (key_type == "cpf" and length != 11)
                or (key_type == "phone" and length not in (10, 11))
                or (key_type == "cnpj" and length != 14)
            ):
                print("\nInvalid PIX key. Please try again.")
                sleep(2)
                continue
            valid_key = digits
        else:  # email
            if "@" not in key_value or "." not in key_value.split("@")[-1]:
                print("\nInvalid PIX key. Please try again.")
                sleep(2)
                continue
            valid_key = key_value.lower()

        # everything is ok: register and confirm
        user.add_pix_key(key_type, valid_key)
        print("\nPIX key registered successfully!")
        sleep(2)
        Pix()
        break

def Pix():
    clear_screen()
    print("PIX Area")
    print("=======================")

    if not user.pix_keys:
        print("No PIX key registered.")
        print("\nDo you want to register one now?")
        response = input("Enter 'yes' to register: ").strip().lower()
        register_pix_key(response)
    else:
        print("Registered PIX keys:")
        for p in user.pix_keys:
            print(f"- {p['type'].upper()}: {p['key']}")
        print("=======================")
        print("\n1 – Register new key")
        print("2 – Back to menu")
        choice = input("Option: ").strip()
        if choice == "1":
            register_pix_key("yes")

def PixTransfer():
    clear_screen()
    print("Transfer Area - PIX")
    print("=======================")
    destination_pix = input("Enter the recipient's PIX key: ").strip()
    amount_str = input("Enter the amount to be transferred: R$ ").strip().replace(',', '.')
    # Simple validation to check if it is a number
    if not amount_str.replace('.', '', 1).isdigit():
        print("\nInvalid amount. Please enter a number.")
        sleep(2)
        input("\nPress Enter to return to the menu...")
        return

    amount_float = float(amount_str)
    if amount_float <= 0:
        print("\nThe transfer amount must be positive.")
        sleep(2)
        input("\nPress Enter to return to the menu...")
        return

    # Logic to check if the transfer is to oneself
    user_keys = []
    for key in user.pix_keys:
        user_keys.append(key['key'])

    # If the destination key is in the user's key list
    if destination_pix in user_keys:
        print(f"\nTransferring R$ {amount_float:.2f} to yourself...")
        sleep(2)
        # Only registers in the statement, without changing the balance
        user.register_statement(f"PIX Transfer to self of R$ {amount_float:.2f}")
        print("Operation successful!")
    
    # If it's for another person, use the normal debit logic
    else:
        print(f"\nTransferring R$ {amount_float:.2f} to the PIX key {destination_pix}...")
        sleep(2)
        if user.debit(amount_float):
            print("Transfer successful!")
            user.register_statement(f"PIX Transfer of R$ {amount_float:.2f} to {destination_pix}")
        else:
            print("Insufficient balance and limit for the transfer.")
            sleep(2)
            
    input("\nPress Enter to return to the menu...")

def AgencyAndAccountTransfer():
    clear_screen()
    print("Transfer Area - Agency and Account")
    print("=======================")
    destination_agency = input("Enter the recipient's agency: ").strip()
    destination_account = input("Enter the recipient's account: ").strip()
    amount_str = input("Enter the amount to be transferred: R$ ").strip()
    amount_float = float(amount_str)
    print(f"\nTransferring R$ {amount_str} to account {destination_account} of agency {destination_agency}...")
    sleep(2)
    if user.debit(amount_float):
        print("Transfer successful!")
        user.register_statement(f"Transfer of R$ {amount_float:.2f} to {destination_agency}/{destination_account}")
    else:
        print("Insufficient balance and limit for the transfer.")
        sleep(2)
    input("\nPress Enter to return to the menu...")

def Deposit():
    clear_screen()
    print("Deposit Area")
    print("=======================")
    amount_str = input("Enter the amount to be deposited: R$ ").strip()
    print(f"\nDepositing R$ {amount_str} into your account...")
    sleep(2)
    print("Deposit successful!")
    user.credit(float(amount_str))  # This line alone correctly updates the balance and limit
    user.register_statement(f"Deposit of R$ {float(amount_str):.2f}")
    input("\nPress Enter to return to the menu...")

def Withdraw():
    clear_screen()
    print("Withdrawal Area")
    print("=======================")
    amount_str = input("Enter the amount to withdraw: R$ ").strip()
    amount_float = float(amount_str)
    if user.debit(amount_float):
        print(f"\nWithdrawing R$ {amount_str} from your account...")
        sleep(2)
        print("Withdrawal successful!")
        user.register_statement(f"Withdrawal of R$ {amount_float:.2f}")
    else:
        print("\nInsufficient balance and limit for withdrawal.")
        sleep(2)
    input("\nPress Enter to return to the menu...")
    
def AdjustLimit():
    clear_screen()
    print("Available Limit Adjustment")
    print("===========================")
    
    used_amount = user.maximum_limit - user.limit
    
    print(f"Your maximum approved limit is: R$ {user.maximum_limit:.2f}")
    print(f"Your current available limit is: R$ {user.limit:.2f}")
    if used_amount > 0:
        print(f"You are already using R$ {used_amount:.2f} of your limit.")
    
    print("\nYou can adjust your available limit.")
    print(f"The value must be between R$ {used_amount:.2f} and R$ {user.maximum_limit:.2f}.")
    
    value_str = input("Enter the new value for the available limit: R$ ").strip().replace(',', '.')
    
    # Simple validation to check if it is a number
    if not value_str.replace('.', '', 1).isdigit():
        print("\nInvalid input. Please enter a number.")
    else:
        new_limit = float(value_str)
        # Calls the class method that contains the logic
        message = user.adjust_limit(new_limit)
        print(f"\n{message}")

    sleep(3)
    input("\nPress Enter to return to the menu...")

def Statement():
    clear_screen()
    print("Account Statement")
    print("=======================")
    print(f"Customer: {user.name} {user.last_name}")
    print(f"Agency: {user.agency}  Account: {user.account}")
    print(f"Current Balance: R$ {user.balance:.2f}")
    print("=======================")
    print("Operations:")
    if not user.statement:
        print("No operations performed.")
    else:
        for operation in user.statement:
            print(f"- {operation}")
    input("\nPress Enter to return to the menu...")

# UPDATED SETTINGS FUNCTION
def Settings():
    clear_screen()
    print("Settings Area")
    print("=======================")
    print(f"Name: {user.name} {user.last_name}")
    print(f"Agency: {user.agency}  Account: {user.account}")
    print("----------------------")
    print("1 - Change Name")
    print("2 - Change Password")
    print("3 - Adjust Limit")
    print("0 - Back to Menu")
    choice = input("Option: ").strip()

    if choice == "1":
        new_first_name = input("Enter the new first name: ").strip()
        new_last_name = input("Enter the new last name: ").strip()
        user.name = new_first_name
        user.last_name = new_last_name
        print("Name changed successfully!...")
        sleep(2)
    elif choice == "2":
        print("To change the password, please provide the current password.")
        current_password = input("Current password: ").strip()
        if current_password == user.password:
            new_password = input("Enter the new password: ").strip()
            confirm_password = input("Confirm the new password: ").strip()
            if new_password == confirm_password:
                user.password = new_password
                print("Password changed successfully!...")
            else:
                print("The passwords do not match. Please try again.")
        else:
            print("Incorrect current password.")
        sleep(2)
    elif choice == "3":
        AdjustLimit()

def Home():
    clear_screen()
    print("Welcome to Codfy Bank")
    print("=======================")
    print(f"Customer: {user.name} {user.last_name}")
    print(f"Agency: {user.agency}  Account: {user.account}")
    print(f"Balance: R$ {user.balance:.2f} - Limit: {user.limit}")
    print("____________")
    print("1 – Deposit")
    print("2 – Withdraw")
    print("3 – Statement")
    print("4 – PIX")
    print("5 - Transfer - PIX")
    print("6 - Transfer - Agency and Account")
    print("7 - Settings")
    print("0 – Exit")
    print("____________")

    option_menu = input("Select the desired option: ").strip()
    if option_menu == "1":
        Deposit()
    elif option_menu == "2":
        Withdraw()
    elif option_menu == "3":
        Statement()
    elif option_menu == "4":
        Pix()
    elif option_menu == "5":
        PixTransfer()
    elif option_menu == "6":
        AgencyAndAccountTransfer()
    elif option_menu == "7":
        Settings()
    elif option_menu == "0":
        print("\nExiting...")
        sleep(1)
        exit()
    else:
        print("\nOption not yet implemented.")
        sleep(1.5)

# 5. MAIN PROGRAM EXECUTION
# Login
while not valid_login:
    clear_screen()
    print("Welcome to Codfy Bank")
    print("=======================")
    input_agency = input("Enter your agency: ").strip()
    input_account = input("Enter your account: ").strip()
    # Here the password does not appear on the screen
    input_password = getpass.getpass("Enter your password: ").strip()

    if (input_agency == user.agency and
        input_account == user.account and
        input_password == user.password):
        print("\nLogin successful!")
        valid_login = True
        sleep(1.5)
    else:
        print("\nIncorrect data!")
        sleep(1.5)

# Main loop
while True:
    Home()
