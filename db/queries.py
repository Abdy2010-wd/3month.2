CREATE_TABLE_TASK = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    completed INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now', 'localtime'))
);
"""

INSERT_TASK = "INSERT INTO tasks (task, created_at) VALUES (?, datetime('now', 'localtime'));"

SELECT_TASK = "SELECT id, task, completed, created_at FROM tasks;"

SELECT_TASKS_COMPLETED = "SELECT id, task, completed, created_at FROM tasks WHERE completed = 1;"

SELECT_TASKS_UNCOMPLETED = "SELECT id, task, completed, created_at FROM tasks WHERE completed = 0;"

DELETE_TASK = "DELETE FROM tasks WHERE id = ?;"

UPDATE_TASK = "UPDATE tasks SET task = ? WHERE id = ?;"
