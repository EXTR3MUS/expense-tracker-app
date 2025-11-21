-- PostgreSQL database setup script

-- 1. CATEGORY Table
CREATE TABLE Category (
    category_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- 2. TRANSACTIONS Table
CREATE TABLE Transactions (
    transaction_id SERIAL PRIMARY KEY,
    amount NUMERIC(10,2) NOT NULL CHECK (amount > 0),
    description TEXT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES Category(category_id) ON DELETE RESTRICT
);

-- 3. BUDGET Table
CREATE TABLE Budget (
    budget_id INTEGER PRIMARY KEY,
    total_spent_ever NUMERIC(10,2) DEFAULT 0
);
INSERT INTO Budget (budget_id, total_spent_ever) VALUES (1, 0);

-- 4. TRANSACTION LOG Table (for auditing)
CREATE TABLE Transaction_Log (
    log_id SERIAL PRIMARY KEY,
    operation TEXT NOT NULL,
    transaction_id INTEGER,
    old_amount NUMERIC(10,2),
    new_amount NUMERIC(10,2),
    old_description TEXT,
    new_description TEXT,
    old_date TIMESTAMP,
    new_date TIMESTAMP,
    old_category_id INTEGER,
    new_category_id INTEGER,
    log_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- VIEW: Monthly Summary
CREATE VIEW View_Monthly_Summary AS
SELECT
    TO_CHAR(date, 'YYYY-MM') AS month,
    SUM(amount) AS total_expenses
FROM Transactions
GROUP BY TO_CHAR(date, 'YYYY-MM')
ORDER BY month DESC;

-- STORED PROCEDURE: Update budget on transaction changes
CREATE OR REPLACE FUNCTION update_budget_on_transaction()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        UPDATE Budget 
        SET total_spent_ever = total_spent_ever + NEW.amount 
        WHERE budget_id = 1;
        RETURN NEW;
    ELSIF (TG_OP = 'UPDATE') THEN
        UPDATE Budget 
        SET total_spent_ever = total_spent_ever - OLD.amount + NEW.amount 
        WHERE budget_id = 1;
        RETURN NEW;
    ELSIF (TG_OP = 'DELETE') THEN
        UPDATE Budget 
        SET total_spent_ever = total_spent_ever - OLD.amount 
        WHERE budget_id = 1;
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- TRIGGER: Call budget update function
CREATE TRIGGER budget_trigger
AFTER INSERT OR UPDATE OR DELETE ON Transactions
FOR EACH ROW EXECUTE FUNCTION update_budget_on_transaction();

-- STORED PROCEDURE: Log transaction changes
CREATE OR REPLACE FUNCTION log_transaction_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        INSERT INTO Transaction_Log (
            operation, transaction_id, 
            new_amount, new_description, new_date, new_category_id
        )
        VALUES (
            'INSERT', NEW.transaction_id,
            NEW.amount, NEW.description, NEW.date, NEW.category_id
        );
        RETURN NEW;
    ELSIF (TG_OP = 'UPDATE') THEN
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
        RETURN NEW;
    ELSIF (TG_OP = 'DELETE') THEN
        INSERT INTO Transaction_Log (
            operation, transaction_id,
            old_amount, old_description, old_date, old_category_id
        )
        VALUES (
            'DELETE', OLD.transaction_id,
            OLD.amount, OLD.description, OLD.date, OLD.category_id
        );
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- TRIGGER: Call audit log function
CREATE TRIGGER audit_trigger
AFTER INSERT OR UPDATE OR DELETE ON Transactions
FOR EACH ROW EXECUTE FUNCTION log_transaction_changes();

-- STORED PROCEDURE: Get expense summary (demonstrating stored procedures)
CREATE OR REPLACE FUNCTION get_expense_summary()
RETURNS TABLE(
    total_expenses NUMERIC,
    expense_count BIGINT,
    average_expense NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COALESCE(SUM(amount), 0) as total_expenses,
        COUNT(transaction_id) as expense_count,
        COALESCE(AVG(amount), 0) as average_expense
    FROM Transactions;
END;
$$ LANGUAGE plpgsql;

-- STORED PROCEDURE: Get expenses by category
CREATE OR REPLACE FUNCTION get_expenses_by_category()
RETURNS TABLE(
    category TEXT,
    transaction_count BIGINT,
    total_amount NUMERIC,
    average_amount NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.name::TEXT as category,
        COUNT(t.transaction_id) as transaction_count,
        COALESCE(SUM(t.amount), 0) as total_amount,
        COALESCE(AVG(t.amount), 0) as average_amount
    FROM Category c
    INNER JOIN Transactions t ON c.category_id = t.category_id
    GROUP BY c.category_id, c.name
    ORDER BY total_amount DESC;
END;
$$ LANGUAGE plpgsql;
