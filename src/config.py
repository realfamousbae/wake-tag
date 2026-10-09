from os import environ
from logging import Formatter, getLogger, INFO, Logger, StreamHandler

from yaml import safe_dump, safe_load


def init_logger() -> Logger:
    logger = getLogger(__name__)

    console_handler = StreamHandler()
    console_handler.setFormatter(Formatter("%(asctime)s %(levelname)s %(message)s"))

    logger.setLevel(INFO)
    logger.addHandler(console_handler)

    logger.info("Logger initialized successfully.")
    return logger


class Config:
    def __init__(self, logger: Logger) -> None:
        self.logger = logger
        self.data = {
            "tech": {
                "api_id": 0,
                "api_hash": "0",
                "admin_id": 0,
                "bot_token": "0"
            }
        }

    def load_config(self, config_filename: str) -> None:
        env_keys = {"api_id": "TG_API_ID", "api_hash": "TG_API_HASH", "bot_token": "TG_BOT_TOKEN"}

        if all(environ.get(name) for name in env_keys.values()):
            self.data = {"tech": {key: environ[name] for key, name in env_keys.items()}}
            self.data["tech"]["api_id"] = int(self.data["tech"]["api_id"])
            self.logger.info('Config loaded from environment variables.')
            return

        config_file_path = f'./{config_filename}'

        try:
            with open(config_file_path, "r") as config_file:
                config = safe_load(config_file)
                self.data = config
                self.logger.info('Config successfully loaded.')
        except FileNotFoundError:
            with open(config_file_path, "w") as config_file:
                config_file.write(safe_dump(self.data))

            self.logger.info('Created new config file.')

            raise Exception("Enter the auth keys into config file.")
