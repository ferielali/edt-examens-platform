"""
Script to list all users in the database - compact output
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://postgres:aboubakar@localhost:5432/exam_scheduler"
engine = create_engine(DATABASE_URL)

def list_users():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, email, role, nom, prenom, active FROM users ORDER BY id"))
        users = result.fetchall()
        
        print("COMPTES UTILISATEURS")
        print("-" * 80)
        print(f"{'ID':<5} {'Email':<40} {'Role':<15} {'Nom':<15} {'Prenom':<15} {'Actif'}")
        print("-" * 80)
        
        for u in users:
            nom = u[3] or 'N/A'
            prenom = u[4] or 'N/A'
            email = u[1][:38] + '..' if len(u[1]) > 40 else u[1]
            print(f"{u[0]:<5} {email:<40} {u[2]:<15} {nom:<15} {prenom:<15} {u[5]}")
        
        print("-" * 80)
        print(f"Total: {len(users)} utilisateur(s)")

if __name__ == "__main__":
    list_users()
