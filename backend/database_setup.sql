-- database_setup.sql

-- 1. CATEGORY Table
CREATE TABLE Category (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- 2. TRANSACTION Table
CREATE TABLE Transaction (
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
FROM Transaction
GROUP BY month
ORDER BY month DESC;

-- TRIGGER (SIMULA A PROCEDURE - REQUISITO)
CREATE TRIGGER update_budget_after_insert
AFTER INSERT ON Transaction
FOR EACH ROW
BEGIN
    UPDATE Budget
    SET total_spent_ever = total_spent_ever + NEW.amount
    WHERE budget_id = 1;
END;