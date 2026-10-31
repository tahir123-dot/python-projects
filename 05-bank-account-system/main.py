from models import InsufficientFunds
from storage import load_bank, save_bank


def get_amount(prompt, allow_zero=False):
    while True:
        try:
            amount = float(input(prompt))
        except ValueError:
            print("Number likho, text nahi.")
            continue

        if amount > 0 or (allow_zero and amount == 0):
            return amount
        print("Raqam positive honi chahiye.")


def get_account_type():
    while True:
        choice = input("Account type (1 = Savings, 2 = Current): ").strip()
        if choice == "1":
            return "savings"
        if choice == "2":
            return "current"
        print("1 ya 2 likho.")


def open_account(bank):
    name = input("Naam: ").strip()
    if not name:
        raise ValueError("Naam khali nahi ho sakta.")
    kind = get_account_type()
    opening = get_amount("Shuruati raqam (0 bhi chalega): ", allow_zero=True)
    account = bank.open_account(name, kind, opening)
    print(f"Account ban gaya. Account number: {account.account_number}")


def deposit(bank):
    account = bank.get_account(input("Account number: ").strip())
    account.deposit(get_amount("Raqam: "))
    print(f"Done. Naya balance: {account.get_balance():.2f}")


def withdraw(bank):
    account = bank.get_account(input("Account number: ").strip())
    account.withdraw(get_amount("Raqam: "))
    print(f"Done. Naya balance: {account.get_balance():.2f}")


def show_balance(bank):
    account = bank.get_account(input("Account number: ").strip())
    print(f"{account.name} ({account.account_type}) ka balance: {account.get_balance():.2f}")


def transfer(bank):
    from_number = input("Bhejne wala account number: ").strip()
    to_number = input("Milne wala account number: ").strip()
    bank.transfer(from_number, to_number, get_amount("Raqam: "))
    print("Transfer ho gaya.")


def show_history(bank):
    account = bank.get_account(input("Account number: ").strip())
    if not account.history:
        print("Abhi koi transaction nahi.")
        return
    for item in account.history:
        print(
            f"{item['date']} | {item['type']:<12} | "
            f"{item['amount']:>10.2f} | balance: {item['balance_after']:.2f}"
        )


def close_account(bank):
    bank.close_account(input("Account number: ").strip())
    print("Account band ho gaya.")


MENU = {
    "1": ("Naya account kholo", open_account),
    "2": ("Paise jama karo", deposit),
    "3": ("Paise nikalo", withdraw),
    "4": ("Balance dekho", show_balance),
    "5": ("Transfer", transfer),
    "6": ("Transaction history", show_history),
    "7": ("Account band karo", close_account),
}


def show_menu():
    print("\n--- Bank ---")
    for key, (name, _) in MENU.items():
        print(f"{key} : {name}")
    print("8 : Exit")


def main():
    bank = load_bank()
    while True:
        show_menu()
        choice = input("Choice: ").strip()

        if choice == "8":
            print("Khuda hafiz!")
            break
        if choice not in MENU:
            print("Menu ka number likho.")
            continue

        _, action = MENU[choice]
        try:
            action(bank)
        except (ValueError, InsufficientFunds) as e:
            print("Error:", e)
        else:
            save_bank(bank)


if __name__ == "__main__":
    main()