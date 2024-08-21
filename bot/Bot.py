#!/bin/python3
import locale
import datetime

import discord

import Config as cfg


class Bot(discord.Bot):
    config: cfg.Config

    def __init__(self, config: cfg.Config):
        self.config = config
        super().__init__(
            intents=discord.Intents.all(),
            status=discord.Status.online,
            activity=discord.CustomActivity(config.getValue("Discord", "activity", "None")),
            command_prefix=config.getValue("Discord", "prefix", "!")
        )

    async def on_ready(self):
        print(f'Logged in as {self.user} with ID {self.user.id}')
        pass


def main():
    locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
    print(f"Started on {datetime.datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}");

    config = cfg.Config("config\\config.cfg", {
        ("Discord", "activity"): "None",
        ("Discord", "prefix"): "!",
        ("Discord", "token"): "<TOKEN>",
    })
    bot = Bot(config)

    try:
        bot.run(config.getValue("Discord", "token"))
    except discord.errors.LoginFailure:
        print("Login failed")
    except Exception as e:
        print(f"Failed to run Bot.\n{e}")
    finally:
        print("Bot about to stop")


if __name__ == "__main__":
    main()
