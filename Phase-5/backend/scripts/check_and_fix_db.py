#!/usr/bin/env python3
"""Check and fix database schema - Run this to verify and apply migrations."""
import os
import sys
from sqlalchemy import create_engine, inspect, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_database_url():
    """Get database URL from environment or Kubernetes secret."""
    # Try environment variable first
    db_url = os.environ.get('DATABASE_URL')
    
    if not db_url:
        print("❌ DATABASE_URL not found in environment")
        print("   Please set DATABASE_URL environment variable")
        sys.exit(1)
    
    return db_url

def check_columns(engine):
    """Check if required columns exist in task table."""
    inspector = inspect(engine)
    
    try:
        columns = [col['name'] for col in inspector.get_columns('task')]
    except Exception as e:
        print(f"❌ Error checking task table: {e}")
        return False, []
    
    print("\n📋 Current columns in 'task' table:")
    for col in sorted(columns):
        print(f"   ✓ {col}")
    
    # Required columns for advanced features
    required_columns = [
        'priority', 'tags', 'due_date', 'reminder_time',
        'recurrence_pattern', 'recurrence_interval',
        'next_due_date', 'parent_task_id'
    ]
    
    missing_columns = [col for col in required_columns if col not in columns]
    
    return len(missing_columns) == 0, missing_columns

def apply_migration(engine):
    """Apply migration to add missing columns."""
    migration_sql = """
-- Add new columns to tasks table
ALTER TABLE task ADD COLUMN IF NOT EXISTS priority VARCHAR(20) DEFAULT 'medium';
ALTER TABLE task ADD COLUMN IF NOT EXISTS tags TEXT;
ALTER TABLE task ADD COLUMN IF NOT EXISTS due_date TIMESTAMP;
ALTER TABLE task ADD COLUMN IF NOT EXISTS reminder_time TIMESTAMP;
ALTER TABLE task ADD COLUMN IF NOT EXISTS recurrence_pattern VARCHAR(50);
ALTER TABLE task ADD COLUMN IF NOT EXISTS recurrence_interval INTEGER;
ALTER TABLE task ADD COLUMN IF NOT EXISTS next_due_date TIMESTAMP;
ALTER TABLE task ADD COLUMN IF NOT EXISTS parent_task_id INTEGER REFERENCES task(id);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_task_priority ON task(priority);
CREATE INDEX IF NOT EXISTS idx_task_due_date ON task(due_date);
CREATE INDEX IF NOT EXISTS idx_task_created_at ON task(created_at);
CREATE INDEX IF NOT EXISTS idx_task_title ON task(title);
CREATE INDEX IF NOT EXISTS idx_task_completed ON task(completed);

-- Create recurring_tasks table
CREATE TABLE IF NOT EXISTS recurringtask (
    id SERIAL PRIMARY KEY,
    task_id INTEGER NOT NULL UNIQUE REFERENCES task(id) ON DELETE CASCADE,
    pattern VARCHAR(50) NOT NULL,
    interval INTEGER NOT NULL DEFAULT 1,
    last_created_at TIMESTAMP,
    next_due_date TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_recurringtask_task_id ON recurringtask(task_id);
CREATE INDEX IF NOT EXISTS idx_recurringtask_next_due_date ON recurringtask(next_due_date);
CREATE INDEX IF NOT EXISTS idx_recurringtask_is_active ON recurringtask(is_active);

-- Create reminders table
CREATE TABLE IF NOT EXISTS reminder (
    id SERIAL PRIMARY KEY,
    task_id INTEGER NOT NULL REFERENCES task(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    remind_at TIMESTAMP NOT NULL,
    sent BOOLEAN NOT NULL DEFAULT FALSE,
    sent_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_reminder_task_id ON reminder(task_id);
CREATE INDEX IF NOT EXISTS idx_reminder_user_id ON reminder(user_id);
CREATE INDEX IF NOT EXISTS idx_reminder_remind_at ON reminder(remind_at);
CREATE INDEX IF NOT EXISTS idx_reminder_sent ON reminder(sent);
"""
    
    print("\n🔧 Applying migration...")
    
    try:
        with engine.connect() as conn:
            statements = [s.strip() for s in migration_sql.split(';') if s.strip()]
            
            for statement in statements:
                try:
                    conn.execute(text(statement))
                    conn.commit()
                except Exception as e:
                    # Ignore errors for IF NOT EXISTS clauses
                    error_msg = str(e).lower()
                    if 'already exists' not in error_msg and 'duplicate' not in error_msg:
                        print(f"   ⚠️  Warning: {e}")
            
            print("✅ Migration applied successfully!")
            return True
    except Exception as e:
        print(f"❌ Error applying migration: {e}")
        return False

def test_query(engine):
    """Test a simple query to verify everything works."""
    print("\n🧪 Testing database query...")
    
    try:
        with engine.connect() as conn:
            # Try to query tasks with new columns
            result = conn.execute(text("""
                SELECT id, title, priority, due_date, tags 
                FROM task 
                LIMIT 1
            """))
            
            rows = result.fetchall()
            print(f"✅ Query successful! Found {len(rows)} test row(s)")
            return True
    except Exception as e:
        print(f"❌ Query test failed: {e}")
        return False

def main():
    print("=" * 50)
    print("  🔍 DATABASE SCHEMA CHECKER")
    print("=" * 50)
    
    # Get database URL
    db_url = get_database_url()
    print(f"\n✅ Database URL found")
    
    # Create engine
    try:
        engine = create_engine(db_url)
        print("✅ Database connection established")
    except Exception as e:
        print(f"❌ Failed to connect to database: {e}")
        sys.exit(1)
    
    # Check columns
    is_complete, missing_columns = check_columns(engine)
    
    if is_complete:
        print("\n✅ All required columns exist!")
    else:
        print(f"\n❌ Missing {len(missing_columns)} column(s):")
        for col in missing_columns:
            print(f"   - {col}")
        
        # Apply migration
        if apply_migration(engine):
            # Verify again
            is_complete, missing_columns = check_columns(engine)
            if is_complete:
                print("\n✅ All columns added successfully!")
            else:
                print(f"\n⚠️  Still missing: {missing_columns}")
                sys.exit(1)
        else:
            print("\n❌ Migration failed!")
            sys.exit(1)
    
    # Test query
    if test_query(engine):
        print("\n" + "=" * 50)
        print("  ✅ DATABASE IS READY!")
        print("=" * 50)
        print("\n💡 Next steps:")
        print("   1. Restart backend: kubectl rollout restart deployment/todo-backend -n todo-app")
        print("   2. Test application: http://148.116.94.66:3000")
        print("")
    else:
        print("\n⚠️  Database check passed but query test failed")
        print("   Check backend logs for more details")
        sys.exit(1)

if __name__ == "__main__":
    main()

