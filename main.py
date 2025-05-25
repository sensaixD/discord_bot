import discord
from discord.ext import commands
import os
from keep_alive import keep_alive
keep_alive()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)

VERIFIED_ROLE_NAME = "Verified"
VERIFY_CHANNEL_NAME = "〢🍀・𝐕𝐞𝐢𝐫𝐟𝐲"
VERIFY_EMOJI = "<:1307915427644440596:1375850805541732392>"
VERIFY_IMAGE_URL = "https://cdn.discordapp.com/attachments/1193235978027024504/1375798605436289054/standard.gif?ex=6832ffcc&is=6831ae4c&hm=362b64c2240262ffaf83246e31e4608db6da80e08c8fb5cc6bdd293799174124&"  # Replace with your actual image link

@bot.event
async def on_ready():
    print(f"<:1307915427644440596:1375850805541732392> Bot is online as {bot.user}")

@bot.command()
@commands.has_permissions(administrator=True)
async def send_verify_embed(ctx):
    embed = discord.Embed(title="VERIFY HERE <a:1149083222723022978:1375850567817101383>", description="REACT <:1307915427644440596:1375850805541732392> TO VERIFY NOW", color=0x00ff00)
    embed.set_image(url=VERIFY_IMAGE_URL)

    message = await ctx.send(embed=embed)
    await message.add_reaction(VERIFY_EMOJI)

    # Save the message ID for future use
    with open("verify_msg.txt", "w") as f:
        f.write(str(message.id))

@bot.event
async def on_raw_reaction_add(payload):
    if payload.member.bot:
        return

    # Load the stored verification message ID
    try:
        with open("verify_msg.txt", "r") as f:
            verify_message_id = int(f.read())
    except FileNotFoundError:
        return

    if payload.message_id != verify_message_id or str(payload.emoji) != VERIFY_EMOJI:
        return

    guild = bot.get_guild(payload.guild_id)
    role = discord.utils.get(guild.roles, name=VERIFIED_ROLE_NAME)
    member = guild.get_member(payload.user_id)

    if role and member:
        await member.add_roles(role)
        channel = guild.get_channel(payload.channel_id)
        if channel:
            try:
                await channel.send(f"{member.mention}, <a:1149083222723022978:1375850567817101383> you are now verified!", delete_after=10)
            except discord.Forbidden:
                pass

bot.run(os.environ['TOKEN'])








