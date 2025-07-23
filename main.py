import os
from discord.ext import commands
import discord

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)

MESSAGE_ID = int(os.getenv("MESSAGE_ID"))
GUILD_ID = int(os.getenv("GUILD_ID"))         # Add your server ID as env variable
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))     # Add your channel ID as env variable

EMOJI_ROLE_MAP = {
    "<:corona:725994542909882419>": "TestRole",
    "<:5944_EmpMoan:725994542641315910>": "TestRole2",
    "<:OWO:725994544943857764>": "TestRole3"
}

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

    guild = bot.get_guild(GUILD_ID)
    channel = guild.get_channel(CHANNEL_ID)
    try:
        message = await channel.fetch_message(MESSAGE_ID)
    except Exception as e:
        print(f"Failed to fetch message: {e}")
        return

    for emoji in EMOJI_ROLE_MAP.keys():
        try:
            await message.add_reaction(emoji)
        except Exception as e:
            print(f"Failed to add reaction {emoji}: {e}")

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
        print(f"Added role {role_name} to {member}")

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
        print(f"Removed role {role_name} from {member}")

bot.run(os.getenv("DISCORD_TOKEN"))
