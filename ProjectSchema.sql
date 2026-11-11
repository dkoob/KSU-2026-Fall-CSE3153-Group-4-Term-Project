/* =========================================================
   CSE 3153 - Group 4 Project Schema
   Project: Personal Finance Tracker
   Database: CSE3153_Group4_Finance_Tracker
   Schema: tracker
   ========================================================= */

-- #1: Switch to the system database so the project database can be created or dropped.
USE master;
GO

-- #2: Drop the existing project database, if it exists.
IF DB_ID(N'CSE3153_Group4_Finance_Tracker') IS NOT NULL
BEGIN
    ALTER DATABASE CSE3153_Group4_Finance_Tracker
        SET SINGLE_USER WITH ROLLBACK IMMEDIATE;

    DROP DATABASE CSE3153_Group4_Finance_Tracker;
END;
GO

-- #3: Create the project database.
CREATE DATABASE CSE3153_Group4_Finance_Tracker;
GO

-- #4: Select the project database for the remaining statements.
USE CSE3153_Group4_Finance_Tracker;
GO

-- #5: Create the application-specific schema.
CREATE SCHEMA tracker;
GO

-- #6: Create the Accounts table.
CREATE TABLE tracker.Accounts (
    account_id          INT IDENTITY(1,1) NOT NULL,
    account_name        VARCHAR(100) NOT NULL,
    account_type        VARCHAR(30) NOT NULL,

    starting_balance    DECIMAL(10,2) NOT NULL
        CONSTRAINT DF_Accounts_StartingBalance DEFAULT (0.00),

    created_at          DATETIME2 NOT NULL
        CONSTRAINT DF_Accounts_CreatedAt DEFAULT (SYSDATETIME()),

    CONSTRAINT PK_Accounts PRIMARY KEY (account_id),
    CONSTRAINT UQ_Accounts_AccountName UNIQUE (account_name),
    CONSTRAINT CK_Accounts_AccountType CHECK (account_type IN ('Checking', 'Savings', 'Cash'))
);
GO

-- #7: Create the Categories table.
CREATE TABLE tracker.Categories (
    category_id         INT IDENTITY(1,1) NOT NULL,
    category_name       VARCHAR(50) NOT NULL,
    category_type       VARCHAR(20) NOT NULL,

    CONSTRAINT PK_Categories PRIMARY KEY (category_id),
    CONSTRAINT UQ_Categories_CategoryName UNIQUE (category_name),
    CONSTRAINT CK_Categories_CategoryType CHECK (category_type IN ('Income', 'Expense'))
);
GO

-- #8: Create the Merchants table.
CREATE TABLE tracker.Merchants (
    merchant_id         INT IDENTITY(1,1) NOT NULL,
    merchant_name       VARCHAR(100) NOT NULL,

    CONSTRAINT PK_Merchants PRIMARY KEY (merchant_id),
    CONSTRAINT UQ_Merchants_MerchantNamae UNIQUE (merchant_name)
);
GO

-- #9: Create the Transactions table.
CREATE TABLE tracker.Transactions
(
    transaction_id      INT IDENTITY(1,1) NOT NULL,
    account_id          INT NOT NULL,
    category_id         INT NOT NULL,
    merchant_id         INT NULL,
    amount              DECIMAL(10,2) NOT NULL,
    transaction_date    DATETIME2 NOT NULL,
    description         VARCHAR(255) NULL,

    created_at             DATETIME2 NOT NULL
        CONSTRAINT DF_Transactions_CreatedAt DEFAULT (SYSDATETIME()),

    CONSTRAINT PK_Transactions PRIMARY KEY (transaction_id),
    CONSTRAINT FK_Transactions_Accounts
        FOREIGN KEY (account_id) REFERENCES tracker.Accounts (account_id),
    CONSTRAINT FK_Transactions_Categories
        FOREIGN KEY (category_id) REFERENCES tracker.Categories (category_id),
    CONSTRAINT FK_Transactions_Merchants
        FOREIGN KEY (merchant_id) REFERENCES tracker.Merchants (merchant_id),
    CONSTRAINT CK_Transactions_Amount CHECK (amount > 0)
);
GO

-- #10: Create the Budgets table.
CREATE TABLE tracker.Budgets
(
    budget_id           INT IDENTITY(1,1) NOT NULL,
    account_id          INT NOT NULL,
    category_id         INT NOT NULL,
    monthly_limit       DECIMAL(10,2) NOT NULL,
    [month]             INT NOT NULL,
    [year]              INT NOT NULL,

    CONSTRAINT PK_Budgets PRIMARY KEY (budget_id),
    CONSTRAINT FK_Budgets_Accounts
        FOREIGN KEY (account_id) REFERENCES tracker.Accounts (account_id),
    CONSTRAINT FK_Budgets_Categories
        FOREIGN KEY (category_id) REFERENCES tracker.Categories (category_id),
    CONSTRAINT CK_Budgets_MonthlyLimit CHECK (monthly_limit > 0),
    CONSTRAINT CK_Budgets_Month CHECK ([month] BETWEEN 1 AND 12),
    CONSTRAINT CK_Budgets_Year CHECK ([year] >= 1),
    CONSTRAINT UQ_Budgets_AccountCategoryMonthYear
        UNIQUE (account_id, category_id, [month], [year])
);
GO
