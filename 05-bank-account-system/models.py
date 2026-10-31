from datetime import datetime


class InsufficientFunds(Exception):
    pass


class Account:
    account_type = "account"

    def __init__(self, account_number, name, balance=0, history=None):
        self.account_number = account_number
        self.name = name
        self.__balance = balance
        self.history = history if history is not None else []

    def get_balance(self):
        return self.__balance

    def _record(self, kind, amount):
        self.history.append({
            "type": kind,
            "amount": amount,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "balance_after": self.__balance,
        })

    def _check_amount(self, amount):
        if amount <= 0:
            raise ValueError("Raqam positive honi chahiye.")

    def _can_withdraw(self, amount):
        return amount <= self.__balance

    def deposit(self, amount, kind="deposit"):
        self._check_amount(amount)
        self.__balance += amount
        self._record(kind, amount)

    def withdraw(self, amount, kind="withdraw"):
        self._check_amount(amount)
        if not self._can_withdraw(amount):
            raise InsufficientFunds("Balance kam hai.")
        self.__balance -= amount
        self._record(kind, amount)

    def to_dict(self):
        return {
            "account_number": self.account_number,
            "name": self.name,
            "type": self.account_type,
            "balance": self.__balance,
            "history": self.history,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["account_number"],
            data["name"],
            data["balance"],
            data["history"],
        )


class SavingsAccount(Account):
    account_type = "savings"
    MIN_BALANCE = 500

    def _can_withdraw(self, amount):
        return self.get_balance() - amount >= self.MIN_BALANCE


class CurrentAccount(Account):
    account_type = "current"
    OVERDRAFT_LIMIT = 5000

    def _can_withdraw(self, amount):
        return amount <= self.get_balance() + self.OVERDRAFT_LIMIT


ACCOUNT_TYPES = {
    "savings": SavingsAccount,
    "current": CurrentAccount,
}


def account_from_dict(data):
    return ACCOUNT_TYPES[data["type"]].from_dict(data)


class Bank:
    def __init__(self, accounts=None):
        self.accounts = accounts if accounts is not None else {}

    def next_number(self):
        if not self.accounts:
            return "1001"
        return str(max(int(n) for n in self.accounts) + 1)

    def open_account(self, name, kind, opening_amount):
        account = ACCOUNT_TYPES[kind](self.next_number(), name)
        if opening_amount > 0:
            account.deposit(opening_amount)
        self.accounts[account.account_number] = account
        return account

    def get_account(self, number):
        if number not in self.accounts:
            raise ValueError("Ye account number maujood nahi hai.")
        return self.accounts[number]

    def transfer(self, from_number, to_number, amount):
        if from_number == to_number:
            raise ValueError("Khud ko transfer nahi kar sakte.")
        sender = self.get_account(from_number)
        receiver = self.get_account(to_number)
        sender.withdraw(amount, kind="transfer out")
        receiver.deposit(amount, kind="transfer in")

    def close_account(self, number):
        account = self.get_account(number)
        if account.get_balance() != 0:
            raise ValueError("Account band karne ke liye balance zero hona chahiye.")
        del self.accounts[number]