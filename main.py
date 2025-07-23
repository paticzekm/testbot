import os
from discord.ext import commands
import discord

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)

MESSAGE_ID = int(os.getenv("MESSAGE_ID"))
GUILD_ID = int(os.getenv("GUILD_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))

EMOJI_ROLE_MAP = {
    "<:corona:725994542909882419>": "TestRole",
    "<:5944_EmpMoan:725994542641315910>": "TestRole2",
    "<:OWO:725994544943857764>": "TestRole3"
}

@bot.event
async def on_ready():
    global log_channel
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    await log(f"✅ Bot is online as {bot.user}")

    guild = bot.get_guild(GUILD_ID)
    channel = guild.get_channel(CHANNEL_ID)
    try:
        message = await channel.fetch_message(MESSAGE_ID)
    except Exception as e:
        await log(f"Failed to fetch message: {e}")
        return

    for emoji in EMOJI_ROLE_MAP.keys():
        try:
            await message.add_reaction(emoji)
        except Exception as e:
            await log(f"Failed to add reaction {emoji}: {e}")

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id != MESSAGE_ID:
        return

    emoji_str = str(payload.emoji)
    if emoji_str not in EMOJI_ROLE_MAP:
        return

    guild = bot.get_guild(payload.guild_id)
    role_name = EMOJI_ROLE_MAP[emoji_str]
    role = discord.utils.get(guild.roles, name=role_name)
    member = guild.get_member(payload.user_id)

    if role and member and not member.bot:
        await member.add_roles(role)
        await log(f"Added role {role_name} to {member.mention}")

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id != MESSAGE_ID:
        return

    emoji_str = str(payload.emoji)
    if emoji_str not in EMOJI_ROLE_MAP:
        return

    guild = bot.get_guild(payload.guild_id)
    role_name = EMOJI_ROLE_MAP[emoji_str]
    role = discord.utils.get(guild.roles, name=role_name)
    member = guild.get_member(payload.user_id)

    if role and member and not member.bot:
        await member.remove_roles(role)
        await log(f"Removed role {role_name} from {member.mention}")

async def log(message: str):
    print(message)
    if log_channel:
        await log_channel.send(message)

bot.run(os.getenv("DISCORD_TOKEN"))
