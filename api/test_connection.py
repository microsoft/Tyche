import pyodbc
import os


# DB credentials (from .env or hardcoded — update accordingly)
DB_USER = os.getenv("DB_USER", "voiceadmin")
DB_PASS = os.getenv("DB_PASS", "Voice@dm!n")
DB_SERVER = os.getenv("DB_SERVER", "july-hackathon.database.windows.net")
DB_NAME = os.getenv("DB_NAME", "voice_nba")

# Connection string
connection_string = (
    f'DRIVER={{ODBC Driver 18 for SQL Server}};'
    f'SERVER=tcp:{DB_SERVER},1433;'
    f'DATABASE={DB_NAME};'
    f'UID={DB_USER};'
    f'PWD={DB_PASS};'
    'Encrypt=yes;'
    'TrustServerCertificate=no;'
)


try:
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute("SELECT ticket_number," \
    "                       creation_date, " \
    "                       current_Status, " \
    "                       assigned_to, " \
    "                       priority, " \
    "                       subject, " \
    "                       any_other_comments " \
    "                FROM voice_nba.dbo.voice_tickets;")
    result = cursor.fetchone()
    print("Connection successful, test query result:", result)
    conn.close()
except Exception as e:
    print("Connection failed:", e)