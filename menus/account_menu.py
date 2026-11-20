from decimal import Decimal

import questionary
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from services import account_service
from menus import menu_utils

console = Console()

account_color = "#519E8A"

def account_menu(connection):
    while True:
        console.clear()

        console.print(
            Panel(
                f"[bold {account_color}]PERSONAL FINANCE TRACKER - ACCOUNTS MENU[/bold {account_color}]\n"
                "Manage your accounts",
                border_style=f"{account_color}",
                padding=1
            )
        )

        choice = questionary.select(
            "Select an interaction:",
            choices=[
                "Get Accounts",
                "Add Account",
                "Delete Account",
                "Get Account Transactions",
                "Get Account Categories",
                "Get Account Merchants",
                "Back"
            ],
            qmark="",
            pointer="❯"
        ).ask()

        if choice is None or choice == "Back":
            return

        elif choice == "Get Accounts":
            get_account_message(connection)

        elif choice == "Add Account":
            add_account_prompt(connection)

        elif choice == "Delete Account":
            delete_account_prompt(connection)

        elif choice == "Get Account Transactions":
            get_account_transactions(connection)

        elif choice == "Get Account Categories":
            get_account_categories(connection)

        elif choice == "Get Account Merchants":
            get_account_merchants(connection)

def get_account_message(connection):
    console.clear()

    accounts = account_service.get_accounts(connection)

    console.print(
        Panel(
            f"[bold {account_color}]YOUR ACCOUNTS[/bold {account_color}]\n"
            "View all registered accounts",
            border_style=account_color
        )
    )

    if not accounts:
        console.print("\n[yellow]No accounts have been created yet...[/yellow]")

    else:
        table = Table(
            header_style=f"bold {account_color}",
            show_lines=True,
            border_style=account_color
        )

        table.add_column("ID", justify="center")
        table.add_column("Account Name")
        table.add_column("Account Type")
        table.add_column("Balance", justify="right")

        for account in accounts:
            table.add_row(
                str(account["account_id"]),
                account["account_name"],
                account["account_type"],
                f"${account['account_balance']:,.2f}"
            )

        console.print(table)

    questionary.text("\nPress Enter to return to the accounts menu.", qmark="").ask()

def add_account_prompt(connection):
    console.clear()

    console.print(
        Panel(
            f"[bold {account_color}]ADD NEW ACCOUNT[/bold {account_color}]\n"
            "Create a new account",
            border_style=f"{account_color}",
            padding=1
        )
    )

    console.print("\n[bold]Follow the prompts below to create your account.[/bold]")
    console.print(
        "[dim]Enter the following information to continue.[/dim]\n"
    )

    account_name = questionary.text(
        "Account name:",
        validate=lambda value: (
            "Account name cannot be empty."
            if not (len(value.strip()) > 0)
            else "Account name cannot be over 100 characters."
            if not (len(value.strip()) < 100)
            else True
        )
    ).ask()

    if account_name is None:
        return

    account_type = questionary.select(
        "Account type:",
        choices=[
            "Checking",
            "Savings",
            "Cash"
        ],
        qmark="",
        pointer="❯"
    ).ask()

    if account_type is None:
        return

    account_balance = questionary.text(
        "Account balance:",
        default="0.00"
    ).ask()

    if account_balance is None:
        return

    account_balance = Decimal(account_balance)

    try:
        account_id = account_service.add_account(connection, account_name.strip(), account_type, account_balance)

        console.print(
            Panel(
                f"[bold green]Account created successfully![/bold green]\n\n"
                f"Account ID: {account_id}\n"
                f"Account Name: {account_name.strip()}\n"
                f"Account Type: {account_type}\n"
                f"Starting Balance: ${account_balance:,.2f}",
                border_style="green",
                padding=1
            )
        )

    except Exception as error:
        console.print(f"\n[bold red]Failed to create account:[/bold red] {error}")

    questionary.text("\nPress Enter to return to the accounts menu.", qmark="").ask()

def delete_account_prompt(connection):
    console.clear()

    console.print(
        Panel(
            f"[bold {account_color}]DELETE AN ACCOUNT[/bold {account_color}]\n"
            "Choose an account below to delete",
            border_style=f"{account_color}",
            padding=1
        )
    )

    account_id = menu_utils.select_account(connection)

    if account_id is None:
        return

    account = account_service.get_account(connection, account_id)

    if not account:
        console.print("\n[yellow]No information found for this account.[/yellow]")

    else:
        table = Table(
            border_style=account_color,
            header_style=f"bold {account_color}",
            show_lines=True
        )

        table.add_column("ID", justify="center")
        table.add_column("Account Name")
        table.add_column("Account Type")
        table.add_column("Balance", justify="right")

        table.add_row(
            str(account["account_id"]),
            account["account_name"],
            account["account_type"],
            f"${account['account_balance']:,.2f}"
        )

        console.print(table)

        choice = questionary.select(
            "Are you sure you want to delete this account (PERMANENT):",
            choices=[
                "NO, do not delete this account",
                "YES, delete this account",
            ],
            qmark="",
            pointer="❯"
        ).ask()

        if choice is None or choice == "NO, do not delete this account":
            return

        elif choice == "YES, delete this account":
            try:
                account_service.delete_account(connection, account_id)

                console.print(f"\n[green]Account deleted successfully.[/green]")

            except Exception as error:
                console.print(f"\n[red]Failed to delete account:[/red] {error}")

    questionary.text("\nPress Enter to return to the accounts menu.", qmark="").ask()

