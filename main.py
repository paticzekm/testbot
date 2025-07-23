import os
from discord.ext import commands
import discord

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)

MESSAGE_ID = os.getenv("MESSAGE_ID") 
EMOJI = "✅"
ROLE_NAME = os.getenv("ROLE_NAME")

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id != MESSAGE_ID or str(payload.emoji.name) != EMOJI:
        return
    guild = bot.get_guild(payload.guild_id)
    role = discord.utils.get(guild.roles, name=ROLE_NAME)
    member = guild.get_member(payload.user_id)
    if role and member and not member.bot:
        await member.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id != MESSAGE_ID or str(payload.emoji.name) != EMOJI:
        return
    guild = bot.get_guild(payload.guild_id)
    role = discord.utils.get(guild.roles, name=ROLE_NAME)
    member = guild.get_member(payload.user_id)
    if role and member and not member.bot:
        await member.remove_roles(role)

bot.run(os.getenv("DISCORD_TOKEN"))
