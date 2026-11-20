import questionary
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from services import report_service
from menus import menu_utils

console = Console()

report_color = "#B88E8D"

def select_report_filters(connection):
    """
    Prompts the user for report filters.
    """

    account_id = menu_utils.select_account(connection)

    if account_id is None:
        return None

    month = menu_utils.select_month(connection)

    if month is None:
        return None

    year = menu_utils.select_year(connection)

    if year is None:
        return None

    return {
        "account_id": account_id,
        "month": month,
        "year": year
    }

def report_menu(connection):
    while True:
        console.clear()

        console.print(
            Panel(
                f"[bold {report_color}]PERSONAL FINANCE TRACKER - REPORT MENU[/bold {report_color}]\n"
                "View your monthly financial reports",
                border_style=f"{report_color}",
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
            display_spending_by_category(connection)

        elif choice == "Get Income vs Expenses":
            display_income_vs_expenses(connection)

        elif choice == "Get Top Merchants":
            display_top_merchants(connection)

def display_spending_by_category(connection):
    filters = select_report_filters(connection)

    if filters is None:
        return

    results = report_service.get_spending_by_category(connection, **filters)

    if not results:
        console.print("[yellow]No spending data found.[/yellow]")
        return

    table = Table(title="Spending by Category", border_style=report_color)

    table.add_column("Category")
    table.add_column("Total Spending", justify="right")

    for result in results:
        table.add_row(
            result["category_name"],
            f"[red]-${result['expense_amount']:,.2f}[/red]"
        )

    console.print(table)

    questionary.text("\nPress Enter to return to the reports menu.", qmark="").ask()

def display_income_vs_expenses(connection):
    filters = select_report_filters(connection)

    if filters is None:
        return

    results = report_service.get_income_vs_expenses(connection, **filters)

    net_income = results["net_income"]

    net_color = "green" if net_income >= 0 else "red"

    console.print(
        Panel(
            f"[bold green]Total Income:[/bold green] "
            f"${results['total_income']:,.2f}\n"
            f"[bold red]Total Expenses:[/bold red] "
            f"-${results['total_expenses']:,.2f}\n"
            f"[bold {net_color}]Net Income:[/bold {net_color}] "
            f"${net_income:,.2f}\n\n"
            f"[bold]Current Account Balance:[/bold] "
            f"${results['current_balance']:,.2f}",
            title="Income vs Expenses",
            border_style=report_color,
            padding=1
        )
    )

    questionary.text("\nPress Enter to return to the reports menu.", qmark="").ask()

def display_top_merchants(connection):
    filters = select_report_filters(connection)

    if filters is None:
        return

    results = report_service.get_top_merchants(connection, **filters)

    if not results:
        console.print("[yellow]No merchant spending data found.[/yellow]")
        return

    table = Table(title="Top Merchants", border_style=report_color)

    table.add_column("Rank", justify="center")
    table.add_column("Merchant")
    table.add_column("Total Spending", justify="right")

    for index, result in enumerate(results, start=1):
        table.add_row(
            str(index),
            result["merchant_name"],
            f"[red]-${result['total_spending']:,.2f}[/red]"
        )

    console.print(table)

    questionary.text("\nPress Enter to return to the reports menu.", qmark="").ask()