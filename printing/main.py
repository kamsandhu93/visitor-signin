from printapi import app

if __name__ == "__main__":
    app.logger.info("Starting Print Service")
    app.run(app.config["HOST"],
            app.config["PORT"])
