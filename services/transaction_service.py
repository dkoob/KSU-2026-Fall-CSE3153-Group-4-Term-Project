def add_transaction(account_id: int, category_id: int, amount: float, transaction_date, merchant_id: int = None, description: str = None) -> int | None:
    """
    Create a new transaction.
    Returns the new transaction ID, or None if unsuccessful.

    I will add a way for the user to add a merchant in the middle of adding a transaction within the looping menu.
    """
    pass

def get_transactions(account_id: int = None) -> list[dict]:
    """
    Retrieve transactions.
    Optionally filter by account ID.
    Returns a list of transaction records.
    """
    pass

def update_transaction(transaction_id: int, account_id: int, category_id: int, amount: float, transaction_date, merchant_id: int = None, description: str = None) -> bool:
    """
    Update an existing transaction using its ID.
    Returns True if updated, otherwise False.

    This one may be tricky because the account balances will also have to be updated if a transaction's amount is updated.
    So if the transaction is changed to have costed more, subtract more from the balance, if the transaction is less now, add to the balance.
    """
    pass

def delete_transaction(transaction_id: int) -> bool:
    """
    Delete a transaction using its ID.
    Returns True if deleted, otherwise False.

    Same as above, should reverse the initial effect on the account's balance.
    """
    pass