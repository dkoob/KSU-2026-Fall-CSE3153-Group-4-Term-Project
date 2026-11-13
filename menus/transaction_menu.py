import questionary
from rich.console import Console
from rich.panel import Panel

from services import transaction_service

console = Console()

def transaction_menu(connection):
    console.clear()

    console.print(
        Panel(
            "[bold cyan]PERSONAL FINANCE TRACKER - TRANSACTION MENU[/bold cyan]\n"
            "[dim]Manage your transactions[/dim]",
            border_style="cyan",
            padding=1
        )
    )

    choice = questionary.select(
        "Select an interaction:",
        choices=[
            "Add Transaction",
            "Delete Transaction",
            "Update Transaction",
            "Get Transactions",
            "Back"
        ],
        qmark="",
        pointer="❯"
    ).ask()

    if choice is None or choice == "Back":
        return