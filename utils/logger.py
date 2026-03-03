import logging
from db_functions import connect_to_db


db = connect_to_db()
cursor = db.cursor(dictionary=True)


logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)
    
    
def audit_log(cursor, db, action, username):
    cursor.execute(
        "INSERT INTO audit_logs (action, username) VALUES (%s, %s)",
        (action, username),
    )
    db.commit()