def get_account_transactions(connection):
    console.clear()

    console.print(
        Panel(
            f"[bold {account_color}]ACCOUNT TRANSACTIONS[/bold {account_color}]\n"
            "View transactions associated with an account",
            border_style=account_color,
            padding=1
        )
    )

    account_id = menu_utils.select_account(connection)

    if account_id is None:
        return

    transactions = account_service.get_account_transactions(connection, account_id)

    console.clear()

    console.print(
        Panel(
            f"[bold {account_color}]ACCOUNT TRANSACTIONS[/bold {account_color}]",
            border_style=account_color,
            padding=1
        )
    )

    if not transactions:
        console.print("\n[yellow]No transactions found for this account.[/yellow]")

    else:
        table = Table(
            border_style=account_color,
            header_style=f"bold {account_color}",
            show_lines=True
        )

        table.add_column("ID", justify="center")
        table.add_column("Date")
        table.add_column("Category")
        table.add_column("Merchant")
        table.add_column("Description")
        table.add_column("Amount", justify="right")

        for transaction in transactions:
            is_income = transaction["category_type"] == "Income"

            amount = transaction["transaction_amount"]
            formatted_amount = (
                f"[green]+${amount:.2f}[/green]"
                if is_income
                else f"[red]-${amount:.2f}[/red]"
            )

            table.add_row(
                str(transaction["transaction_id"]),
                transaction["transaction_date"].strftime("%m/%d/%Y"),
                transaction["category_name"],
                transaction["merchant_name"] or "N/A",
                transaction["transaction_description"] or "N/A",
                formatted_amount
            )

        console.print(table)

    questionary.text("\nPress Enter to return to the accounts menu.", qmark="").ask()

def get_account_categories(connection):
    console.clear()

    console.print(
        Panel(
            f"[bold {account_color}]ACCOUNT CATEGORIES[/bold {account_color}]\n"
            "View categories used by an account",
            border_style=account_color,
            padding=1
        )
    )

    account_id = menu_utils.select_account(connection)

    if account_id is None:
        return

    categories = account_service.get_account_categories(connection, account_id)

    console.clear()

    console.print(
        Panel(
            f"[bold {account_color}]ACCOUNT CATEGORIES[/bold {account_color}]",
            border_style=account_color,
            padding=1
        )
    )

    if not categories:
        console.print("\n[yellow]No categories found for this account.[/yellow]")

    else:
        table = Table(
            border_style=account_color,
            header_style=f"bold {account_color}",
            show_lines=True
        )

        table.add_column("ID", justify="center")
        table.add_column("Category Name")
        table.add_column("Category Type")

        for category in categories:
            category_color = (
                "green" if category["category_type"] == "Income"
                else "red"
            )

            table.add_row(
                str(category["category_id"]),
                category["category_name"],
                f"[{category_color}]{category['category_type']}[/{category_color}]"
            )

        console.print(table)

    questionary.text("\nPress Enter to return to the accounts menu.", qmark="").ask()

def get_account_merchants(connection):
    console.clear()

    console.print(
        Panel(
            f"[bold {account_color}]ACCOUNT MERCHANTS[/bold {account_color}]\n"
            "View merchants used by an account",
            border_style=account_color,
            padding=1
        )
    )

    account_id = menu_utils.select_account(connection)

    if account_id is None:
        return

    merchants = account_service.get_account_merchants(connection, account_id)

    console.clear()

    console.print(
        Panel(
            f"[bold {account_color}]ACCOUNT MERCHANTS[/bold {account_color}]",
            border_style=account_color,
            padding=1
        )
    )

    if not merchants:
        console.print("\n[yellow]No merchants found for this account.[/yellow]")

    else:
        table = Table(
            border_style=account_color,
            header_style=f"bold {account_color}",
            show_lines=True
        )

        table.add_column("ID", justify="center")
        table.add_column("Merchant Name")

        for merchant in merchants:
            table.add_row(
                str(merchant["merchant_id"]),
                merchant["merchant_name"]
            )

        console.print(table)

    questionary.text("\nPress Enter to return to the accounts menu.", qmark="").ask()