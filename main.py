from src import Config, init_logger, TelegramBot

from asyncio import run


async def main() -> None:
    logger = init_logger()

    config = Config(logger)
    config.load_config("config.yaml")

    bot = TelegramBot(logger, config.data)

    await bot.client.start(bot_token=config.data["tech"]["bot_token"])

    async with bot.client:
        await bot.handlers()
        await bot.run()


if __name__ == "__main__":
    run(main())
