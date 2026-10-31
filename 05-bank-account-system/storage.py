import json
from pathlib import Path

from models import Bank, account_from_dict

DATA_FILE = Path(__file__).parent / "accounts.json"


def load_bank():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return Bank()
    except json.JSONDecodeError:
        print("accounts.json kharab thi, khali bank se shuru kar raha hun.")
        return Bank()

    accounts = {}
    for item in data:
        account = account_from_dict(item)
        accounts[account.account_number] = account
    return Bank(accounts)


def save_bank(bank):
    data = [account.to_dict() for account in bank.accounts.values()]
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)