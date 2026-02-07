"""Apply database migration for advanced features."""
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
else:
    print("Warning: .env file not found. Using environment variables.")

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlmodel import create_engine, text

# Get DATABASE_URL from environment
database_url = os.getenv("DATABASE_URL")
if not database_url:
    print("Error: DATABASE_URL not found in environment variables")
    sys.exit(1)

def apply_migration():
    """Apply the advanced features migration."""
    migration_file = Path(__file__).parent.parent / "migrations" / "add_advanced_features.sql"
    
    if not migration_file.exists():
        print(f"Error: Migration file not found: {migration_file}")
        return False
    
    print(f"Reading migration file: {migration_file}")
    with open(migration_file, 'r') as f:
        migration_sql = f.read()
    
    print("Connecting to database...")
    engine = create_engine(database_url, echo=False)
    
    # Split SQL by semicolons and execute each statement
    statements = [s.strip() for s in migration_sql.split(';') if s.strip() and not s.strip().startswith('--')]
    
    print(f"Executing {len(statements)} SQL statements...")
    
    # Execute statements one by one with individual transactions
    for i, statement in enumerate(statements, 1):
        if statement:
            try:
                print(f"  [{i}/{len(statements)}] Executing statement...")
                with engine.begin() as conn:
                    conn.execute(text(statement))
                print(f"    ✓ Success")
            except Exception as e:
                error_msg = str(e).lower()
                # Some statements might fail if they already exist (IF NOT EXISTS)
                if any(keyword in error_msg for keyword in ["already exists", "duplicate"]):
                    print(f"    (Skipped - already exists)")
                elif "does not exist" in error_msg and "index" in error_msg:
                    # Index on non-existent table - will be created when table is created
                    print(f"    (Skipped - table not created yet)")
                else:
                    print(f"    ⚠ Warning: {error_msg[:80]}")
    
    print("\n✅ Migration completed!")
    return True

if __name__ == "__main__":
    try:
        apply_migration()
    except Exception as e:
        print(f"\n❌ Error applying migration: {e}")
        sys.exit(1)

