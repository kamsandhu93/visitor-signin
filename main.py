from visitor_app import app
import logging
import os



if __name__ == "__main__":
    log_format = "%(asctime)s | Visitor_app | %(levelname)s | %(message)s"
    formatter = logging.Formatter(log_format)
    logger = logging.getLogger()

    file_handler = logging.FileHandler("visitor.log")
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    app.logger.addHandler(console_handler)

    app.logger.setLevel(logging.DEBUG)
    print(app.root_path)

    app.logger.info("Starting visitor service")
    app.run()

