#!/usr/bin/env python3
"""Fix foreign key constraints to use CASCADE delete."""
import os
import sys
from sqlalchemy import create_engine, text, inspect
from dotenv import load_dotenv

load_dotenv()

def fix_foreign_key_constraints():
    """Ensure foreign key constraints have ON DELETE CASCADE."""
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("❌ DATABASE_URL not found")
        sys.exit(1)
    
    engine = create_engine(db_url)
    
    print("=" * 60)
    print("  🔧 FIXING FOREIGN KEY CONSTRAINTS")
    print("=" * 60)
    print()
    
    try:
        with engine.connect() as conn:
            # Check current constraints
            print("1️⃣ Checking current foreign key constraints...")
            result = conn.execute(text("""
                SELECT 
                    tc.constraint_name, 
                    tc.table_name, 
                    kcu.column_name,
                    ccu.table_name AS foreign_table_name,
                    ccu.column_name AS foreign_column_name,
                    rc.delete_rule
                FROM information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                    ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.constraint_column_usage AS ccu
                    ON ccu.constraint_name = tc.constraint_name
                LEFT JOIN information_schema.referential_constraints AS rc
                    ON rc.constraint_name = tc.constraint_name
                WHERE tc.constraint_type = 'FOREIGN KEY'
                    AND tc.table_name IN ('recurringtask', 'reminder')
                ORDER BY tc.table_name;
            """))
            
            constraints = result.fetchall()
            print(f"   Found {len(constraints)} foreign key constraint(s)")
            for constraint in constraints:
                print(f"   - {constraint[1]}.{constraint[2]} → {constraint[3]}.{constraint[4]} (delete_rule: {constraint[5]})")
            print()
            
            # Drop and recreate constraints with CASCADE
            print("2️⃣ Fixing constraints...")
            
            # Fix recurringtask constraint
            print("   Fixing recurringtask.task_id → task.id...")
            conn.execute(text("""
                ALTER TABLE recurringtask 
                DROP CONSTRAINT IF EXISTS recurringtask_task_id_fkey;
            """))
            conn.execute(text("""
                ALTER TABLE recurringtask 
                ADD CONSTRAINT recurringtask_task_id_fkey 
                FOREIGN KEY (task_id) 
                REFERENCES task(id) 
                ON DELETE CASCADE;
            """))
            print("   ✅ recurringtask constraint fixed")
            
            # Fix reminder constraints
            print("   Fixing reminder.task_id → task.id...")
            conn.execute(text("""
                ALTER TABLE reminder 
                DROP CONSTRAINT IF EXISTS reminder_task_id_fkey;
            """))
            conn.execute(text("""
                ALTER TABLE reminder 
                ADD CONSTRAINT reminder_task_id_fkey 
                FOREIGN KEY (task_id) 
                REFERENCES task(id) 
                ON DELETE CASCADE;
            """))
            print("   ✅ reminder.task_id constraint fixed")
            
            print("   Fixing reminder.user_id → user.id...")
            conn.execute(text("""
                ALTER TABLE reminder 
                DROP CONSTRAINT IF EXISTS reminder_user_id_fkey;
            """))
            conn.execute(text("""
                ALTER TABLE reminder 
                ADD CONSTRAINT reminder_user_id_fkey 
                FOREIGN KEY (user_id) 
                REFERENCES "user"(id) 
                ON DELETE CASCADE;
            """))
            print("   ✅ reminder.user_id constraint fixed")
            
            conn.commit()
            
            print()
            print("3️⃣ Verifying constraints...")
            result = conn.execute(text("""
                SELECT 
                    tc.table_name, 
                    kcu.column_name,
                    ccu.table_name AS foreign_table_name,
                    rc.delete_rule
                FROM information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                    ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.constraint_column_usage AS ccu
                    ON ccu.constraint_name = tc.constraint_name
                LEFT JOIN information_schema.referential_constraints AS rc
                    ON rc.constraint_name = tc.constraint_name
                WHERE tc.constraint_type = 'FOREIGN KEY'
                    AND tc.table_name IN ('recurringtask', 'reminder')
                ORDER BY tc.table_name;
            """))
            
            constraints = result.fetchall()
            all_cascade = True
            for constraint in constraints:
                delete_rule = constraint[3]
                if delete_rule != 'CASCADE':
                    all_cascade = False
                    print(f"   ⚠️  {constraint[0]}.{constraint[1]} → {constraint[2]} (delete_rule: {delete_rule})")
                else:
                    print(f"   ✅ {constraint[0]}.{constraint[1]} → {constraint[2]} (delete_rule: CASCADE)")
            
            if all_cascade:
                print()
                print("=" * 60)
                print("  ✅ ALL CONSTRAINTS FIXED!")
                print("=" * 60)
                print()
                print("💡 Now task deletion will automatically cascade to:")
                print("   - recurringtask records")
                print("   - reminder records")
                print()
            else:
                print()
                print("⚠️  Some constraints still need fixing")
                sys.exit(1)
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    fix_foreign_key_constraints()

