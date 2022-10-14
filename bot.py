
from datetime import datetime
from datetime import timedelta
import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
import redis
f = open('TOKEN.txt', 'r')
TOKEN = f.read()
f.close()
prefix = '!'
r6StatsUrl ="https://r6.tracker.network/profile/pc/sh4p3.0507"
bot = commands.Bot(command_prefix=prefix, intents = discord.Intents.all())
bot.remove_command("help")

r = redis.StrictRedis(host="localhost", port="2050", decode_responses=True)

class CacheObject():
    def __init__(self, title, desc, color):
        self.title = title
        self.desc = desc 
        self.color = color 

@bot.event
async def on_ready():
    print('logged in problemless as {0.user}'.format(bot))
    totalservercount = 0
    activeservers = bot.guilds
    print("Active Servers\n ")
    for guild in activeservers:
        print(guild.name)
        totalservercount += 1
    print(f"Bot is in total at the moment in {totalservercount} servers")

@bot.command()
async def ping(ctx):
    await ctx.channel.send(f"Ping:{round(bot.latency * 1000)} ms")

#-----------------------------------------------------------------------------------------

@bot.command()
async def r6stats(ctx, username, platform="pc", ranked=""):
    if r.exists(ctx.author.id):
        return 0
    else:
        r.psetex(ctx.author.id,5000,0)
        url = f"https://r6.tracker.network/profile/{platform}/{username}"
        result = requests.get(url)
        doc = BeautifulSoup(result.content,features="lxml")
        firststats = doc.find_all(class_="trn-defstat__value-stylized")
        secondstats = doc.find_all(class_="trn-defstat__value")
        try:
            wins = secondstats[1].string
            winRatio = secondstats[2].string
            kills = secondstats[3].string
            KDRatio = secondstats[4].string
            deaths = secondstats[10].string
            loses = secondstats[12].string
            matchesPlayed = secondstats[15].string
            headshotAccuracy = secondstats[16].string
            rankedtimePlayed = secondstats[21].string

            if ranked == "ranked" and rankedtimePlayed == '\n':
                await ctx.channel.send("You didn't play enough ranked so i don't have enough value to show.")
            elif ranked == "ranked" and secondstats[21] != None:
                await ctx.channel.send(f"Ranked stats of {username} in the platform {platform}:")
        
                rankedwins = secondstats[22].string
                rankedlosses = secondstats[23].string
                rankedmatches = secondstats[24].string
                rankeddeaths = secondstats[25].string
                rankedkills = secondstats[26].string
                rankedWLRatio = secondstats[27].string
                rankedKDRatio = secondstats[28].string
                rankedKillsPerMatch = secondstats[29].string
                rankedKillsPerMinute = secondstats[30].string
                xtitle="Ranked Stats"
                xdesc=f"\nRanked Time Played:{rankedtimePlayed}\nRanked Wins:{rankedwins}\nRanked Losses:{rankedlosses}\nRanked Matches:{rankedmatches}\nRanked Deaths:{rankeddeaths}\nRanked Kills:{rankedkills}\nRanked WL%:{rankedWLRatio}\nRankedKDRatio:{rankedKDRatio}\nRanked Kills Per Match:{rankedKillsPerMatch}\nRanked Kills Per Minute:{rankedKillsPerMinute}"
                color=0xFFA500
                embed1=discord.Embed(title=xtitle, description=xdesc, color=color)
                await ctx.channel.send(embed=embed1)
            else:
                await ctx.channel.send(f"Stats of {username} in the platform {platform}:")
                if firststats[2].string == None:
                    level = firststats[0].string

                    embed1=discord.Embed(title="Overall Stats", description="\nLevel: " + level + "\nWin%: " + winRatio  + "\nKDRatio: " + KDRatio, color=0xFF5733)
                    embed1.set_author(name="R6 Stats", icon_url=ctx.author.avatar.url)
                    await ctx.channel.send(embed=embed1)
                    embed2 = discord.Embed(title="Other Stats(General)", description="\nWins: " + wins +  "\nKills: " + kills + "\nDeaths: " + deaths + "\nLosses" + loses + "\nTime Played: " + matchesPlayed + "\nHeadshot%: " + headshotAccuracy, color =0x5733FF)
                    await ctx.send(embed=embed2)

                else:
                    bestmmr = firststats[0].string
                    level = firststats[1].string
                    averageSeasonEnjoyer = firststats[2].string

                    embed1=discord.Embed(title="Overall Stats", description="Best Mmr: " + bestmmr+"\nLevel: " + level +"\nAverage Seasonal Mmr: " + averageSeasonEnjoyer + "\nWin%: " + winRatio  + "\nKDRatio: " + KDRatio, color=0xFF5733)
                    embed1.set_author(name="R6 Stats", icon_url=ctx.author.avatar.url)
                    await ctx.channel.send(embed=embed1)
                    embed2 = discord.Embed(title="Other Stats(General)", description="\nWins: " + wins +  "\nKills: " + kills + "\nDeaths: " + deaths + "\nLosses" + loses + "\nTime Played: " + matchesPlayed + "\nHeadshot%: " + headshotAccuracy, color =0x5733FF)
                    await ctx.send(embed=embed2)
        except IndexError:
            await ctx.channel.send("Please write in the following format:\n!r6stats {username} {(platform)} {(ranked)}\nReminder:It is not necessary to write platform and ranked")

@bot.group(invoke_without_command=True)
async def help(ctx):
        embedHelp = discord.Embed(title="Help", description="!r6stats username (platform) [ranked]\n!ping")
        await ctx.send(embed=embedHelp)
@help.command()
async def r6stats(ctx):
    embedR6Stats = discord.Embed(title="!r6stats", description="This command gives your overall stats.If you type ranked at the end of the command then the bot gives you only the ranked statistics of yours.")
    await ctx.channel.send(embed=embedR6Stats)
@help.command()
async def ping(ctx):
    embedR6Stats = discord.Embed(title="!ping", description="This command tells you the momentary ping of the bot.")
    await ctx.channel.send(embed=embedR6Stats)


bot.run(TOKEN)