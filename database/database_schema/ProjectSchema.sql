/* =========================================================
   CSE 3153 - Group 4 Project Schema
   Project: Personal Finance Tracker
   Database: CSE3153_Group4_Finance_Tracker
   Schema: tracker
   ========================================================= */

-- ==========================================
-- Section 1: Creating the database and schema
-- ==========================================

-- #1.1: Switch to the system database so the project database can be created or dropped.
USE master;
GO

-- #1.2: Drop the existing project database, if it exists.
IF DB_ID(N'CSE3153_Group4_Finance_Tracker') IS NOT NULL
BEGIN
    ALTER DATABASE CSE3153_Group4_Finance_Tracker
        SET SINGLE_USER WITH ROLLBACK IMMEDIATE;

    DROP DATABASE CSE3153_Group4_Finance_Tracker;
END;
GO

-- #1.3: Create the project database.
CREATE DATABASE CSE3153_Group4_Finance_Tracker;
GO

-- #1.4: Select the project database for the remaining statements.
USE CSE3153_Group4_Finance_Tracker;
GO

-- #1.5: Create the application-specific schema.
CREATE SCHEMA tracker;
GO

-- ==========================================
-- Section 2: Creating tables
-- ==========================================

-- #2.1: Create the Accounts table.
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

-- #2.2: Create the Categories table.
CREATE TABLE tracker.Categories (
    category_id         INT IDENTITY(1,1) NOT NULL,
    category_name       VARCHAR(50) NOT NULL,
    category_type       VARCHAR(20) NOT NULL,

    CONSTRAINT PK_Categories PRIMARY KEY (category_id),
    CONSTRAINT UQ_Categories_CategoryName UNIQUE (category_name),
    CONSTRAINT CK_Categories_CategoryType CHECK (category_type IN ('Income', 'Expense'))
);
GO

-- #2.3: Create the Merchants table.
CREATE TABLE tracker.Merchants (
    merchant_id         INT IDENTITY(1,1) NOT NULL,
    merchant_name       VARCHAR(100) NOT NULL,

    CONSTRAINT PK_Merchants PRIMARY KEY (merchant_id),
    CONSTRAINT UQ_Merchants_MerchantNamae UNIQUE (merchant_name)
);
GO

-- #2.4: Create the Transactions table.
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

-- #2.5: Create the Budgets table.
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

-- ==========================================
-- Section 3: Populating tables with initial data
-- ==========================================

-- #3.1: Insert data into Accounts table.
INSERT INTO tracker.Accounts
    (account_name, account_type, starting_balance)
VALUES
    ('John_Checking', 'Checking', 1500.00),
    ('John_Savings', 'Savings', 5000.00),
    ('John_Cash', 'Cash', 100.00);
GO

-- #3.2 Insert data into Categories table.
INSERT INTO tracker.Categories
    (category_name, category_type)
VALUES
    ('Groceries', 'Expense'),
    ('Dining', 'Expense'),
    ('Transportation', 'Expense'),
    ('Entertainment', 'Expense'),
    ('Utilities', 'Expense'),
    ('Rent', 'Expense'),
    ('Salary', 'Income'),
    ('Freelance', 'Income');
GO

-- #3.3 Insert data into Merchants table.
INSERT INTO tracker.Merchants
    (merchant_name)
VALUES
    ('Kroger'),
    ('Amazon'),
    ('Georgia Power'),
    ('Quick Trip'),
    ('Landlord');
GO

-- #3.4 Insert data into Transactions. 
-- (All amounts are positive, the category determines if the transaction is income or expense)
INSERT INTO tracker.Transactions
    (account_id, category_id, merchant_id, amount, transaction_date, description)
VALUES
    (1, 7, NULL,    2400.00,    '2026-11-01T09:00:00',      'Monthly paycheck'),
    (1, 1, 1,       86.42,      '2026-11-02T17:30:00',      'Weekly grocery shopping'),
    (1, 2, NULL,    28.75,      '2026-11-03T19:15:00',      'Dinner with friends'),
    (1, 3, 4,       42.10,      '2026-11-04T08:20:00',      'Gas for car'),
    (1, 4, 2,       34.99,      '2026-11-05T14:10:00',      'Headphones'),
    (1, 5, 3,       78.35,      '2026-11-06T10:00:00',      'Monthly electricity bill'),
    (1, 6, 5,       950.00,     '2026-11-01T08:00:00',      'November rent payment'),
    (2, 7, NULL,    500.00,     '2026-11-01T09:05:00',      'Paycheck deposit to savings'),
    (2, 8, NULL,    175.00,     '2026-11-07T16:00:00',      'Freelance design work'),
    (2, 1, 1,       54.28,      '2026-11-08T12:40:00',      'Groceries for the week'),
    (3, 2, NULL,    16.50,      '2026-11-08T18:30:00',      'Lunch'),
    (3, 3, 4,       20.00,      '2026-11-09T07:45:00',      'Fuel'),
    (1, 1, 1,       63.17,      '2026-11-11T16:25:00',      'Household groceries');
GO

-- #3.5 Insert data into Budgets.
INSERT INTO tracker.Budgets
    (account_id, category_id, monthly_limit, [month], [year])
VALUES
    (1, 1, 400.00, 11, 2026),  -- 400 on groceries
    (1, 2, 180.00, 11, 2026),  -- 180 on dining
    (1, 3, 120.00, 11, 2026),  -- 120 on transportation
    (1, 4, 100.00, 11, 2026),  -- 100 on entertainment
    (1, 5, 150.00, 11, 2026),  -- 150 on utilities
    (1, 6, 1000.00, 11, 2026); -- 1000 on rent
GO
