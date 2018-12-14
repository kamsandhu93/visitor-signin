import hashlib
import os
import dropbox
from dropbox.files import WriteMode
from shutil import copyfile
from backupapp import app


dbx = dropbox.Dropbox(app.config["DROPBOX_TOKEN"])
local_path = app.config["LOCAL_PATH"]
backup_path = app.config["BACKUP_PATH"]
offline_backup_path = app.config["OFFLINE_BACKUP_PATH"]

def backup():
    with open(local_path, "rb") as f:
        dbx.files_upload(f.read(), backup_path, mode=WriteMode("overwrite"))
        app.logger.info("Backed up {0} to dropbox {1}".format(local_path, backup_path))

def backup_offline():
    copyfile(local_path, offline_backup_path)
    app.logger.info("Offline backup up {0} to {1}".format(local_path, offline_backup_path))

def restore():
    if not os.path.exists(local_path):
        dbx.files_download_to_file(local_path, backup_path)
        app.logger.info("Normal restore {0} from dropbox {1}".format(local_path,backup_path))

def restore_force():
    dbx.files_download_to_file(local_path, backup_path)
    app.logger.info("Forced restore {0} from dropbox {1}".format(local_path, backup_path))
