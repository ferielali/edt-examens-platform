"""
Script to fix password hashes for all users.
This re-hashes passwords using Python's passlib to ensure compatibility.
"""
import sys
import os

# Add the parent directory to path to import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import engine, SessionLocal
from app.core.security import get_password_hash
from app.models import User

# Define passwords for each role
ROLE_PASSWORDS = {
    "director": "Director123!",
    "administrator": "Admin123!",
    "department_head": "Chef123!",
    "professor": "Prof123!",
    "student": "Etudiant123!",
}

def fix_all_passwords():
    """Update all user passwords with Python-compatible hashes."""
    db = SessionLocal()
    try:
        users = db.query(User).all()
        updated_count = 0
        
        for user in users:
            # Get the password for this role
            password = ROLE_PASSWORDS.get(user.role)
            if password:
                # Generate new hash using Python's passlib
                user.password_hash = get_password_hash(password)
                updated_count += 1
                print(f"Updated: {user.email} ({user.role})")
        
        db.commit()
        print(f"\n✅ Successfully updated {updated_count} user passwords!")
        print("\nYou can now login with these credentials:")
        print("-" * 50)
        for role, pwd in ROLE_PASSWORDS.items():
            print(f"  {role}: {pwd}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 50)
    print("Fixing Password Hashes for All Users")
    print("=" * 50)
    fix_all_passwords()
