-- database: ../db/sql.db
ALTER TABLE chores ADD COLUMN task_completion INTEGER DEFAULT 0;
ALTER TABLE chores ADD COLUMN time_slot TEXT;
ALTER TABLE chores ADD COLUMN weekday INTEGER;
SELECT * FROM chores;
SELECT * FROM users;

DELETE FROM chores;