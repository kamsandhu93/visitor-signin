import hashlib
import os
import dropbox
from dropbox.files import WriteMode
from shutil import copyfile
from backupapp import app


dbx = dropbox.Dropbox(app.config["DROPBOX_TOKEN"])
localPath = app.config["LOCAL_PATH"]
backupPath = app.config["BACKUP_PATH"]
offlineBackupPath = app.config["OFFLINE_BACKUP_PATH"]

def backup():
    with open(localPath, "rb") as f:
        dbx.files_upload(f.read(), backupPath, mode=WriteMode("overwrite"))
        app.logge.info("Backed up {0} to dropbox {1}".format(localPath, backupPath))

def backup_offline():
    copyfile(localPath, offlineBackupPath)
    app.logge.info("Offline backup up {0} to {1}".format(localPath, offlineBackupPath))

def restore():
    if not os.path.exists(localPath):
        dbx.files_download_to_file(localPath, backupPath)
        app.logge.info("Normal restore {0} from dropbox {1}".format(localPath,backupPath))

def restore_force():
    dbx.files_download_to_file(localPath, backupPath)
    app.logge.info("Forced restore {0} from dropbox {1}".format(localPath, backupPath))
