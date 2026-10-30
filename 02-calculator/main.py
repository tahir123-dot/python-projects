def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("0 se taqseem nahi hoti.")
    return a / b


OPERATIONS = {
    1: ("Sum (+)", add),
    2: ("Minus (-)", subtract),
    3: ("Multi (*)", multiply),
    4: ("Division (/)", divide),
}


def show_menu():
    print("\nOperation chuno:")
    for key, (name, _) in OPERATIONS.items():
        print(f"{key} : {name}")


def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Number likho, text nahi.")


def get_choice():
    while True:
        try:
            choice = int(input("Operation number likho: "))
        except ValueError:
            print("Menu ka number likho.")
            continue

        if choice in OPERATIONS:
            return choice
        print("Ye number menu mein nahi hai.")


def calculate():
    show_menu()
    choice = get_choice()
    num1 = get_number("Pehla number: ")
    num2 = get_number("Doosra number: ")

    name, func = OPERATIONS[choice]
    try:
        result = func(num1, num2)
    except ZeroDivisionError as e:
        print(e)
        return

    print(f"Result: {result}")


def main():
    while True:
        calculate()
        again = input("Dobara hisaab karna hai? (y/n): ").strip().lower()
        if again != "y":
            print("Khuda hafiz!")
            break


if __name__ == "__main__":
    main()