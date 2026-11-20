import datetime
from decimal import Decimal, InvalidOperation

from services import services_utils

def add_transaction(connection, account_id: int, category_id: int, amount: Decimal, transaction_date: datetime.datetime = None, merchant_id: int = None, description: str = None) -> dict | None:
    """
    Create a new transaction and update the account balance.
    Returns the new transaction record, or None if unsuccessful.
    """

    cursor = connection.cursor()

    try:
        cursor.execute("""
        SELECT category_type
        FROM tracker.Categories
        WHERE category_id = ?;
        """, (category_id,))

        category = cursor.fetchone()

        if category is None:
            return None

        category_type = category[0]

        try:
            amount = Decimal(str(amount))
        except (InvalidOperation, TypeError, ValueError):
            raise ValueError("Please enter a valid transaction amount.")

        if amount <= 0:
            raise ValueError("Transaction amount must be greater than zero.")

        if transaction_date is None:
            transaction_date = datetime.datetime.now()

        cursor.execute("""
        INSERT INTO tracker.Transactions (
            account_id,
            category_id,
            merchant_id,
            transaction_amount,
            transaction_date,
            transaction_description
        )
        OUTPUT INSERTED.transaction_id
        VALUES (?, ?, ?, ?, ?, ?);
        """, (account_id, category_id, merchant_id, amount, transaction_date, description))

        transaction_id = cursor.fetchone()[0]

        if category_type == "Income":
            cursor.execute("""
            UPDATE tracker.Accounts
            SET account_balance = account_balance + ?
            WHERE account_id = ?;
            """, (amount, account_id))
        else:
            cursor.execute("""
            UPDATE tracker.Accounts
            SET account_balance = account_balance - ?
            WHERE account_id = ?;
            """, (amount, account_id))

        connection.commit()

        return services_utils.get_transaction(connection, transaction_id)

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()

def update_transaction(connection, transaction_id: int, account_id: int | None, category_id: int | None, updated_amount: Decimal | None, transaction_date: datetime.datetime | None, merchant_id: int | None, description: str | None) -> dict | None:
    """
    Update an existing transaction using its ID.
    Returns True if updated, otherwise False.

    This one may be tricky because the account balances will also have to be updated if a transaction's amount is updated.
    So if the transaction is changed to have costed more, subtract more from the balance, if the transaction is less now, add to the balance.
    """

    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                t.account_id,
                t.category_id,
                t.merchant_id,
                t.transaction_amount,
                t.transaction_date,
                t.transaction_description,
                c.category_type
            FROM tracker.Transactions AS t
            INNER JOIN tracker.Categories AS c
                ON t.category_id = c.category_id
            WHERE t.transaction_id = ?;
        """, (transaction_id,))

        row = cursor.fetchone()

        if row is None:
            return None

        (
            prev_account_id,
            prev_category_id,
            prev_merchant_id,
            prev_amount,
            prev_date,
            prev_description,
            prev_category_type,
        ) = row

        new_account_id = account_id if account_id is not None else prev_account_id
        new_category_id = category_id if category_id is not None else prev_category_id
        new_merchant_id = merchant_id if merchant_id is not None else prev_merchant_id
        new_amount = prev_amount
        new_date = transaction_date if transaction_date is not None else prev_date
        new_description = description if description is not None else prev_description

        if updated_amount is not None:
            try:
                new_amount = Decimal(str(updated_amount))

            except (InvalidOperation, TypeError, ValueError):
                raise ValueError(f"Invalid transaction amount: {updated_amount}")

            if not new_amount.is_finite() or new_amount <= 0:
                raise ValueError(f"Transaction amount must be greater than zero.")

        cursor.execute("""
            SELECT category_type
            FROM tracker.Categories
            WHERE category_id = ?;
        """, (new_category_id,))

        category_row = cursor.fetchone()

        if category_row is None:
            raise ValueError("Invalid transaction category.")

        new_category_type = category_row[0]

        prev_effect = (
            prev_amount
            if prev_category_type == "Income"
            else -prev_amount
        )

        new_effect = (
            new_amount
            if new_category_type == "Income"
            else -new_amount
        )

        balance_changes = {}

        balance_changes[prev_account_id] = -prev_effect

        balance_changes[new_account_id] = (balance_changes.get(new_account_id, Decimal("0")) + new_effect)

        for affected_account_id, balance_change in balance_changes.items():
            cursor.execute("""
                UPDATE tracker.Accounts
                SET account_balance = account_balance + ?
                WHERE account_id = ?;
            """, (balance_change, affected_account_id))

        cursor.execute("""
            UPDATE tracker.Transactions
            SET
                account_id = ?,
                category_id = ?,
                merchant_id = ?,
                transaction_amount = ?,
                transaction_date = ?,
                transaction_description = ?
            WHERE transaction_id = ?;
        """, (
            new_account_id,
            new_category_id,
            new_merchant_id,
            new_amount,
            new_date,
            new_description,
            transaction_id
        ))

        cursor.execute("""
            SELECT
                t.*,
                a.account_name,
                c.category_name,
                c.category_type,
                m.merchant_name
            FROM tracker.Transactions AS t
            INNER JOIN tracker.Accounts AS a
                ON t.account_id = a.account_id
            INNER JOIN tracker.Categories AS c
                ON t.category_id = c.category_id
            LEFT JOIN tracker.Merchants AS m
                ON t.merchant_id = m.merchant_id
            WHERE t.transaction_id = ?;
        """, (transaction_id,))

        row = cursor.fetchone()

        if row is None:
            connection.rollback()
            return None

        columns = [column[0] for column in cursor.description]
        transaction = dict(zip(columns, row))

        connection.commit()

        return transaction

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()

def delete_transaction(connection, transaction_id: int) -> bool:
    """
    Delete a transaction using its ID.
    Reverses the transaction's effect on the account balance.
    Returns True if deleted, otherwise False.
    """

    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                t.account_id,
                t.transaction_amount,
                c.category_type
            FROM tracker.Transactions AS t
            INNER JOIN tracker.Categories AS c
                ON t.category_id = c.category_id
            WHERE t.transaction_id = ?;
        """, (transaction_id,))

        row = cursor.fetchone()

        if row is None:
            return False

        account_id, amount, category_type = row

        if category_type == "Income":
            amount = -amount

        cursor.execute("""
            UPDATE tracker.Accounts
            SET account_balance = account_balance + ?
            WHERE account_id = ?;
        """, (amount, account_id))

        cursor.execute("""
            DELETE FROM tracker.Transactions
            WHERE transaction_id = ?;
        """, (transaction_id,))

        connection.commit()
        return True

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
