import logging

from src.app import App
from src.config import Config


def main():
    logging.basicConfig(level=logging.INFO)
    config = Config()
    config.files.create_dirs()
    application = App(config)
    application.run()


if __name__ == "__main__":
    main()
