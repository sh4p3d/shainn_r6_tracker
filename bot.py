from forex_python.converter import CurrencyRates
import discord
from discord.ext import commands
from time import sleep
from bs4 import BeautifulSoup
import requests
import os 
f = open('TOKEN.txt', 'r')
TOKEN = f.read()
f.close()
prefix = '!'

#ranked bilgileri alinacak

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
async def r6stats(ctx, username, platform="pc", ranked=""):
    url = f"https://r6.tracker.network/profile/{platform}/{username}"
    result = requests.get(url)
    doc = BeautifulSoup(result.content,features="lxml")
    firststats = doc.find_all(class_="trn-defstat__value-stylized")
    secondstats = doc.find_all(class_="trn-defstat__value")
    
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
        embed1=discord.Embed(title="Ranked Stats", description=f"\nRanked Time Played:{rankedtimePlayed}\nRanked Wins:{rankedwins}\nRanked Losses:{rankedlosses}\nRanked Matches:{rankedmatches}\nRanked Deaths:{rankeddeaths}\nRanked Kills:{rankedkills}\nRanked WL%:{rankedWLRatio}\nRankedKDRatio:{rankedKDRatio}\nRanked Kills Per Match:{rankedKillsPerMatch}\nRanked Kills Per Minute:{rankedKillsPerMinute}", color=0xFFA500)
        await ctx.channel.send(embed=embed1)
    else:
        await ctx.channel.send(f"Stats of {username} in the platform {platform}:")
        if firststats[2].string == None:
            level = firststats[0].string

            embed1=discord.Embed(title="Overall Stats", description="\nLevel: " + level + "\nWin%: " + winRatio  + "\nKDRatio: " + KDRatio, color=0xFF5733)
            embed1.set_author(name="R6 Stats", icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed=embed1)
            embed2 = discord.Embed(title="Other Stats(General)", description="\nWins: " + wins +  "\nKills: " + kills + "\nDeaths: " + deaths + "\nLosses" + loses + "\nTime Played: " + matchesPlayed + "\nHeadshot%: " + headshotAccuracy, color =0x5733FF)
            await ctx.send(embed=embed2)

        else:
            bestmmr = firststats[0].string
            level = firststats[1].string
            averageSeasonEnjoyer = firststats[2].string

            embed1=discord.Embed(title="Overall Stats", description="Best Mmr: " + bestmmr+"\nLevel: " + level +"\nAverage Seasonal Mmr: " + averageSeasonEnjoyer + "\nWin%: " + winRatio  + "\nKDRatio: " + KDRatio, color=0xFF5733)
            embed1.set_author(name="R6 Stats", icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed=embed1)
            embed2 = discord.Embed(title="Other Stats(General)", description="\nWins: " + wins +  "\nKills: " + kills + "\nDeaths: " + deaths + "\nLosses" + loses + "\nTime Played: " + matchesPlayed + "\nHeadshot%: " + headshotAccuracy, color =0x5733FF)
            await ctx.send(embed=embed2)


@bot.command()
async def convcurr(ctx, amount, Currency1, Currency2):
    c = CurrencyRates()
    result = c.convert(Currency1, Currency2, int(amount))
    await ctx.channel.send(f"{amount} {Currency1} is approximately {result} {Currency2}")

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