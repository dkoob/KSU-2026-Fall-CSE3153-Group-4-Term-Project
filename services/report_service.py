def get_spending_by_category(account_id: int = None, month: int = None, year: int = None) -> list[dict]:
    """
    Retrieve total expenses grouped by category.
    Optionally filter by account and month/year.
    Returns a list of category spending totals.

    Return in the list like {"Category_name: expense_amount"}
    """
    pass

def get_income_vs_expenses(account_id: int = None, month: int = None, year: int = None) -> dict:
    """
    Retrieve total income, total expenses, and net income.
    Optionally filter by account and month/year.
    Returns a dictionary containing the totals.

    All positive amounts
    All negative amounts
    Current account balance
    """
    pass

def get_top_merchants(account_id: int = None, month: int = None, year: int = None, limit: int = 5) -> list[dict]:
    """
    Retrieve merchants ranked by total transaction spending.
    Optionally filter by account and month/year.
    Returns a list of merchant spending totals.
    """
    pass