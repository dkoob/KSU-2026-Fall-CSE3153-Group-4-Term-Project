import questionary
from rich.console import Console
from rich.panel import Panel

from services import account_service

console = Console()

def account_menu(connection):
    console.clear()

    console.print(
        Panel(
            "[bold cyan]PERSONAL FINANCE TRACKER - ACCOUNTS MENU[/bold cyan]\n"
            "[dim]Manage your account[/dim]",
            border_style="cyan",
            padding=1
        )
    )

    choice = questionary.select(
        "Select an interaction:",
        choices=[
            "Get Accounts",
            "Add Account",
            "Get Account Balance",
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