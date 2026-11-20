def _build_filters(account_id: int = None, month: int = None, year: int = None) -> tuple[str, tuple]:
    """Helper function to dynamically build WHERE clauses and query parameters."""
    conditions = []
    params = []

    if account_id is not None:
        conditions.append("t.account_id = ?")
        params.append(account_id)
    if month is not None:
        conditions.append("MONTH(t.transaction_date) = ?")
        params.append(month)
    if year is not None:
        conditions.append("YEAR(t.transaction_date) = ?")
        params.append(year)

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    return where_clause, tuple(params)


def get_spending_by_category(connection, account_id: int = None, month: int = None, year: int = None) -> list[dict]:
    """
    Retrieve total expenses grouped by category.
    Optionally filter by account and month/year.
    Returns a list of category spending totals.

    Return in the list like {"Category_name: expense_amount"}
    """
    cursor = connection.cursor()

    try:
        where_clause, params = _build_filters(account_id, month, year)

        expense_condition = "c.category_type = 'Expense'"
        if where_clause:
            where_clause += f" AND {expense_condition}"
        else:
            where_clause = f"WHERE {expense_condition}"

        query = f"""
            SELECT 
                c.category_name,
                COALESCE(SUM(ABS(t.transaction_amount)), 0) AS total_spent
            FROM tracker.Transactions t
            INNER JOIN tracker.Categories c 
                ON t.category_id = c.category_id
            {where_clause}
            GROUP BY c.category_name
            ORDER BY total_spent DESC;
        """

        cursor.execute(query, params)
        rows = cursor.fetchall()

        results = []
        for row in rows:
            results.append({
                "category_name": row[0],
                "total_spent": float(row[1]),
            })
        return results

    finally:
        cursor.close()


def get_income_vs_expenses(connection, account_id: int = None, month: int = None, year: int = None) -> dict:
    """
    Retrieve total income, total expenses, and net income.
    Optionally filter by account and month/year.
    Returns a dictionary containing the totals.

    All positive amounts
    All negative amounts
    Current account balance
    """
    cursor = connection.cursor()

    try:
        where_clause, params = _build_filters(account_id, month, year)

        query = f"""
            SELECT 
                c.category_type,
                COALESCE(SUM(ABS(t.transaction_amount)), 0) AS total_amount
            FROM tracker.Transactions t
            INNER JOIN tracker.Categories c 
                ON t.category_id = c.category_id
            {where_clause}
            GROUP BY c.category_type;
        """

        cursor.execute(query, params)
        rows = cursor.fetchall()

        total_income = 0.0
        total_expenses = 0.0
        for row in rows:
            if row[0] == "Income":
                total_income = float(row[1])
            elif row[0] == "Expense":
                total_expenses = float(row[1])

        if account_id is not None:
            cursor.execute(
                "SELECT COALESCE(SUM(account_balance), 0) FROM tracker.Accounts WHERE account_id = ?;",
                (account_id,)
            )
        else:
            cursor.execute("SELECT COALESCE(SUM(account_balance), 0) FROM tracker.Accounts;")

        balance_row = cursor.fetchone()
        current_balance = float(balance_row[0]) if balance_row else 0.0

        return {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net_income": total_income - total_expenses,
            "current_balance": current_balance,
        }

    finally:
        cursor.close()


def get_top_merchants(connection, account_id: int = None, month: int = None, year: int = None, limit: int = 5) -> list[dict]:
    """
    Retrieve merchants ranked by total transaction spending.
    Optionally filter by account and month/year.
    Returns a list of merchant spending totals.
    """
    cursor = connection.cursor()

    try:
        where_clause, params = _build_filters(account_id, month, year)

        extra_conditions = "c.category_type = 'Expense' AND t.merchant_id IS NOT NULL"
        if where_clause:
            where_clause += f" AND {extra_conditions}"
        else:
            where_clause = f"WHERE {extra_conditions}"

        query = f"""
            SELECT TOP {int(limit)}
                m.merchant_name,
                COUNT(t.transaction_id) AS transaction_count,
                COALESCE(SUM(ABS(t.transaction_amount)), 0) AS total_spent
            FROM tracker.Transactions t
            INNER JOIN tracker.Merchants m 
                ON t.merchant_id = m.merchant_id
            INNER JOIN tracker.Categories c 
                ON t.category_id = c.category_id
            {where_clause}
            GROUP BY m.merchant_name
            ORDER BY total_spent DESC;
        """

        cursor.execute(query, params)
        rows = cursor.fetchall()

        results = []
        for row in rows:
            results.append({
                "merchant_name": row[0],
                "transaction_count": int(row[1]),
                "total_spent": float(row[2]),
            })
        return results

    finally:
        cursor.close()