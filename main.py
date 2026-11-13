import questionary
from rich.console import Console
from rich.panel import Panel

from database.database import get_connection

from menus.account_menu import account_menu
from menus.transaction_menu import transaction_menu
from menus.budget_menu import budget_menu
from menus.report_menu import report_menu

console = Console()

def main_menu(connection):
    while True:
        console.clear()

        console.print(
            Panel(
                "[bold green]PERSONAL FINANCE TRACKER[/bold green]\n"
                "[dim]Manage your accounts, transactions, and budgets[/dim]",
                border_style="green",
                padding=1
            )
        )

        choice = questionary.select(
            "Select a category:",
            choices=[
                "Accounts",
                "Transactions",
                "Budgets",
                "Reports",
                "Exit"
            ],
            qmark="",
            pointer="❯"
        ).ask()

        if choice is None or choice == "Exit":
            break

        elif choice == "Accounts":
            account_menu(connection)

        elif choice == "Transactions":
            transaction_menu(connection)

        elif choice == "Budgets":
            budget_menu(connection)

        elif choice == "Reports":
            report_menu(connection)

def main():
    connection = None

    try:
        connection = get_connection()

        console.print("[green]Successfully connected to the database![/green]")

        cursor = connection.cursor()

        cursor.execute("SELECT DB_NAME()")

        database_name = cursor.fetchone()[0]

        console.print(f"[dim]Connected database: {database_name}[/dim]")

        main_menu(connection)

    except Exception as error:
        console.print(f"[red]Failed to connect to the database: {error}[/red]")

    finally:
        if connection:
            connection.close()
            console.print("[dim]Database connection closed.[/dim]")

if __name__ == "__main__":
    main_menu("test")