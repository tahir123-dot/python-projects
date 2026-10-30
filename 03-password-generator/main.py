import secrets
import string

MAX_LENGTH = 128

OPTIONS = [
    ("Bade harf (A-Z)", string.ascii_uppercase),
    ("Chhote harf (a-z)", string.ascii_lowercase),
    ("Numbers (0-9)", string.digits),
    ("Symbols (@#$%)", string.punctuation),
]


def ask_yes_no(question):
    while True:
        answer = input(f"{question} (y/n): ").strip().lower()
        if answer in ("y", "n"):
            return answer == "y"
        print("Sirf y ya n likho.")


def choose_sets():
    while True:
        selected = []
        for name, chars in OPTIONS:
            if ask_yes_no(f"{name} chahiye?"):
                selected.append(chars)

        if selected:
            return selected
        print("Kam az kam ek qism chunni paregi. Dobara chuno.\n")


def get_length(min_length, max_length):
    while True:
        try:
            length = int(input(f"Password ki length ({min_length} se {max_length}): "))
        except ValueError:
            print("Number likho, text nahi.")
            continue

        if min_length <= length <= max_length:
            return length
        print(f"{min_length} se {max_length} ke beech number likho.")


def generate_password(length, sets):
    # har chuni hui qism ka kam az kam ek character
    password = [secrets.choice(chars) for chars in sets]

    # baqi jagah poore pool se bharo
    pool = "".join(sets)
    while len(password) < length:
        password.append(secrets.choice(pool))

    # order phent do, warna pehle characters ka pattern andaza ho jata hai
    secrets.SystemRandom().shuffle(password)
    return "".join(password)


def main():
    while True:
        sets = choose_sets()
        length = get_length(len(sets), MAX_LENGTH)
        print("\nTumhara password:", generate_password(length, sets))

        again = input("\nDobara banana hai? (y/n): ").strip().lower()
        if again != "y":
            print("Khuda hafiz!")
            break


if __name__ == "__main__":
    main()