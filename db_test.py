from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

username = 'the user'
password = 'yourpassword'  # dein aktuelles Passwort
database_name = 'insolvency_db'

# URL-encoding des Passwortes
password_encoded = quote_plus(password)

DATABASE_URL = f'postgresql://{username}:{password_encoded}@localhost/{database_name}'

engine = create_engine(DATABASE_URL)

# Testabfrage
with engine.connect() as conn:
    result = conn.execute(text("SELECT 'Datenbank Verbunden!' AS status;"))
    row = result.fetchone()
    print(row[0])
