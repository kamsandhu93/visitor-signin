import hashlib
import os
import logging
import dropbox
from dropbox.exceptions import ApiError, AuthError
from dropbox.files import WriteMode

class Database(object):
    def __init__(self, config):
        self.dbx = dropbox.Dropbox(config["DropboxToken"])
        self.localPath = os.path.join(config["DatabaseDir"], config["DatabaseFile"])
        self.backupPath = os.path.join("/", config["DatabaseFile"])
        self.operations = {
            "backup": self.backup,
            "restore": self.restore,
            "restore_force": self.force_restore
        }

    def backup(self):
        with open(self.localPath, "rb") as f:
            self.dbx.files_upload(f.read(), self.backupPath, mode=WriteMode("overwrite"))
            logging.info("Backed up {0} to dropbox {1}".format(self.localPath, self.backupPath))

    def restore(self):
        if not os.path.exists(self.localPath):
            self.dbx.files_download_to_file(self.localPath, self.backupPath)
            logging.info("Normal restore {0} from dropbox {1}".format(self.localPath, self.backupPath))

    def force_restore(self):
        self.dbx.files_download_to_file(self.localPath, self.backupPath)
        logging.info("Forced restore {0} from dropbox {1}".format(self.localPath, self.backupPath))

    def run_operation(self, operationType):
        try:
            self.operations[operationType]()
        except ApiError as err:
            self._report_api_error(err)
        except AuthError as err:
            logging.error(err)
            sys.exit()
        except IOError as err:
            logging.error(err)
            sys.exit()

    def get_hash(self, bufferSize=65536):
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

    def _report_api_error(err):
        insufficientSpace = err.error.is_path() and err.error.get_path().reason.is_insufficient_space()
        if (insufficientSpace):
            logging.error("Cannot back up; insufficient space.")
        elif err.user_message_text:
            logging.error(err.user_message_text)
        else:
            logging.error(err)
        sys.exit()
