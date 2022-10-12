import os
import time
import discord
import asyncio
from discord import Option
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from keep_alive import keep_alive
'''from discord import utils as discord_utils'''
servers = [877691163606413423]

bot = discord.Bot()

def getSecondsByLevel(level):
    levels = {
        "l0": 600,
        "l1": 1800,
        "l2": 3600,
        "l3": 5400,
        "l4": 7200,
        "l5": 9000,
        "l6": 10800,
        "l7": 12600,
        "l8": 14400,
        "l9": 16200,
        "l10": 18000,
        "l16": 28800
    }

    return levels[f"l{level}"]


async def Clock(seconds):
    while True:
        await asyncio.sleep(1)

        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        days, hours = divmod(hours, 24)

        seconds -= 1

        yield '{:02d}:{:02d}:{:02d}'.format(hours, mins, secs)


async def countHandler(ctx, job, seconds):

    hourFormat = time.strftime('%H:%M:%S', time.gmtime(seconds))

    timeLeft = await ctx.channel.send(f"<@&{1024669228147679322}> \nTime left for **{job}** is `{hourFormat}`")
    seconds -= 1
    async for timer in Clock(seconds):
        await timeLeft.edit(content=f"<@&{1024669228147679322}> \nTime left for **{job}** is `{timer}`")
        if timer == "00:00:00":
            await timeLeft.delete()
            await ctx.channel.send(f"Time is up! {ctx.author.mention}! <@&{1024669228147679322}>")
            break


@bot.event
async def on_ready():
    print(f"I have loggen in as {bot.user}")


@bot.slash_command(guild_ids=servers, name="response", description="Checks to see if I am online")
async def response(ctx):
    await ctx.respond(f"Thanks to <@{452606383896920064}>, I\'am Alive! \nLatency: {bot.latency*1000} ms.")


@bot.slash_command(guild_ids=servers, name="countdown", description="Please enter the Job and the level of the manhua")
async def countdown(ctx,
                    task: Option(str,
                                   "Please enter a task",
                                   choices=["Translation", "Typesetting","SR member to respond", "NON-SR member to respond"],
                                   required=True),
                    level: Option(int,
                                  "Please enter the level of the manhua, from 1 to 10",
                                  min_value=0, max_value=16, default=2, )):
    job = None
    if task == "Translation":
        job = "TL"
    elif task == "Typesetting":
        job = "TS"
    elif task == "SR member to respond":
      job = "member to respond"
      #level = 2
    elif task == "NON-SR member to respond":
      job = "member to respond"
      level = 16

    seconds = getSecondsByLevel(level)

    if job != None:
        await ctx.respond(f"Task: {job}, Level: {level}")
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(await countHandler(ctx, job, seconds))
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

keep_alive()
bot.run(OTk5NjU0NjMyMzE1OTQ1MDIw.GwmKrY.c-u4lnPvRbjnORriKzthd2TuT22EasMRNXkkL8)
