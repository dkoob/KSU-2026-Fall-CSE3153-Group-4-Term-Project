from decimal import Decimal

def _rows_to_dicts(cursor) -> list[dict]:
    """
    Helper: turns the rows from the last query into a list of dictionaries,
    using the column names as keys. Example: {"account_id": 1, "account_name": "John_Checking", ...}
    """
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def get_accounts(connection) -> list[dict]:
    """
    Retrieve all accounts.
    Returns a list of account records.

    Should return:
    account id
    account name
    account type
    account balance
    created at
    """

    cursor = connection.cursor()

    try:
        cursor.execute("""
        SELECT
            account_id,
            account_name,
            account_type,
            account_balance,
            created_at
        FROM tracker.Accounts
        ORDER BY account_id;
        """)

        return _rows_to_dicts(cursor)

    finally:
        cursor.close()

def get_account(connection, account_id: int) -> dict | None:
    """
    Retrieves a single account.

    Should return:
    account id
    account name
    account type
    account balance
    created at
    """

    cursor = connection.cursor()

    try:
        cursor.execute("""
        SELECT account_id,
            account_name,
            account_type,
            account_balance,
            created_at
        FROM tracker.Accounts
        WHERE account_id = ?;
        """, account_id)

        row = cursor.fetchone()

        if row is None:
            return None

        columns = [column[0] for column in cursor.description]
        return dict(zip(columns, row))

    finally:
        cursor.close()

def add_account(connection, account_name: str, account_type: str, account_balance: float = 0.00) -> int | None:
    """
    Create a new account.
    Returns the new account ID, or 'None' if unsuccessful.
    """

    cursor = connection.cursor()

    try:
        cursor.execute("""
        INSERT INTO tracker.Accounts (
            account_name, 
            account_type, 
            account_balance
        )
        OUTPUT INSERTED.account_id
        VALUES (?, ?, ?);
        """, (account_name, account_type, account_balance))

        account_id = cursor.fetchone()[0]

        connection.commit()

        return account_id

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()

def delete_account(connection, account_id: int) -> None:
    """
    Deletes the specified account.
    """

    cursor = connection.cursor()

    try:
        cursor.execute("""
        DELETE FROM tracker.Accounts 
        WHERE account_id = ?;
        """, (account_id,))

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()

def get_account_balance(connection, account_id: int) -> Decimal | None:
    cursor = connection.cursor()

    """
    Retrieve an account's current balance.
    Returns the balance, or None if the account does not exist.
    """
    cursor.execute("""
        SELECT account_balance
        FROM tracker.Accounts
        WHERE account_id = ?
    """, (account_id,))
    row = cursor.fetchone()
    return row[0] if row else None

def get_account_transactions(connection, account_id: int) -> list[dict]:
    """
    Retrieve all transactions belonging to a specific account.
    Returns a list of transaction records.

    Should return:
    transaction id
    transaction amount
    transaction description
    category name
    category type
    merchant name
    """

    cursor = connection.cursor()

    try:
        cursor.execute("""
        SELECT
            t.transaction_id,
            t.transaction_amount,
            t.transaction_date,
            t.transaction_description,
            c.category_name,
            c.category_type,
            m.merchant_name
        FROM tracker.Transactions AS t
        INNER JOIN tracker.Categories AS c
            ON t.category_id = c.category_id
        LEFT JOIN tracker.Merchants AS m
            ON t.merchant_id = m.merchant_id
        WHERE t.account_id = ?
        ORDER BY t.transaction_date DESC;
        """, (account_id,))

        return _rows_to_dicts(cursor)

    finally:
        cursor.close()

def get_account_categories(connection, account_id: int) -> list[dict]:
    """
    Retrieve available categories used by an account.
    """

    cursor = connection.cursor()

    try:
        cursor.execute("""
        SELECT DISTINCT
            c.category_id,
            c.category_name,
            c.category_type
        FROM tracker.Categories AS c
        INNER JOIN tracker.Transactions AS t
            ON t.category_id = c.category_id
        WHERE t.account_id = ?
        ORDER BY c.category_type, c.category_name;
        """, (account_id,))

        return _rows_to_dicts(cursor)

    finally:
        cursor.close()

def get_categories(connection) -> list[dict]:
    """
    Retrieve all available categories.
    """

    cursor = connection.cursor()

    try:
        cursor.execute("""
        SELECT DISTINCT
            category_id,
            category_name,
            category_type
        FROM tracker.Categories
        ORDER BY category_type, category_name;
        """)

        return _rows_to_dicts(cursor)

    finally:
        cursor.close()

def create_category(connection, category_name, category_type) -> int | None:
    """
    Creates a new category with the specified name and type, returning the id.
    """

    cursor = connection.cursor()

    try:
        cursor.execute("""
        INSERT INTO tracker.Categories (
            category_name,
            category_type
        )
        OUTPUT INSERTED.category_id
        VALUES (?, ?);
        """, (category_name, category_type))

        category_id = cursor.fetchone()[0]

        connection.commit()

        return category_id

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()

def create_merchant(connection, merchant_name) -> int | None:
    """
    Creates a new merchant with the specified name, returning the id.
    """

    cursor = connection.cursor()

    try:
        cursor.execute("""
        INSERT INTO tracker.Merchants (
            merchant_name
        )
        OUTPUT INSERTED.merchant_id
        VALUES (?);
        """, merchant_name)

        merchant_id = cursor.fetchone()[0]

        connection.commit()

        return merchant_id

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()

def get_account_merchants(connection, account_id: int) -> list[dict]:
    """
    Retrieve all distinct merchants used by an account.
    """

    cursor = connection.cursor()

    try:
        cursor.execute("""
        SELECT DISTINCT
            m.merchant_id,
            m.merchant_name
        FROM tracker.Merchants AS m
        INNER JOIN tracker.Transactions AS t
            ON m.merchant_id = t.merchant_id
        WHERE t.account_id = ?
        ORDER BY m.merchant_name;
        """, (account_id,))

        return _rows_to_dicts(cursor)

    finally:
        cursor.close()

def get_merchants(connection) -> list[dict] | None:
    """
    Retrieve all merchants.
    """

    cursor = connection.cursor()

    try:
        cursor.execute("""
        SELECT DISTINCT 
            merchant_id,
            merchant_name
        FROM tracker.Merchants 
        ORDER BY merchant_id;
        """)

        return _rows_to_dicts(cursor)

    finally:
        cursor.close()
