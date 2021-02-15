import os
import random
import discord
from dotenv import load_dotenv
import string
from googlesearch import search
from bs4 import BeautifulSoup
import requests
from youtubesearchpython import SearchVideos, Search
from youtubesearchpython.internal.constants import ResultMode

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="fortnite funny moments"))

@client.event
async def on_message(msg):
    if msg.author == client.user: #ignores the message if it comes from the bot
        return

    #splits the message to find the arguments. stored in the format of a list
    splitMsg = msg.content.split(' ')
    args = splitMsg[1:]

    #Confession handler. Looks for DMs and sends them for approval.
    if isinstance(msg.channel, discord.channel.DMChannel):

        #stores confessions in a seperate text document
        with open("confessions.txt", "r+") as file:
            count = len(file.readlines())
            file.write(msg.content + "\n")
            file.close()

        print("Confession Received")
        approvalChannel = client.get_channel(772794910826430494)
        fullConfession = "#" + str(count) + ": ", str(msg.content)
        await approvalChannel.send(''.join(fullConfession))

    #Checks whether the message starts with the prefix. If this is not there, bot replies to every message
    if msg.content.startswith("="):
        if msg.content.startswith('=ping'): #ping command
            await msg.channel.send('Pong!')
        elif msg.content.startswith('=help'): #help command
            await msg.channel.send('jeuseBot\'s help menu can be found at: http://jb.joemama.site')
        elif msg.content.startswith('=sunglasses'): #sunglasses command
            if msg.author.id == 258582004738555904:
                await msg.channel.send("<@258582004738555904> is SO FUCKING COOL. All the ladies fall for him wherever he goes. He is super cool and super smart and super amazing and is the perfect specimen of human being. I really fucking love him because he is so cool and he also made me so that makes him EXTRA COOL!!!!!!!!!!!!!!!!!")
            else:
                await msg.channel.send(":sunglasses: im really cool, and so is <@" + str(msg.author.id) + ">")
        elif msg.content.startswith('=speak'): #speak command
            await msg.channel.send(' '.join(args))
        elif msg.content.startswith('=avatar') or msg.content.startswith('=pfp'): #pfp command
            if msg.content == "=pfp" or msg.content == "=avatar" :
                await msg.channel.send("Your avatar: " + str(msg.author.avatar_url))
            else:
                mentioned = msg.mentions[0]
                await msg.channel.send("<@" + str(mentioned.id) + ">\'s avatar is: " + str(mentioned.avatar_url))
        elif msg.content == '=fuck you': #insult command
            await msg.channel.send("Ay fuck you too, buddy")
        elif msg.content.startswith("=random"): #rng command
            if args:
                await msg.channel.send(random.randint(0, int(args[0])))
            else:
                await msg.channel.send(random.randint(0, 10))
        elif msg.content.startswith("=math") or msg.content.startswith("=calc") or msg.content.startswith("=calculate") or msg.content.startswith("=maths"):
            if len(args) > 50:
                await msg.channel.send("There's too many numbers!")
            else:
                for character in list(args):
                    if character in [string.ascii_letters, '[', ']', '{', '}', ',' , '#'] or character in [letter for letter in string.ascii_letters]:
                        break
                    else:
                        answer = eval(str(''.join(args)))
                await msg.channel.send('```' + str(answer) + '```')
        elif msg.content.startswith("=a"):
            #opens the text document from previous code, stores all confessions in a list
            with open('confessions.txt', 'r') as data:
                data = data.readlines()

            numToApprove = splitMsg.pop(1)
            print("confession #" + numToApprove, "will be approved.")
            confessionChannel = client.get_channel(772794910826430494)
            await confessionChannel.send("Confession received: " + data[int(numToApprove)])
        elif msg.content.startswith('=github'):
            await msg.channel.send("jeuseBot's code can be found at: https://github.com/Meme25327/jeuseBot")
        elif msg.content.startswith('=ftoc'):
            farenheit = float(args[0])
            celsius = str(int((farenheit - 32) * 5/9))
            result = str(farenheit) + " degrees farenheit is equal to " + str(celsius) + " degrees celsius."
            await msg.channel.send(''.join(result))
        elif msg.content.startswith("=ctof"):
            celsius = float(args[0])
            farenheit = str(int((celsius * 9/5) + 32))
            result = str(celsius) + " degrees celsius is equal to " + str(farenheit) + " degrees farenheit"
            msg.channel.send(''.join(result))
        elif msg.content.startswith('=g') or msg.content.startswith('=google'):
            query = ''.join(args)

            if len(query) == 0:
                await msg.channel.send("No query given")
                return

            print("google search requested: " + query)

            embed = discord.Embed(title = "Search Results")
            num = 0

            headers = {'User-Agent': 'Mozilla/5.0'}
            
            for results in search(query, num = 1, stop = 3, pause = 1, tld = "co.in"):
                print(results)
                num += 1
                reqs = requests.get(results)
                soup = BeautifulSoup(reqs.text, 'html.parser')
                siteTitle = ''
                for title in soup.find_all('title'): 
                    siteTitle = title.get_text()
                name = str(num) + ": " + str(siteTitle)
                embed.add_field(name = name, value = results, inline = False)

            await msg.channel.send(embed = embed)
        elif msg.content.startswith('=yt') or msg.content.startswith('=youtube'):
            query = ''.join(args)
            results = Search(query, limit = 1)
            info = results.result(mode = ResultMode.dict)
            embed = discord.Embed(title = 'YouTube Results')
            print(info)
            print("--------------------------------------------------------------------------------------------------------------")
            title = info['result'][0]['title']
            url = info['result'][0]['link']
            type = info['result'][0]['type']
            video = '**', title, '**', ' (', type, ')', ':' '\n', url
            await msg.channel.send(''.join(video))
        elif msg.content.startswith('=img') or msg.content.startswith('-image'):
            return
        else:
            await msg.channel.send('Command not recognized. Try =help!')

client.run(TOKEN)