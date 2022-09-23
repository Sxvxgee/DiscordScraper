import random

from rich.progress import track
from discord import Client, Guild
from internal.utils import get_account_settings, create_guild_directory, create_member_file, download_pfp, Logger

client = Client(chunk_guilds_at_startup = False)
logger = Logger(client)

data = get_account_settings()

async def scrape(guild: Guild):
  logger.scraper("Starting...")
  members = await guild.fetch_members([random.choice(guild.channels)])
  members = [member for member in members if not member.bot]
  logger.success("Fetched members successfully")
  return members

@client.listen("on_ready")
async def ready():
  logger.scraper(f"Logged in as {client.user}")
  guild_id = data["guild_id"]
  guild = client.get_guild(int(guild_id))
  create_guild_directory(guild)
  members = await scrape(guild)

  for member in track(members, description = "[bold white][Scraper] Scraping profiles...[/]", refresh_per_second = 100000):
    await create_member_file(member)
    await download_pfp(member)

  logger.success("Finished scraping members profiles and data.\n")
  logger.scraper("Don\"t forget to star the repo and follow Sxvxgee on github!")