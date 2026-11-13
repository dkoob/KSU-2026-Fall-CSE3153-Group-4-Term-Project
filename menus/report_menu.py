import questionary
from rich.console import Console
from rich.panel import Panel

from services import report_service

console = Console()

def report_menu(connection):
    console.clear()

    console.print(
        Panel(
            "[bold cyan]PERSONAL FINANCE TRACKER - REPORT MENU[/bold cyan]\n"
            "[dim]Manage your reports[/dim]",
            border_style="cyan",
            padding=1
        )
    )

    choice = questionary.select(
        "Select an interaction:",
        choices=[
            "Get Spending By Category",
            "Get Income vs Expenses",
            "Get Top Merchants",
            "Back"
        ],
        qmark="",
        pointer="❯"
    ).ask()

    if choice is None or choice == "Back":
        return

    elif choice == "Get Spending By Category":
        pass

    elif choice == "Get Income vs Expenses":
        pass

    elif choice == "Get Top Merchants":
        pass