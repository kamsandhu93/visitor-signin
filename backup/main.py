import sys
from backupapp import app
import backupapp.services as services


if __name__ == "__main__":

    try:
        services.restore()
    except Exception as ex:
        app.logger.error("Initial database restore failed")
        app.log_exception(ex)
        sys.exit()

    app.logger.info("Starting backup and restore service")
    app.run(app.config["HOST"],
            app.config["PORT"])
