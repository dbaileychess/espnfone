import discord
import os

from espn_api.football import League
from espn_fone_client import EspnFoneClient

# Read the private information from enviroment variables
league_id = int(os.environ["LEAGUE_ID"])
espn_s2 = os.environ["ESPN_S2"]
swid = os.environ["SWID"]
bot_token = os.environ["BOT_TOKEN"]
dev_channel_id = int(os.environ["DEV_CHANNEL_ID"])

league = League(league_id=league_id, year=2022, espn_s2=espn_s2, swid=swid)

intents = discord.Intents.default()
intents.message_content = True

client = EspnFoneClient(
    intents=intents,
    league=league,
    dev_channel_id=dev_channel_id,
)
client.run(bot_token)
