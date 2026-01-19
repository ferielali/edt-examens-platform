"""
Script to reset student password
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from passlib.context import CryptContext
from sqlalchemy import create_engine, text

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

DATABASE_URL = "postgresql://postgres:aboubakar@localhost:5432/exam_scheduler"
engine = create_engine(DATABASE_URL)

# Generate new password hash for "Student123!"
new_password = "Student123!"
password_hash = pwd_context.hash(new_password)

print(f"Resetting password for student account...")
print(f"New password: {new_password}")

with engine.connect() as conn:
    # Update the student password
    conn.execute(text(f"""
        UPDATE users 
        SET password_hash = :hash 
        WHERE email = 'etu1@etu.univ.edu'
    """), {"hash": password_hash})
    conn.commit()
    
    # Verify
    result = conn.execute(text("SELECT id, email, role FROM users WHERE email = 'etu1@etu.univ.edu'"))
    user = result.fetchone()
    if user:
        print(f"✅ Password reset successful for: {user[1]} (role: {user[2]})")
    else:
        print("❌ User not found!")

print("\nYou can now login with:")
print(f"  Email: etu1@etu.univ.edu")
print(f"  Password: {new_password}")
