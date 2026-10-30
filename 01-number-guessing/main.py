import random


def get_guess(low, high):
    while True:
        try:
            guess = int(input(f"Guess karo ({low} se {high}): "))
        except ValueError:
            print("Number likho, text nahi.")
            continue

        if low <= guess <= high:
            return guess
        print(f"{low} se {high} ke beech number likho.")


def play_game(low, high):
    secret = random.randint(low, high)
    attempts = 0

    while True:
        guess = get_guess(low, high)
        attempts += 1

        if guess == secret:
            print(f"Sahi! Tumne {attempts} koshishon mein jeeta.")
            return
        elif guess < secret:
            print("Kam hai, bara number likho.")
        else:
            print("Zyada hai, chhota number likho.")


def main():
    while True:
        play_game(1, 10)
        again = input("Dobara khelna hai? (y/n): ").strip().lower()
        if again != "y":
            print("Khuda hafiz!")
            break


if __name__ == "__main__":
    main()