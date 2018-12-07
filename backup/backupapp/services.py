import hashlib
import os
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError
from shutil import copyfile
from exceptions import ApiErrorEx, AuthErrorEx, IOErrorEx
from backupapp import app



dbx = dropbox.Dropbox(app.config["DROPBOX_TOKEN"])
localPath = os.path.join(app.config["DB_PATH"], app.config["DB_FILE"])
backupPath = os.path.join("/", app.config["DB_FILE"])
offlineBackupPath = os.path.join(app.config["OFFLINE_BACKUP_PATH"], app.config["DB_FILE"])
operations = {
    "backup": self.backup,
    "backupOffline": self.backupOffline,
    "restore": self.restore,
    "restoreForce": self.restoreForce
}

def backup():
    with open(localPath, "rb") as f:
        dbx.files_upload(f.read(), backupPath, mode=WriteMode("overwrite"))
        app.logge.info("Backed up {0} to dropbox {1}".format(localPath, backupPath))

def backupOffline():
    copyfile(localPath, offlineBackupPath)
    app.logge.info("Offline backup up {0} to {1}".format(localPath, offlineBackupPath))

def restore():
    if not os.path.exists(localPath):
        dbx.files_download_to_file(localPath, backupPath)
        app.logge.info("Normal restore {0} from dropbox {1}".format(localPath,backupPath))

def restoreForce():
    dbx.files_download_to_file(localPath, backupPath)
    app.logge.info("Forced restore {0} from dropbox {1}".format(localPath, backupPath))

def runOperation(operationType):
    try:
        operations[operationType]()
    except Exception as ex:
        app.logge.error(ex)
        raise Exception(ex)

