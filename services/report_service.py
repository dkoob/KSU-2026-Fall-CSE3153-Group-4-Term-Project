from decimal import Decimal

def _build_report_filters(account_id = None, month = None, year = None):
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

    where_clause = (
        "WHERE " + " AND ".join(conditions)
        if conditions
        else ""
    )

    return where_clause, params

def get_spending_by_category(connection, account_id: int = None, month: int = None, year: int = None) -> list[dict]:
    """
    Retrieve total expenses grouped by category.
    Optionally filter by account and month/year.
    Returns category names and expense totals.
    """

    cursor = connection.cursor()

    try:
        where_clause, params = _build_report_filters(account_id, month, year)

        query = f"""
            SELECT
                c.category_name,
                SUM(t.transaction_amount) AS expense_amount
            FROM tracker.Transactions AS t
            INNER JOIN tracker.Categories AS c
                ON t.category_id = c.category_id
            {where_clause}
            {"AND" if where_clause else "WHERE"} c.category_type = 'Expense'
            GROUP BY c.category_name
            ORDER BY expense_amount DESC;
        """

        cursor.execute(query, params)

        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()

        return [dict(zip(columns, row)) for row in rows]

    finally:
        cursor.close()

def get_income_vs_expenses(connection, account_id: int = None, month: int = None, year: int = None) -> dict:
    """
    Retrieve total income, expenses, and net income.
    Expenses are returned as positive totals.
    Also returns the current account balance, regardless of date filters.
    """

    cursor = connection.cursor()

    try:
        where_clause, params = _build_report_filters(account_id, month, year)

        cursor.execute(f"""
            SELECT
                COALESCE(SUM(
                    CASE
                        WHEN c.category_type = 'Income'
                        THEN t.transaction_amount
                        ELSE 0
                    END
                ), 0) AS total_income,

                COALESCE(SUM(
                    CASE
                        WHEN c.category_type = 'Expense'
                        THEN t.transaction_amount
                        ELSE 0
                    END
                ), 0) AS total_expenses

            FROM tracker.Transactions AS t
            INNER JOIN tracker.Categories AS c
                ON t.category_id = c.category_id
            {where_clause};
        """, params)

        row = cursor.fetchone()

        total_income = row[0]
        total_expenses = row[1]

        if account_id is not None:
            cursor.execute("""
                SELECT account_balance
                FROM tracker.Accounts
                WHERE account_id = ?;
            """, (account_id,))

            balance_row = cursor.fetchone()
            current_balance = balance_row[0] if balance_row else Decimal("0")

        else:
            cursor.execute("""
                SELECT COALESCE(SUM(account_balance), 0)
                FROM tracker.Accounts;
            """)

            current_balance = cursor.fetchone()[0]

        return {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net_income": total_income - total_expenses,
            "current_balance": current_balance
        }

    finally:
        cursor.close()


def get_top_merchants(connection, account_id: int = None, month: int = None, year: int = None, limit: int = 5) -> list[dict]:
    """
    Retrieve merchants ranked by total transaction spending.
    Optionally filter by account and month/year.
    Returns merchant names and spending totals.
    """

    if limit < 1:
        raise ValueError("Limit must be greater than zero.")

    cursor = connection.cursor()

    try:
        where_clause, params = _build_report_filters(account_id, month, year)

        query = f"""
            SELECT
                m.merchant_name,
                SUM(t.transaction_amount) AS total_spending
            FROM tracker.Transactions AS t
            INNER JOIN tracker.Categories AS c
                ON t.category_id = c.category_id
            INNER JOIN tracker.Merchants AS m
                ON t.merchant_id = m.merchant_id
            {where_clause}
            {"AND" if where_clause else "WHERE"} c.category_type = 'Expense'
            GROUP BY m.merchant_name
            ORDER BY total_spending DESC
            OFFSET 0 ROWS FETCH NEXT ? ROWS ONLY;
        """

        cursor.execute(query, params + [limit])

        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()

        return [dict(zip(columns, row)) for row in rows]

    finally:
        cursor.close()