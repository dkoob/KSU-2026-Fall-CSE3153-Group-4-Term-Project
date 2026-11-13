def set_budget(connection, account_id: int, category_id: int, monthly_limit: float, month: int, year: int) -> bool:
    cursor = connection.cursor()

    """
    Create or update a budget for an account and category
    for a specific month and year.
    Returns True if successful, otherwise False.
    Handle the errors from the database to automatically check whether the month/year is valid and determine if this
    function should return true/false.
    """
    pass

def get_budgets(connection, account_id: int = None, month: int = None, year: int = None) -> list[dict]:
    cursor = connection.cursor()

    """
    Retrieve budgets.
    Optionally filter by account, month, and year.
    Returns a list of budget records.
    """
    pass

def get_budget_remaining(connection, account_id: int, category_id: int, month: int, year: int) -> dict | None:
    cursor = connection.cursor()

    """
    Calculate a category's budget limit, amount spent,
    and remaining amount for a specific month.
    Returns a dictionary, or None if no budget exists.

    Basically tally all transactions for this month for this category for a net amount.
    """
    pass