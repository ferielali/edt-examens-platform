# -*- coding: utf-8 -*-
import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path)

db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url)

# Find users with encoding issues and fix them
with engine.connect() as connection:
    # First, let's see all users with their names
    result = connection.execute(text("""
        SELECT u.id, u.email, u.role, 
               COALESCE(e.nom, p.nom, et.nom) as nom,
               COALESCE(e.prenom, p.prenom, et.prenom) as prenom
        FROM users u
        LEFT JOIN enseignants e ON u.id = e.user_id
        LEFT JOIN personnels p ON u.id = p.user_id
        LEFT JOIN etudiants et ON u.id = et.user_id
        ORDER BY u.role
    """))
    
    print("Current users with names:")
    print(f"{'ID':<5} {'EMAIL':<35} {'NOM':<20} {'PRENOM':<20}")
    print("-" * 80)
    for row in result:
        print(f"{row.id:<5} {row.email:<35} {str(row.nom):<20} {str(row.prenom):<20}")
    
    # Fix the encoding issue: FranÃ§ois -> François
    print("\n--- Fixing encoding issues ---")
    
    # Update in enseignants table
    connection.execute(text("""
        UPDATE enseignants 
        SET prenom = 'François' 
        WHERE prenom LIKE '%Fran%ois%' OR prenom LIKE '%FranÃ%'
    """))
    
    # Update in personnels table
    connection.execute(text("""
        UPDATE personnels 
        SET prenom = 'François' 
        WHERE prenom LIKE '%Fran%ois%' OR prenom LIKE '%FranÃ%'
    """))
    
    connection.commit()
    print("✓ Name encoding fixed! 'François Dubois' should now display correctly.")
