import os
import random
import discord
from dotenv import load_dotenv
import string
from googlesearch import search
from bs4 import BeautifulSoup
import requests
from youtubesearchpython import SearchVideos, Search
#from youtubesearchpython.internal.constants import ResultMode
from PIL import Image, ImageFont, ImageDraw
import textwrap
import json
import youtube_dl
import asyncio
from discord.ext import commands
import datetime
import wikipediaapi
from discord.utils import get

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

intents = discord.Intents
intents.members = True

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="fortnite funny moments"))

@client.event
async def on_member_leave(self, member):
    chan = self.bot.get_channel(716887644365258772)
    print("E")
    await chan.send(f"{member.display_name}#{member.tag} just left the server.")


@client.event
async def on_message(msg):
    global nsfwLocked
    with open("data.txt", 'r') as data:
        nsfwLocked = data.readline()
    if msg.author == client.user or msg.author.id in [194186448277078016, 253213361938890753]: #ignores the message if it comes from the bot, list is banned users
        return
    chance = random.randint(1, 250)
    if msg.channel.id == 671429515846615110:
        chance = 0
    if chance == 250:
        #await msg.channel.send("https://images-ext-1.discordapp.net/external/m_y7k6wh-vwjl7jZisRBuzehmiNj76kj3c0Zidj0YD0/https/media.discordapp.net/attachments/853014263260774400/946064570190037032/m-1.gif")
        speechGifs = ["https://tenor.com/view/lil-nas-x-nickb-pregnant-speech-bubble-gif-25238772", "https://tenor.com/view/speech-bubble-cat-talking-reply-gif-24471552", "https://media.discordapp.net/attachments/724646506698637422/962039536198758440/strangledsay-1.gif", "https://tenor.com/view/speech-bubble-tourneycord-gif-25096367"]
        randomGif = random.randint(0, 3)
        print(speechGifs[randomGif])
        await msg.channel.send(speechGifs[randomGif])
        if msg.channel.id == 976794585378480188:
            print(nsfwLocked)
            if nsfwLocked == 'False':
                print("NSFW CLOSING!!!!!")
                await msg.channel.send("#nsfw is now closed.")
                await lockChannel(976794585378480188, msg)
                await msg.channel.send("#nsfw is now closed.")
                print("closed")
                with open('data.txt', 'w') as data:
                    data.write("True")
        else:
            print("NSFW opening")
            await unlockChannel(933273342419542066, msg)
            print("open")
            with open('data.txt', 'w') as data:
                data.write("False")
            await msg.channel.send("#nsfw is now open.")

    #splits the message to find the arguments. stored in the format of a list
    splitMsg = msg.content.split(' ')
    args = splitMsg[1:]

    if msg.attachments:
        msg.content = msg.content + " " + msg.attachments[0].proxy_url

    #Confession handler. Looks for DMs and sends them for approval.
    if isinstance(msg.channel, discord.channel.DMChannel):

        #stores confessions in a seperate text document
        rawMsg = str(msg.content)
        confession = rawMsg.replace('\n', '. ').replace(' .', '.').replace('.. ', '. ')
        with open("confessions.txt", "a+") as file:
            count = len(file.readlines())
            
            print(confession)
        
            file.write(confession + "\n")
            file.close()
        print("Confession Received")
        approvalChannel = client.get_channel(908646167146012716) #should end with 2716 when running
        fullConfession = confession
        #confessionChannel = client.get_channel(740256233403056158) #should end with 0494 when running
        if "<@" in msg.content:
            await msg.channel.send("You can't ping anyone in a confession. If you're calling out someone specific, you can still use their name, just not ping them")
        else:
            await approvalChannel.send('Message Received: ' + ''.join(fullConfession))

        '''if msg.content.startswith("=a") and msg.channel.id == 772780671634374677:#should end with 0466 when running
            with open("confessions.txt", 'r') as file:
                lines = file.readlines()
                num = args[0]
                print(lines[-num])
                await confessionChannel.send(lines[-num])'''

    #Checks whether the message starts with the prefix. If this is not there, bot replies to every message
    if msg.content.startswith("="):
        if msg.content.startswith('=ping'): #ping command
            await msg.channel.send('Pong!')
        elif msg.content.startswith('=help'): #help command
            await msg.channel.send('jeuseBot\'s help menu can be found at: https://meme25327.github.io/jeuseBot/')
        elif msg.content.startswith('=sunglasses'): #sunglasses command
            if msg.author.id == 258582004738555904:
                await msg.channel.send("<@258582004738555904> is SO FUCKING COOL. All the ladies fall for him wherever he goes. He is super cool and super smart and super amazing and is the perfect specimen of human being. I really fucking love him because he is so cool and he also made me so that makes him EXTRA COOL!!!!!!!!!!!!!!!!!")
            elif msg.author.id == 445130486491119627:
                await msg.channel.send("<@445130486491119627> is better than u.")
            elif msg.author.id == 187160540995387392:
                await msg.channel.send("B)")
            else:
                await msg.channel.send(":sunglasses: im really cool, and so is <@" + str(msg.author.id) + ">")
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
                for character in ''.join(args).strip(" "):
                    print(''.join(args).strip(" "))
                    if character in [string.ascii_letters, '[', ']', '{', '}', ',' , '#'] or character in [letter for letter in string.ascii_letters]:
                        break
                    else:
                        try:
                            checker = ''.join(args)
                            if "exec" in checker:
                                await msg.channel.send("Naughty, naughty...")
                                break
                            answer = eval(str(''.join(args)))
                        except ZeroDivisionError:
                            #await msg.channel.send('The answer is: "a/b is the unique solution to the equation bz=a." (I am using z as the unknown, since you are using x for other things). Given that answer, let us discuss your points out of order: (3) is perfectly fine: 0/x, with x≠0, is the solution to xz=0; the unique solution is z=0, so 0/x=z. The reason it's unique is because x≠0, so the only way for the product to be 0 is if z is 0. In (1), by "impossible" we mean that the equation that defines it has no solutions: for something to be equal to x/0, with x≠0, we would need 0z=x. But 0z=0 for any z, so there are no solutions to the equation. Since there are no solutions to the equation, there is no such thing as "x/0". So x/0 does not represent any number. In (2), the situation is a bit trickier; in terms of the defining equation, the problem here is that the equation 0z=0 has any value of z as a solution (that's what the "infinite solutions" means). Since the expression a/b means "the unique solution to bx=a, then when a=b=0, you don't have a unique answer, so there is no "unique solution" . Generally speaking, we simply do not define "division by 0". The issue is that, once you get to calculus, you are going to find situations where you have two variable quantities, a and b, and you are considering a/b; and as a and b changes, you want to know what happens to a/b. In those situations, if a is approaching x and b is approaching y≠0, then a/b will approach x/y, no problem. If a approaches x≠0, and b approaches 0, then a/b does not approach anything (the "limits does not exist"). But if both a and b approach 0, then you don't know what happens to a/b; it can exist, not exist, or approach pretty much any number. We say this kind of limit is "indeterminate". So there is a reason for separating out cases (1) and (2): very soon you will see an important qualitative difference between the first kind of "does not exist" and the second kind.'))
                            await msg.channel.send("https://math.stackexchange.com/questions/26445/division-by-zero")
                await msg.channel.send('```' + str(answer) + '```')
        elif msg.content.startswith("=a"):
            if msg.channel.id == 908646167146012716: #approval channel should end with 2716 when running
                #opens the text document from previous code, stores all confessions in a list
                with open('confessions.txt', 'r') as data:
                    data = data.readlines()
                    try:
                        numToApprove = splitMsg.pop(1)
                    except:
                        numToApprove = 1
                if numToApprove == "nsfw" or numToApprove == "spoil":
                    numToApprove = 1
                print("confession #" + str(numToApprove), "will be approved.")
                confessionChannel = client.get_channel(772794910826430494) #should end with 0494 when running
                
                if len(args) > 0:
                    print("ge")
                    if "spoil" in args and "nsfw" in args:
                        confession = "||" + data[-(int(numToApprove))][:-1] + "|| (spoiler tags typically indicate sensitive content)"
                        nsfwConfessionChannel = client.get_channel(976794585378480188) #should end with 6672 when running
                        await nsfwConfessionChannel.send("Message received: " + confession)
                    if "spoil" in args and "nsfw" not in args:
                        confession = "|| " + data[-(int(numToApprove))][:-1] + " || (spoiler tags typically indicate sensitive content)"
                        await confessionChannel.send("Message received: " + confession)
                    '''else:
                        approvalChannel = client.get_channel(772780671634374677) #should end with 0466 when running
                        await approvalChannel.send("Please try that again!")'''
                    if "nsfw" in args and "spoil" not in args:
                        nsfwConfessionChannel = client.get_channel(976794585378480188) #should end with 6672 when running
                        await nsfwConfessionChannel.send("Message received: " + data[-int(numToApprove)])
                    if "nsfw" not in args and "spoil" not in args:
                        confession = data[-int(numToApprove)]
                        await confessionChannel.send("Message received: " + confession)
                else:
                    print("waogj")
                    confession = data[-int(numToApprove)]
                    await confessionChannel.send("Message received: " + confession)
            else:
                print("V")
                    
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
            await msg.channel.send(''.join(result))
        elif msg.content.startswith('=g') or msg.content.startswith('=google'):
            query = ' '.join(args)
            
            if len(query) == 0:
                await msg.channel.send("No query given")
                return

            await msg.channel.send("Searching for ***" + query + "***. This may take some time, so please be patient.")
            print("google search requested: " + query)

            embed = discord.Embed(title = "Search Results")
            num = 0

            headers = {'User-Agent': 'Mozilla/5.0'}
            
            for results in search(query, 1, 1, 0):
                print(results)
                num += 1
                try:
                    reqs = requests.get(results)
                except:
                    await msg.channel.send("```bot bronk. jeuse knows so don't bother him about it.```")
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
            print(results)
            info = results.result(mode = ResultMode.dict)
            embed = discord.Embed(title = 'YouTube Results')
            print(info)
            print("--------------------------------------------------------------------------------------------------------------")
            try:
                title = info['result'][0]['title']
                url = info['result'][0]['link']
                type = info['result'][0]['type']
                video = '**', title, '**', ' (', type, ')', ':' '\n', url
                await msg.channel.send(''.join(video))
            except IndexError:
                await msg.channel.send("Sorry, no results found. Try refining your query or fixing any typos.")
        elif msg.content.startswith('=nick'):
            num = 0
            guild = msg.guild
            for i in guild.members:
                print(guild.members)

            '''print(memberList)
            for mem in memberList:
                if str(args[0]) == "reset":
                    await mem.edit(nick = None)
                else:
                    await mem.edit(nick = str(args[0]))
                num += 1
            await msg.channel.send(num)'''
        elif msg.content.startswith('=truth'):
            with open('truths.txt', 'r') as truths:
                truths = truths.readlines()
                rng = random.randint(0, 83)
                truth = truths[rng]
                await msg.channel.send(truth)
        elif msg.content.startswith('=dare'):
            with open('dares.txt', 'r') as dares:
                dares = dares.readlines()
                rng = random.randint(0, 40)
                dare = dares[rng]
                await msg.channel.send(dare)
        elif msg.content.startswith('=cum'): #shoutout jaggi
            await msg.channel.send( "<@357576484543660043>")
        elif msg.content.startswith('=quote'): #shoutout piracy
            with open('quotes.txt', 'r') as quotes:
                quoteList = quotes.readlines()
                rng = random.randint(0, 30)
                selectedQuote = quoteList[rng]
                print(selectedQuote)
                await msg.channel.send(selectedQuote)
        elif msg.content.startswith('=1984'): #shoutout laura
            if msg.reference:
                repliedMsg = await msg.channel.fetch_message(msg.reference.message_id)
                content = repliedMsg.content
                url = content.replace(' ', '_')
                await msg.channel.send('https://api.memegen.link/images/custom/'+ url + '.png?background=https://i.kym-cdn.com/photos/images/newsfeed/002/223/795/e7c.jpg')
                '''my_image = Image.open("1984.png")
                title_font = ImageFont.truetype('impact.ttf', 50)
                text_to_add = repliedMsg.content
                image_editable = ImageDraw.Draw(my_image)
                width, height = image_editable.textsize(text_to_add, font=title_font)
                lines = textwrap.wrap(text_to_add, width=20)
                y_text = 0
                for line in lines:
                    width, height = title_font.getsize(line)
                    image_editable.text((200 - width/2, y_text), line, font=title_font, stroke_width=5, stroke_fill=(0, 0, 0))
                    y_text += height
                print(width)
                #image_editable.text((200 - width/2, 0), text_to_add, (255, 255, 255), font=title_font)
                my_image.save("result.png")
                file = discord.File("result.png")
                await msg.channel.send(file=file)
                '''
            else:
                url = '_'.join(args)
                await msg.channel.send('https://api.memegen.link/images/custom/' + url + '.png?background=https://i.kym-cdn.com/photos/images/newsfeed/002/223/795/e7c.jpg')
        elif msg.content.startswith('=define'):
            word = args[0]
            headers = {
                'User-Agent': 'RuneXchange',
                'From': 'Meme25327#4475'
            }

            result = requests.get('https://api.dictionaryapi.dev/api/v2/entries/en/' + word, headers = headers)
            resultJson = result.json()
            num = 0
            print("="*30)
            print(word)
            definition1 = resultJson[0]['meanings'][0]['definitions'][0]['definition']
            #print(json.dumps(definition, sort_keys=True, indent = 1))
            embed = discord.Embed(title = "Definition for " + word)
            embed.add_field(name = "Top Result:", value = definition1, inline = False)

            for definitionNo in resultJson[0]['meanings'][0]['definitions']:
                wordDef = resultJson[0]['meanings'][0]['definitions'][num]['definition']
                if num != 0:
                    embed.add_field(name = "Also see:", value = wordDef, inline = False)
                num += 1
            
            await msg.channel.send(embed = embed)
        elif msg.content.startswith('=join'):
            if msg.author.voice:
                global voiceChannel
                voiceChannel = msg.author.voice.channel  
                await voiceChannel.connect()
                await msg.channel.send("Succesfully joined the voice channel!")
            else:
                await msg.channel.send("You need to be in a voice channel to use this command!")
        elif msg.content.startswith("=play"):
            try: 
                print("lol")
            except:
                print("unlol")
        elif msg.content.startswith("=leave"):
            await self.voiceChannel.disconnect()
        elif msg.content == "=sex":
            await msg.channel.send("https://cdn.discordapp.com/attachments/853014263260774400/907336361240043621/image0.gif")
        elif msg.content.startswith("=jerrry"):
            await msg.channel.send("Husband. Entrepreneur. Lover. Top 0.7% of OnlyFans creators.")
        elif msg.content.startswith("=weather"):
            #--------------------get temps-------------
            city = ' '.join(args)
            data = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=f473f2a3e1eb64697114b4dfdbd4e6d5")
            response = data.json()
            responseDict = dict(response)
            try:
                cityStr = ''.join(responseDict["name"] + ", " + responseDict["sys"]["country"])
            except KeyError:
                await msg.channel.send("Couldn't find **" + city + "**. Maybe the city was misspelt, or it isn't in the database.")
            temps = [responseDict["main"]["temp"]-273.15, responseDict["main"]["feels_like"]-273.15]
            #results = "The weather in **", city.capitalize(), "** is: **", str(round(temps[0], 2)) + "c**. It feels like: **", str(round(temps[1], 2))+"**c."
            #------------------end temps------------------
            #------------------get time---------------------
            hours = responseDict["timezone"]
            if hours == 19800:
                hours = 0
            else:
                hours = hours - 19800
            result = datetime.datetime.now() + datetime.timedelta(seconds=hours)
            if len(str(result.hour)) == 1:
                tempStr = "0"
                resultHour = tempStr + str(result.hour)
            else:
                resultHour = str(result.hour)
            if len(str(result.minute)) == 1:
                tempStr2 = "0"
                resultMinute = tempStr2 + str(result.minute)
            else:
                resultMinute = str(result.minute)
            #-------------------end time-----------------------
            #-------------------get descriptor---------------
            usedTemp = int(responseDict["main"]["feels_like"]-273.15)
        
            if usedTemp <= 7:
                descriptor = "Cold"
            else:
                if usedTemp <= 15:
                    descriptor = "Cool"
                else:
                    if usedTemp <= 23:
                        descriptor = "Warm"
                    else:
                        descriptor = "Hot"
            #--------------end descriptor------------------
            #--------------construct embed---------------
            embed = discord.Embed(title = "Weather for " + cityStr, color = 0xFF5733)
            iconCode = responseDict["weather"][0]["icon"]
            embed.set_thumbnail(url = "http://openweathermap.org/img/wn/"+iconCode+"@2x.png")
            embed.add_field(name = 'Temperature', value = "It is **" + str(round(temps[0], 2)) + "c**.", inline = True)
            embed.add_field(name = 'Feels Like', value = "It feels like **"+str(round(temps[1], 2))+"c**.", inline = True)
            embed.add_field(name = 'Time', value = resultHour + ":" + resultMinute, inline = False)
            weather = responseDict["weather"][0]["main"]
            embed.add_field(name = "Weather", value = weather, inline = True)
            embed.add_field(name = 'Description', value = descriptor, inline = True)
            embed.set_footer(text = "Use fahrenheit? Convert celsius to fahrenheit using the `=ctof [celsius]` command!")
            #-----------------end embed-------------------
            await msg.channel.send(embed = embed)
        elif msg.content.startswith("=jesse"):
            await msg.channel.send("https://cdn.discordapp.com/attachments/716887644365258772/914135132183601153/unknown.png")
        elif msg.content.startswith("=sex2014"):
            await msg.channel.send("https://cdn.discordapp.com/attachments/716887644365258772/938846601227673650/sex2014.gif")
        elif msg.content.startswith("=wiki") or msg.content.startswith("=wikipedia"):
            wiki_wiki = wikipediaapi.Wikipedia('en')
            
            splitReq = args
            formattedReq = []
            
            for word in splitReq:
                formattedReq.append(word.capitalize())
                page_py = wiki_wiki.page('_'.join(formattedReq))


            print("="*15, "Wikipedia Search", "="*15)
            print("Page - Title: %s" % page_py.title)
            print("Page - Exists: %s" % page_py.exists())
            print("="*15, "Wikipedia Search", "="*15)
            
            summary = []
            splitSum = page_py.summary.split('. ')
            print("sentence count:", len(splitSum))
            i = 0
            try:
                while len('. '.join(summary)) < 500:
                    summary.append(splitSum[i])
                    i += 1
                summary.append('')
            except IndexError:
                pass
            print("character count:", len(str(summary)))
            print('. '.join(summary))
            print("="*30)
            try:
                url = requests.get("http://en.wikipedia.org/w/api.php?action=query&titles="+' '.join(formattedReq)+"&prop=pageimages&format=json&pithumbsize=500")
                urlJson = url.json()
                print(urlJson)
                pageID = urlJson['query']['pages'].keys()
                thumbnailURL = urlJson['query']['pages'][list(pageID)[0]]['thumbnail']['source']
            except KeyError:
                thumbnailURL = "https://cdn.discordapp.com/attachments/716887644365258772/919215219228704818/unknown.png"
            try:
                embed = discord.Embed(title = "Wikipedia Article for " + ' '.join(args), color = 0xFF5733)
                embed.set_thumbnail(url = thumbnailURL)
                embed.add_field(name = 'Summary', value = '. '.join(summary), inline = True)
                embed.add_field(name = 'Link', value = page_py.canonicalurl, inline = False)
            except:
                await msg.channel.send("Couldn't find that on wikipedia. You could try a google search (`=g`).")
            await msg.channel.send(embed=embed)
        elif msg.content.startswith("=imdb"):
            inputName = '%20'.join(args)

            initResponse = requests.get("https://imdb-api.com/API/SearchTitle/k_5yuw9s65/%s"%inputName)
            initResponseJSON = initResponse.json()

            titleID = initResponseJSON['results'][0]['id']
            titleImage = initResponseJSON['results'][0]['image']

            secondResponse = requests.get("https://imdb-api.com/eng/API/Title/k_5yuw9s65/%s"%titleID)
            secondResponseJSON = secondResponse.json()

            titleName = secondResponseJSON['fullTitle']
            titleType = secondResponseJSON['type']
            titleRuntime = secondResponseJSON['runtimeStr']
            titlePlot = secondResponseJSON['plot']
            titleStars = secondResponseJSON['stars']
            titleGenres = secondResponseJSON['genres']
            titleContentRating = secondResponseJSON['contentRating']
            titleImdbRating = secondResponseJSON['imDbRating']

            #print(titleID, titleName, titleImage, titleType, titleRuntime, titlePlot, titleStars, titleGenres, titleContentRating, titleImdbRating, end='\n')
            embed=discord.Embed(title=titleName, url="https://www.imdb.com/title/%s/"%titleID, description=titleType)
            embed.set_thumbnail(url=titleImage)
            embed.add_field(name="Plot", value=titlePlot, inline=False)
            embed.add_field(name="Runtime", value=titleRuntime, inline=True)
            embed.add_field(name="Genre", value=titleGenres, inline=True)
            embed.add_field(name="Starring", value=titleStars, inline=False)
            embed.add_field(name="Content Rating", value=titleContentRating, inline=True)
            embed.add_field(name="IMDB Rating", value=titleImdbRating, inline=True)
            embed.set_footer(text="https://www.imdb.com/title/%s/"%titleID)
            await msg.channel.send(embed=embed)
        elif msg.content.startswith("=troll"):
            if msg.author.id == 258582004738555904:
                chan = client.get_channel(int(args[0]))
                await chan.send(' '.join(args[1:]))
        elif msg.content.startswith("=lock"):
            if msg.author.id == 258582004738555904:
                #chan = client.get_channel(int(args[0]))
                print("hello")
                await lockChannel(args[0], msg)
        elif msg.content.startswith("=unlock"):
            if msg.author.id == 258582004738555904:
                await unlockChannel(args[0], msg)
        else:
            await msg.channel.send('Command not recognized. Try =help!')
        
async def lockChannel(channelID, msg):
    channel = client.get_channel(int(channelID))
    nsfwLocked = True
    rolesGetList = []
    role = msg.guild.get_role(853001629908074502)
    await channel.set_permissions(role, read_messages=True, send_messages=False)
    await msg.channel.send("locked")

async def unlockChannel(channelID, msg):
    channel = client.get_channel(int(channelID))
    nsfwLocked = False
    role = msg.guild.get_role(853001629908074502)
    await channel.set_permissions(role, read_messages=True, send_messages=True)
    await msg.channel.send("unlocked")


client.run(TOKEN)
