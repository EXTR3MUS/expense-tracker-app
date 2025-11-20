-- database_setup.sql

-- 1. CATEGORY Table
CREATE TABLE Category (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- 2. TRANSACTIONS Table
CREATE TABLE Transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL CHECK (amount > 0), -- Validação por restrição!
    description TEXT,
    date TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES Category(category_id)
);

-- 3. BUDGET Table (Suporte para o Trigger/Procedure)
CREATE TABLE Budget (
    budget_id INTEGER PRIMARY KEY,
    total_spent_ever REAL DEFAULT 0
);
INSERT INTO Budget (budget_id, total_spent_ever) VALUES (1, 0);

-- VIEW (REQUISITO)
CREATE VIEW View_Monthly_Summary AS
SELECT
    strftime('%Y-%m', date) AS month,
    SUM(amount) AS total_expenses
FROM Transactions
GROUP BY month
ORDER BY month DESC;

-- TRIGGER modifies budget after inserting a transaction
CREATE TRIGGER update_budget_after_insert
AFTER INSERT ON Transactions
FOR EACH ROW
BEGIN
    UPDATE Budget
    SET total_spent_ever = total_spent_ever + NEW.amount
    WHERE budget_id = 1;
END;

-- TRIGGER modifies budget after updating a transaction
CREATE TRIGGER update_budget_after_update
AFTER UPDATE ON Transactions
FOR EACH ROW
BEGIN
    UPDATE Budget
    SET total_spent_ever = total_spent_ever - OLD.amount + NEW.amount
    WHERE budget_id = 1;
END;

-- TRIGGER modifies budget after deleting a transaction
CREATE TRIGGER update_budget_after_delete
AFTER DELETE ON Transactions
FOR EACH ROW
BEGIN
    UPDATE Budget
    SET total_spent_ever = total_spent_ever - OLD.amount
    WHERE budget_id = 1;
END;

-- TRIGGER to log transaction inserts (for auditing)
CREATE TABLE Transaction_Log (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    operation TEXT NOT NULL,
    transaction_id INTEGER,
    old_amount REAL,
    new_amount REAL,
    old_description TEXT,
    new_description TEXT,
    old_date TEXT,
    new_date TEXT,
    old_category_id INTEGER,
    new_category_id INTEGER,
    log_timestamp TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'))
);

CREATE TRIGGER log_transaction_insert
AFTER INSERT ON Transactions
FOR EACH ROW
BEGIN
    INSERT INTO Transaction_Log (operation, transaction_id, new_amount, new_description, new_date, new_category_id)
    VALUES ('INSERT', NEW.transaction_id, NEW.amount, NEW.description, NEW.date, NEW.category_id);
END;

-- TRIGGER to log transaction updates (for auditing)
CREATE TRIGGER log_transaction_update
AFTER UPDATE ON Transactions
FOR EACH ROW
BEGIN
    INSERT INTO Transaction_Log (
        operation, transaction_id, 
        old_amount, new_amount,
        old_description, new_description,
        old_date, new_date,
        old_category_id, new_category_id
    )
    VALUES (
        'UPDATE', NEW.transaction_id,
        OLD.amount, NEW.amount,
        OLD.description, NEW.description,
        OLD.date, NEW.date,
        OLD.category_id, NEW.category_id
    );
END;

-- TRIGGER to log transaction deletions (for auditing)
CREATE TRIGGER log_transaction_delete
AFTER DELETE ON Transactions
FOR EACH ROW
BEGIN
    INSERT INTO Transaction_Log (operation, transaction_id, old_amount, old_description, old_date, old_category_id)
    VALUES ('DELETE', OLD.transaction_id, OLD.amount, OLD.description, OLD.date, OLD.category_id);
END;