import shutil
import os
import logging
from datetime import datetime, timedelta
import time

# Setup logs
logging.basicConfig(filename='backup.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

database_path = 'db.sqlite3'
backup_dir = './backups/'

# verify if the backup directory exists
os.makedirs(backup_dir, exist_ok=True)

# Creates the backup files
def backup_database():
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        backup_filename = f"db_backup_{timestamp}.sqlite3"
        backup_file_path = os.path.join(backup_dir, backup_filename)
        shutil.copy2(database_path, backup_file_path)
        logging.info(f"Database backed up to: {backup_file_path}")
    except Exception as e:
        logging.error(f"Failed to backup database: {e}")

# Delete 10 days old backups
def delete_old_backups(days=10):
    try:
        now = datetime.now()
        cutoff = now - timedelta(days=days)
        for filename in os.listdir(backup_dir):
            file_path = os.path.join(backup_dir, filename)
            file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_time < cutoff:
                os.remove(file_path)
                logging.info(f"Backup file deleted: {filename}")
    except Exception as e:
        logging.error(f"Failed to delete old backups: {e}")

# New backup made every 12 hours
while True:
    backup_database()
    delete_old_backups()
    # Consider using a scheduler instead of sleep for more robustness.
    time.sleep(12 * 3600)
