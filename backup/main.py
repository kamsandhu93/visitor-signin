from backupapp import app

if __name__ == "__main__":
    app.logger.info("Starting backup and restore service")
    app.run(app.config["HOST"],
            app.config["PORT"])
