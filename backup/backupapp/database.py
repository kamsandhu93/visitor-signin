import hashlib
import os
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError
from shutil import copyfile
from exceptions import ApiErrorEx, AuthErrorEx, IOErrorEx

class Database(object):
    def __init__(self, config, logger):
        self.dbx = dropbox.Dropbox(config["DROPBOX_TOKEN"])
        self.localPath = os.path.join(config["DB_PATH"], config["DB_FILE"])
        self.backupPath = os.path.join("/", config["DB_FILE"])
        self.offlineBackupPath = os.path.join(config["OFFLINE_BACKUP_PATH"], config["DB_FILE"])
        self.logger = logger
        self.operations = {
            "backup": self.backup,
            "backupOffline": self.backupOffline,
            "restore": self.restore,
            "restoreForce": self.restoreForce
        }

    def backup(self):
        with open(self.localPath, "rb") as f:
            self.dbx.files_upload(f.read(), self.backupPath, mode=WriteMode("overwrite"))
            self.logger.info("Backed up {0} to dropbox {1}".format(self.localPath, self.backupPath))

    def backupOffline(self):
        copyfile(self.localPath, self.offlineBackupPath)
        self.logger.info("Offline backup up {0} to {1}".format(self.localPath, self.offlineBackupPath))

    def restore(self):
        if not os.path.exists(self.localPath):
            self.dbx.files_download_to_file(self.localPath, self.backupPath)
            self.logger.info("Normal restore {0} from dropbox {1}".format(self.localPath, self.backupPath))

    def restoreForce(self):
        self.dbx.files_download_to_file(self.localPath, self.backupPath)
        self.logger.info("Forced restore {0} from dropbox {1}".format(self.localPath, self.backupPath))

    def runOperation(self, operationType):
        try:
            self.operations[operationType]()
        except ApiError as ex:
            self._reportApiError(ex)
            raise ApiErrorEx(ex)
        except AuthError as ex:
            self.logger.error(ex)
            raise AuthErrorEx(ex)
        except IOError as ex:
            self.logger.error(ex)
            raise IOErrorEx(ex)

    def getHash(self, bufferSize=65536):
        sha1 = hashlib.sha1()
        md5 = hashlib.md5()

        with open(self.localPath, "rb") as f:
            while True:
                data = f.read(bufferSize)
                if not data:
                    break
                md5.update(data)
                sha1.update(data)

        return {
            "md5": md5.hexdigest(),
            "sha1": sha1.hexdigest()
        }

    def _reportApiError(err):
        insufficientSpace = err.error.is_path() and err.error.get_path().reason.is_insufficient_space()
        if (insufficientSpace):
            self.logger.error("Cannot back up; insufficient space.")
        elif err.user_message_text:
            self.logger.error(err.user_message_text)
        else:
            self.logger.error(err)
