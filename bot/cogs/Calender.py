import discord
from discord.ext import commands, tasks

import bot.Config as Cfg
import bot.apis.Moodle as Moodle


class Calender(commands.Cog):
    bot: discord.Bot
    config: Cfg.Config
    api: Moodle.MoodleAPI

    last_message: discord.Message = None

    def __init__(self, bot: discord.Bot, config: Cfg.Config) -> None:
        self.bot = bot
        self.config = config
        self.api = Moodle.MoodleAPI(
            domain=config.getValue("Moodle", "domain"),
            userid=config.getValue("Moodle", "userid"),
            token=config.getValue("Moodle", "token")
        )

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        channel_id = int(self.config.getValue("Channel", "id"))
        channel = self.bot.get_channel(channel_id)
        if channel is None:
            print(f"Channel {channel_id} not found.")
            return

        # Purge Channel
        if self.config.getValue("Channel", "purge") == "true":
            await channel.purge(limit=None)
            print(f"Channel \"{channel.name}\" purged.")

        # Send Welcome Embed
        await channel.send(
            embed=discord.Embed(
                type="rich",
                title=self.config.getValue("Channel", "title"),
                description=self.config.getValue("Channel", "description"),
                url=f"https://{self.api.domain}/my/",
                color=0x00ff55
            ).add_field(
                name=self.config.getValue("Welcome", "message"),
                value=self.config.getValue("Welcome", "description"),
                inline=False
            )
        )

        # Adding update task
        self.update.change_interval(seconds=int(self.config.getValue("Moodle", "interval", "60")))
        self.update.start()

    @tasks.loop(minutes=1)
    async def update(self) -> None:
        channel_id = int(self.config.getValue("Channel", "id"))
        channel = self.bot.get_channel(channel_id)
        if channel is None:
            print(f"Channel {channel_id} not found.")
            return
        entries = await self.api.parse_calender(Moodle.PW_All, Moodle.PT_RECENTUPCOMING)

        embed = discord.Embed(
            type="rich",
            title=self.config.getValue("Channel", "title"),
            description=self.config.getValue("Channel", "description"),
            url=f"https://{self.api.domain}/my/",
            color=0x00ffff
        )

        if entries:
            for entry in entries:
                embed.add_field(
                    name=f"{entry.title} - {entry.end.strftime('%A %d.%m.%Y %H:%M')}",
                    value=f"{entry.content}",
                    inline=False
                )
        else:
            embed.add_field(
                name=self.config.getValue("Channel", "notfound"),
                value="",
                inline=False
            )

        if self.last_message:
            await self.last_message.delete()
        self.last_message = await channel.send(embed=embed)


def setup(bot: discord.Bot) -> None:
    config = Cfg.Config("config\\calender.cfg", {
        ("Moodle", "domain"): "moodle.moodleapp.com",
        ("Moodle", "userid"): "0",
        ("Moodle", "token"): "0",
        ("Moodle", "interval"): "60",
        ("Moodle", "enabled"): "false",

        ("Channel", "title"): "Hausaufgaben",
        ("Channel", "description"): "Die aktuellen Aufgaben",
        ("Channel", "notfound"): "Keine Einträge gefunden",
        ("Channel", "purge"): "false",
        ("Channel", "id"): "0",

        ("Welcome", "message"): "Der Bot ist neu gestartet",
        ("Welcome", "description"): "Die Nächste Nachricht beinhaltet alle aktuellen Aufgaben",
    })

    if config.getValue("Moodle", "enabled") == "true":
        bot.add_cog(Calender(bot, config))
        print("Moodle cog started")
