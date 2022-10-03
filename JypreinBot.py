from forex_python.converter import CurrencyRates
import discord
from discord.ext import commands
from time import sleep
from bs4 import BeautifulSoup
import requests

#
#komutlar icin description ve acilan komut menüsü
deranlog_channel = 1022567536589549599
TOKEN = 'MTAyMjU2ODI3OTc3NDA4NTE2MQ.Gq_HQm.693OV-89DWxrG7Csic1b11Y5FhDWwGJ9oEJQoE'

prefix = '!'

r6StatsUrl ="https://r6.tracker.network/profile/pc/sh4p3.0507"
bot = commands.Bot(command_prefix=prefix, intents = discord.Intents.all())

@bot.event
async def on_ready():
    print('logged in problemless as {0.user}'.format(bot))


@bot.command()
async def ping(ctx):
    await ctx.channel.send(f"Ping:{round(bot.latency * 1000)}")

@bot.command()
async def sa(ctx):
    await ctx.channel.send("as")

@bot.command()
async def members_count(ctx):
    await ctx.channel.send(f"Members Count: {ctx.guild.member_count}")

@bot.command()
async def members(ctx):
    for guild in bot.guilds:
        for member in guild.members:
            print(member)

@bot.command()
async def delete(ctx, amount=5):
    await ctx.channel.purge(limit=amount+1)
    await ctx.channel.send(f"{amount} messages was deleted.")
    sleep(1.5)
    await ctx.channel.purge(limit=1)


@bot.command()
async def r6stats(ctx, username, platform):
    await ctx.channel.send(f"Stats of {username} in the platform {platform}:")
    url = f"https://r6.tracker.network/profile/{platform}/{username}"
    result = requests.get(url)
    doc = BeautifulSoup(result.content,features="lxml")
    firststats = doc.find_all(class_="trn-defstat__value-stylized")

    bestmmr = firststats[0].string

    level = firststats[1].string

    averageSeasonEnjoyer = firststats[2].string

    secondstats = doc.find_all(class_="trn-defstat__value")

    wins = secondstats[1].string
    winRatio = secondstats[2].string
    kills = secondstats[3].string
    KDRatio = secondstats[4].string
    deaths = secondstats[10].string
    loses = secondstats[12].string
    matchesPlayed = secondstats[15].string
    headshotAccuracy = secondstats[16].string

    embed1=discord.Embed(title="Overall Stats", url=url, description="Best Mmr: " + bestmmr+"\nLevel: " + level +"\nAverage Seasonal Mmr: " + averageSeasonEnjoyer + "\nWin%: " + winRatio  + "\nKDRatio: " + KDRatio, color=0xFF5733)
    embed1.set_author(name="R6 Stats", url=url, icon_url=ctx.author.avatar_url)
    await ctx.channel.send(embed=embed1)
    embed2 = discord.Embed(title="Other Stats(General)", description="\nWins: " + wins +  "\nKills: " + kills + "\nDeaths: " + deaths + "\nLosses" + loses + "\nTime Played: " + matchesPlayed + "\nHeadshot%: " + headshotAccuracy, color =0x5733FF)
    await ctx.send(embed=embed2)


@bot.command()
async def convcurr(ctx, amount, Currency1, Currency2):
    c = CurrencyRates()
    result = c.convert(Currency1, Currency2, int(amount))
    await ctx.channel.send(f"{amount} {Currency1} is {result} {Currency2}")
    
#@bot.command()
#async def kick(ctx, member : discord.Member, *, reason=None):
#    await member.kick(reason=reason)

#@bot.command()
#async def addrole(ctx, role:discord.Role,user:discord.Member):
#    await user.add_roles(role)
#    await ctx.send(f"Succesfully given {role.mention} to {user.mention}")
#@bot.command()
#async def takerole(ctx, role:discord.Role,user:discord.Member):
#    await user.remove_roles(role)
#    await ctx.send(f"Succesfully taken the role {role.mention} from the user {user.mention}")


bot.run(TOKEN)