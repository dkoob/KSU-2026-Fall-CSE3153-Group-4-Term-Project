import questionary
from rich.console import Console
from rich.panel import Panel

from services import budget_service

console = Console()

def budget_menu(connection):
    console.clear()

    console.print(
        Panel(
            "[bold cyan]PERSONAL FINANCE TRACKER - BUDGET MENU[/bold cyan]\n"
            "[dim]Manage your budgets[/dim]",
            border_style="cyan",
            padding=1
        )
    )

    choice = questionary.select(
        "Select an interaction:",
        choices=[
            "Set Budget",
            "Get Budgets",
            "Calculate Remaining Budget",
            "Back"
        ],
        qmark="",
        pointer="❯"
    ).ask()

    if choice is None or choice == "Back":
        return

    elif choice == "Set Budget":
        pass

    elif choice == "Get Budgets":
        pass

    elif choice == "Calculate Remaining Budget":
        pass