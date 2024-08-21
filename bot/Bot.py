import locale
import datetime

import discord

import bot.Config as Cfg


class Bot(discord.Bot):
    config: Cfg.Config

    def __init__(self, config: Cfg.Config) -> None:
        self.config = config
        super().__init__(
            intents=discord.Intents.all(),
            status=discord.Status.online,
            activity=discord.CustomActivity(config.getValue("Discord", "activity")),
            command_prefix=config.getValue("Discord", "prefix")
        )

    async def on_ready(self) -> None:
        print(f'Logged in as {self.user} with ID {self.user.id}')
        pass


def main() -> None:
    locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
    print(f"Started on {datetime.datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}");

    config = Cfg.Config("config\\config.cfg", {
        ("Discord", "activity"): "None",
        ("Discord", "prefix"): "!",
        ("Discord", "token"): "<TOKEN>",
    })
    bot = Bot(config)

    try:
        bot.load_extension("bot.cogs.Calender")
        bot.run(config.getValue("Discord", "token"))
    except discord.errors.LoginFailure:
        print("Login failed")
    except Exception as e:
        print(f"Failed to run Bot.\n{e}")
    finally:
        print("Bot about to stop")
