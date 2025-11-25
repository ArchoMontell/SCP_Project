"""
Simple migration script to convert the `objects` table to use an enum-like CHECK for `classification`.
This is a safe, minimal approach for SQLite:
- Creates a new table `objects_new` with the desired schema (classification constrained by CHECK)
- Copies rows from `objects` to `objects_new` (unknown values will be set to 'Unspecified')
- Drops the old table and renames the new one to `objects`

Usage (from project root):
    python scp-backend/migrations/migrate_classification_enum.py

Make sure the Flask app is not running while performing the migration.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scp.db')

ALLOWED = ['Unspecified','Safe','Euclid','Keter','Thaumiel','Exotic','Metaclass']

def migrate():
    if not os.path.exists(DB_PATH):
        print('Database not found at', DB_PATH)
        return
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        print('Disabling foreign keys')
        cur.execute('PRAGMA foreign_keys = OFF;')
        conn.commit()

        print('Creating new table objects_new with CHECK constraint for classification')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS objects_new (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                classification TEXT NOT NULL DEFAULT 'Unspecified' CHECK(classification IN ({allowed})),
                description TEXT,
                storage_requirements TEXT,
                camera_id INTEGER,
                status TEXT DEFAULT 'stored',
                history_of_movements TEXT,
                created_at DATETIME,
                updated_at DATETIME
            );
        '''.replace('{allowed}', ','.join(['"%s"' % v for v in ALLOWED])))
        conn.commit()

        print('Copying data from objects to objects_new (invalid classifications set to Unspecified)')
        # Insert rows, coercing invalid classifications to 'Unspecified'
        cur.execute('SELECT id, name, classification, description, storage_requirements, camera_id, status, history_of_movements, created_at, updated_at FROM objects;')
        rows = cur.fetchall()
        insert_sql = 'INSERT INTO objects_new (id, name, classification, description, storage_requirements, camera_id, status, history_of_movements, created_at, updated_at) VALUES (?,?,?,?,?,?,?,?,?,?);'
        to_insert = []
        for r in rows:
            cls = r[2]
            if cls not in ALLOWED:
                cls = 'Unspecified'
            to_insert.append((r[0], r[1], cls, r[3], r[4], r[5], r[6], r[7], r[8], r[9]))
        cur.executemany(insert_sql, to_insert)
        conn.commit()

        print('Dropping old objects table')
        cur.execute('DROP TABLE objects;')
        conn.commit()

        print('Renaming objects_new -> objects')
        cur.execute('ALTER TABLE objects_new RENAME TO objects;')
        conn.commit()

        print('Migration finished successfully.')
    except Exception as e:
        print('Migration failed:', e)
        conn.rollback()
    finally:
        print('Re-enabling foreign keys')
        try:
            cur.execute('PRAGMA foreign_keys = ON;')
            conn.commit()
        except Exception:
            pass
        conn.close()

if __name__ == '__main__':
    migrate()
