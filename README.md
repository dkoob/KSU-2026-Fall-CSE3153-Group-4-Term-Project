# KSU-2026-Fall-CSE3153-Group-4-Term-Project

## Personal Finance Tracker Idea
### Overview
This app is a super simple, console-based finance tracking application that allows
users to track income, expenses, accounts, and monthly budgets. The application
serves as an organized way to record financial transactions and view their spending habits
through basic reports and summaries.

The project will use a Python console application connected to a Microsoft SQL Server Database.
All financial records are stored persistently in the database rather than through temporary
application memory.

### Features
* **Transaction Management**: Create, view, update, and delete transaction records.
* **Spending Reports**: View spending totals organized by category using database queries and aggregate functions.
* **Budget Tracking**: Users can save monthly spending limits for individual categories and view their remaining budgets.
* **Account Management**: View financial accounts and the transactions associated with them.
* **Financial Summaries**: Review basic reports on account balances and spending activity.

### Database Design
This application will use a Microsoft SQL Server Database that consists of five tables:
* **Accounts**: Stores the user's accounts (checking, savings, cash).
* **Categories**: Organizes spending into categories, such as dining, groceries, and entertainment.
* **Merchants**: Stores the businesses associated with transactions.
* **Transactions**: Records individual income and expense transactions, including the associated accounts, categories, and merchants.
* **Budgets**: Stores the user's set monthly spending limits associated with each individual category.

Many of these tables will be connected to each other through primary and foreign keys.

### Tentative Project Structure
* **ProjectSchema.sql** - Creates the database, schema, tables, relationships, and three rows of sample data per table.
* **main.py** - Application's entry point and sentinel loop for the console menu.
* **database.py** - Handles the SQL Sever database connection and query execution.
* **transaction_service.py** - Handles transaction related operations.
* **report_service.py** - Generates the financial and account reports and summaries.
* **budget_service.py** - Handles the monthly budget management.

If we are all on board with this idea, we can split the work in a way where everyone can work mostly independent of each other.