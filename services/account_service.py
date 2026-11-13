from decimal import Decimal

def get_accounts() -> list[dict]:
    """
    Retrieve all accounts.
    Returns a list of account records.
    """
    pass

def add_account(account_name: str, account_type: str, starting_balance: float = 0.00) -> int | None:
    """
    Create a new account.
    Returns the new account ID, or 'None' if unsuccessful.
    """
    pass

def get_account_balance(account_id: int) -> Decimal | None:
    """
    Retrieve an account's current balance.
    Returns a dictionary, or None if the account does not exist.
    """
    pass

def get_account_transactions(account_id: int) -> list[dict]:
    """
    Retrieve all transactions belonging to a specific account.
    Returns a list of transaction records.
    """
    pass

def get_categories(category_type: str = None) -> list[dict]:
    """
    Retrieve available categories.
    Optionally filter by 'Income' or 'Expense' (not necessarily required, but should not be hard to implement)
    Returns a list of category records.
    """
    pass

def get_merchants() -> list[dict]:
    """
    Retrieve all available merchants.
    Returns a list of merchant records.
    """
    pass