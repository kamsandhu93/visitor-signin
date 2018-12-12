import sys
from backupapp import app
import backupapp.services as services


if __name__ == "__main__":
    app.logger.info("Starting backup and restore service")
    app.run(app.config["HOST"],
            app.config["PORT"])

    try:
        services.restore()
    except Exception as ex:
        app.logge.error(ex)
        app.logger.error("Initial database restore failed")
        sys.exit()
