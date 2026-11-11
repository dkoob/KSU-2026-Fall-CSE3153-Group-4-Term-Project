/* =========================================================
   CSE 3153 - Group 4 Project Schema - Personal Finance Tracker
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
    account_id          INT IDENTITIY(1,1) NOT NULL,
    account_name        VARCHAR(100) NOT NULL,
    account_type        VARCHAR(30) NOT NULL,

    starting_balance    DECIMAL(10,2) NOT NULL
        CONSTRAINT DF_Accounts_StartingBalance DEFAULT (0.00),

    created_at          DATETIME2 NOT NULL
        CONSTRAINT DF_Accounts_CreatedAt DEFAULT (SYSDATETIME()),

    CONSTRAINT PK_Accounts PRIMARY KEY (account_id),
    CONSTRAINT UQ_Accounts_AccountName UNIQUE (account_name),
    CONSTRAINT CK_Accounts_AccountType
        CHECK (account_type IN ('Checking', 'Savings', 'Cash'))
);
GO