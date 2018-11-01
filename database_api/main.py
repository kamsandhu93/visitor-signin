from dbapi import app

if __name__ == "__main__":
    app.logger.info("Starting visitor service")
    app.run(app.config["HOST"],
            app.config["PORT"])
