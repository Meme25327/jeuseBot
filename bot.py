'''
TODO:
-Approval
-Google
-Youtube
-Image
'''

import random
import os
import datetime
import string
from unicodedata import name
import requests
import asyncio

import wikipediaapi
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Fortnite"))


@client.event
async def on_message(msg):
    if msg.author == client.user: #ignores the message if it comes from the bot
        return

    #splits the message to find the arguments. stored in the format of a list
    splitMsg = msg.content.split(' ')
    global args
    args = splitMsg[1:]

    if msg.attachments:
        msg.content = msg.content + " " + msg.attachments[0].proxy_url

    #Confession handler. Looks for DMs and sends them for approval.
    if isinstance(msg.channel, discord.channel.DMChannel):
        await confessionHandler(msg)
    else:        
        chance = random.randint(1, 250)
        if chance == 251: #reply gif joke
            gifs = ["media/cat.gif", "media/crash.gif", "media/mammoth.gif", "media/nasx.gif", "media/strangled.gif"]
            chosenGif = random.randint(0, len(gifs)-1)
            await msg.channel.send(file=discord.File(gifs[chosenGif]))
        
    #Check Commands_____________________________________________________________________________________________________________________________________________________________
    #line is there so i can spot it easily -jeuse    
    if msg.content.startswith('='):
        print("="*30)
        print("Command Used:", splitMsg[0][1:])
        print("="*30)
        try:
            match splitMsg[0][1:]: #splitMsg[0][1:] is the command
                case 'ping':
                    await pingCommand(msg)
                case 'help':
                    await helpCommand(msg)
                case ('sunglasses'|'cool'):
                    await coolCommand(msg)
                case 'pfp':
                    await pfpCommand(msg)
                case ('random'|'rng'):
                    await rngCommand(msg)
                case ('math'|'maths'|'calc'|'calculate'):
                    await mathCommand(msg)
                case 'github':
                    await githubCommand(msg)
                case 'ftoc':
                    await ftocCommand(msg)
                case 'ctof':
                    await ctofCommand(msg)
                case '1984':
                    await command1984(msg) #shoutout laura
                case 'truth':
                    await truthCommand(msg)
                case 'dare':
                    await dareCommand(msg)
                case 'imdb':
                    await imdbCommand(msg)
                case 'define':
                    await defineCommand(msg)
                case ('jerry' | 'jerrry'):
                    await jerryCommand(msg)
                case ('weather' | 'w'):
                    await weatherCommand(msg)
                case 'jesse':
                    await jesseCommand(msg)
                case 'sex':
                    await sexCommand(msg)
                case 'sex2014':
                    await sex2014Command(msg)
                case ('wikipedia' | 'wiki'):
                    await wikipediaCommand(msg)
                case ('a'):
                    await approvalCommand(msg)
                case ('pokedex' | 'poke' | 'pokemon' | 'dex'):
                    await pokedexCommand(msg)
                case 'join':
                    await joinCommand(msg)
                case 'play':
                    await playCommand(msg)
                case 'svname':
                    await svNameCommand(msg)
                case 'stopsvname':
                    await stopSvNameCommand(msg)
                case 'test':
                    await testCommand(msg)
                case _: #catch-all case
                    await msg.channel.send("`Command not recognized! Try =help.`")
        except Exception as error:
            #Error handler, should catch any error in any command
            embed = discord.Embed()
            embed.add_field(name='ERROR', value="Uh oh! The bot broke! Not to fear, jeuse has been pinged! (If he's not in the server, bug him personally at <@258582004738555904>). The error is down here:", inline=False)
            embed.add_field(name='Description', value="```%s```"%str(error))
            await msg.channel.send(embed=embed)
            jeuse = await client.fetch_user('258582004738555904')
            if msg.author.id != 258582004738555904:
                await jeuse.send(msg.jump_url, embed=embed)
            print(">"*60, "!!ERROR IN ABOVE COMMAND!!")        

#COMMANDS FUNCTIONS START ---------------------------------------------------------------------------------------------------------------
#lined so i can find it easier -jeuse

async def confessionHandler(msg):
        confession = str(msg.content)

        #print confession
        print('='*30)
        print("Confession Received: %s" % confession)
        print('='*30)

        approvalChannel = client.get_channel(992071503392817174) #should end with 7174 when running

        if "<@" in msg.content: #ensures people can't ping other people in a confession
            await msg.channel.send("Pinging is not allowed in a confession.")
        else:
            await approvalChannel.send('Message Received: ' + ''.join(confession))
            emoji = '\N{THUMBS UP SIGN}'
            await msg.add_reaction(emoji)

async def pingCommand(msg):
    timeDif = datetime.datetime.utcnow() - msg.created_at
    pong = "Pong! Responded in: 0." + str(timeDif)[-4:-7:-1] + " seconds!"
    await msg.channel.send(pong)

async def helpCommand(msg):
    embed = discord.Embed(title="jeuseBot Help Menu")
    embed.add_field(name="=ping", value="Pings the bot", inline=False)
    embed.add_field(name="=help", value="DMs you this embed", inline=False)
    embed.add_field(name="=sunglasses OR =cool", value="Compliments you", inline=False)
    embed.add_field(name="=pfp", value="Links the PFP of a mentioned user (Links your PFP if no one is mentioned)", inline=False)
    embed.add_field(name="=random OR =rng", value="Generates a random number (between 0 and 100 if no limit provided, between 0 and any given number, or between any two given numbers)", inline=False)
    embed.add_field(name="=math OR =maths OR =calc OR =calculate", value="Computes a given equation", inline=False)
    embed.add_field(name="=github", value="Links jeuseBot's github page", inline=False)
    embed.add_field(name="=ftoc", value="Converts a given fahrenheit temperature to celsius", inline=False)
    embed.add_field(name="=ctof", value="Converts a given celsius temperature to fahrenheit", inline=False)
    embed.add_field(name="=1984", value="When used in reply to a message, puts the message text on a still from 1984 (1984). If not used in a reply, it puts whatever text you give on the still (unless it's a link) (shoutout Laura btw)", inline=False)
    embed.add_field(name="=truth", value="Picks a random truth", inline=False)
    embed.add_field(name="=dare", value="Picks a random dare", inline=False)
    embed.add_field(name="=imdb", value="Returns an IMDB summary of a given movie", inline=False)
    embed.add_field(name="=define", value="Defines a given word", inline=False)
    embed.add_field(name="=jerry OR =jerrry", value="Shouts out my main man Jerry (shoutout Jerry btw)", inline=False)
    embed.add_field(name="=weather OR =w", value="Returns a weather summary of a given place", inline=False)
    embed.add_field(name="=jesse", value="Posts a still from El Camino (2019)", inline=False)
    embed.add_field(name="=sex", value="Posts The Rock raising his eyebrow (shoutout updog btw)", inline=False)
    embed.add_field(name="=sex2014", value="Posts The Rock raising his eyebrow but in Fortnite: Battle Royale (shoutout Puresh btw)", inline=False)
    embed.add_field(name="=wikipidea OR =wiki", value="Returns a summary of a given topic's wikipedia article", inline=False)
    embed.add_field(name="=pokedex OR =pokemon", value="Look up a pokemon on the pokedex", inline=False)
    embed.set_footer(text="Please do not try to use commands in DMs, jeuseBot will not respond.")
    await msg.author.send(embed = embed)
    await msg.channel.send("Check your DMs!")

async def coolCommand(msg):
    if msg.author.id == 258582004738555904: #jeuse
        await msg.channel.send("<@258582004738555904> is SO FUCKING COOL. All the ladies fall for him wherever he goes. He is super cool and super smart and super amazing and is the perfect specimen of human being. I really fucking love him because he is so cool and he also made me so that makes him EXTRA COOL!!!!!!!!!!!!!!!!!")
    elif msg.author.id == 445130486491119627: #jerry
        await msg.channel.send("<@445130486491119627> is better than u.")
    elif msg.author.id == 187160540995387392: #updog
        await msg.channel.send("B)")
    else:
        await msg.channel.send(":sunglasses: im really cool, and so is <@" + str(msg.author.id) + ">")

async def pfpCommand(msg):
    if args:
        mentioned = msg.mentions[0]
        url = str(mentioned.avatar_url)
    else:
        url = str(msg.author.avatar_url)
    embed = discord.Embed()
    embed.set_image(url=url)
    embed.description = "[URL](%s)"%url
    await msg.channel.send(embed=embed)

async def rngCommand(msg):
    match len(args):
        case 0:
            randNo = random.randint(0, 100)
        case 1:
            upperLimit = int(args[0])
            randNo = random.randint(0, upperLimit)
        case 2:
            upperLimit, lowerLimit = int(max(map(int, args))), int(min(map(int, args)))
            randNo = random.randint(lowerLimit, upperLimit)
        case _: #catch-all case
            await msg.channel.send("`An error occurred. Please try again.`")
    await msg.channel.send('```%s```'%str(randNo))

async def mathCommand(msg):
    if len(args) > 50:
        await msg.channel.send("`There's too many numbers!`")
    else:
        i=0
        for character in list(args)[i]:
            if character in [string.ascii_letters, '[', ']', '{', '}', ',' , '#', '(', ')','='] or character in [letter for letter in string.ascii_letters]: #checks for any bad characters (ie characters that could kill my computer)
                isAllowed = False
                break
            else:
                isAllowed = True
                answer = eval(str(''.join(args).replace("^", "**")))

    if isAllowed:
        await msg.channel.send('```' + str(answer) + '```')
    else:
        await msg.channel.send('`You sent a bad character! Please try again, and make sure you use only numbers and operators (+, -, /, *, **)`')

async def githubCommand(msg):
    await msg.channel.send("jeuseBot's code can be found at: https://github.com/Meme25327/jeuseBot")

async def ftocCommand(msg):
    fahrenheit = float(args[0])
    celsius = str(round(float((fahrenheit - 32) * 5/9), 2))
    embed = discord.Embed(title = "Fahrenheit to Celsius Conversion")
    embed.add_field(name='Fahrenheit', value=fahrenheit, inline=True)
    embed.add_field(name='Celsius', value=celsius, inline=True)

    await msg.channel.send(embed=embed)

async def ctofCommand(msg):
    celsius = float(args[0])
    fahrenheit = str(round(float((celsius * 9/5) + 32)))
    embed = discord.Embed(title = "Celsius to Fahrenheit Conversion")
    embed.add_field(name='Celsius', value=celsius, inline=True)
    embed.add_field(name='Fahrenheit', value=fahrenheit, inline=True)

    await msg.channel.send(embed=embed)

async def command1984(msg): #shoutout laura
    if msg.reference:
        repliedMsg = await msg.channel.fetch_message(msg.reference.message_id)
        content = repliedMsg.content
        url = content.replace(' ', '_')
        await msg.channel.send('https://api.memegen.link/images/custom/'+ url + '.png?background=https://i.kym-cdn.com/photos/images/newsfeed/002/223/795/e7c.jpg')
    else:
        url = '_'.join(args)
        await msg.channel.send('https://api.memegen.link/images/custom/' + url + '.png?background=https://i.kym-cdn.com/photos/images/newsfeed/002/223/795/e7c.jpg')

async def truthCommand(msg):
    with open('media/truths.txt', 'r', encoding='utf-8') as truths:
        truthsList = truths.readlines()
        rng = random.randint(0, 84)
        truth = truthsList[rng]
        await msg.channel.send(truth)

async def dareCommand(msg):
    with open('media/dares.txt', 'r', encoding='utf-8') as dares:
        daresList = dares.readlines()
        rng = random.randint(0, 41)
        dare = daresList[rng]
        await msg.channel.send(dare)

async def imdbCommand(msg):
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

async def defineCommand(msg):
    word = args[0]
    headers = {
    'User-Agent': 'jeuseBot',
    'From': 'Discord: Meme25327#4475'
    }
    try:
        result = requests.get('https://api.dictionaryapi.dev/api/v2/entries/en/' + word, headers = headers)
        resultJson = result.json()
        num = 0
        mainDefinition = resultJson[0]['meanings'][0]['definitions'][0]['definition']
        embed = discord.Embed(title = "Definition for " + word)
        embed.add_field(name = "Top Result:", value = mainDefinition, inline = False)
        wordDefList = []
    
        for definitionNo in resultJson[0]['meanings'][0]['definitions']:
            if num != 0:
                wordDef = "- " + resultJson[0]['meanings'][0]['definitions'][num]['definition']
                wordDefList.append(wordDef)
            num += 1
        
        embed.add_field(name = "Also see:", value = '\n'.join(wordDefList), inline = False)
                
        await msg.channel.send(embed = embed)
    except:
        await msg.channel.send("Word not found.")

async def jerryCommand(msg): #shoutout jerry
    await msg.channel.send("Husband. Entrepreneur. Lover. Top 0.7% of OnlyFans creators.")

async def weatherCommand(msg):
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
    embed.set_footer(text = "Use fahrenheit? Convert celsius to fahrenheit using the =ctof [celsius] command!")
    #-----------------end embed-------------------
    await msg.channel.send(embed = embed)

async def jesseCommand(msg):
    await msg.channel.send(file=discord.File('media\jesse.png'))

async def sexCommand(msg): #shoutout puresh
    await msg.channel.send(file=discord.File('media\sex.gif'))

async def sex2014Command(msg):
    await msg.channel.send(file=discord.File('media\sex2014.gif'))

async def wikipediaCommand(msg):
    wiki_wiki = wikipediaapi.Wikipedia('en')
            
    splitReq = args
    formattedReq = []
    
    for word in splitReq:
        formattedReq.append(word.capitalize())
        page_py = wiki_wiki.page('_'.join(formattedReq))
    
    summary = []
    splitSum = page_py.summary.split('. ')
    i = 0
    try:
        while len('. '.join(summary)) < 500:
            summary.append(splitSum[i])
            i += 1
        summary.append('')
    except IndexError:
        pass
    try:
        url = requests.get("http://en.wikipedia.org/w/api.php?action=query&titles="+' '.join(formattedReq)+"&prop=pageimages&format=json&pithumbsize=500")
        urlJson = url.json()
        pageID = urlJson['query']['pages'].keys()
        thumbnailURL = urlJson['query']['pages'][list(pageID)[0]]['thumbnail']['source']
    except KeyError:
        thumbnailURL = "media/imageNotFound.png"
    if summary == ['']: #prevents "cant find" message AND jeuse ping
        await msg.channel.send("Couldn't find that on wikipedia. You could try a google search (`=g`).")
        return 
    try:
        embed = discord.Embed(title = "Wikipedia Article for " + ' '.join(args), color = 0xFF5733)
        #embed.set_thumbnail(url = "attachment://") <------------ TODO: FIX
        embed.add_field(name = 'Summary', value = '. '.join(summary), inline = True)
        embed.add_field(name = 'Link', value = page_py.canonicalurl, inline = False)
    except:
        pass
    await msg.channel.send(embed=embed)

async def approvalCommand(msg):
    if msg.channel.id == 992071503392817174: #approval channel should end with 7174 when running   
        fetch = await msg.channel.history(limit=100).flatten()
        confessions = []
        i = 0
        for fetched in fetch:
            if fetched.author.id == 719764139702091836:
                if fetched.content != '':
                    confessions.append(fetched.content)
        numToApprove = 1
        for a in args:
            if a.isdigit():
                numToApprove = int(a)
        approved = confessions[0:numToApprove]
        revApproved = approved[::-1]
        spoiled = False
        nsfw = False
        if "spoil" in args and "nsfw" in args:
            nsfw = True
            spoiled = True
        elif "nsfw" in args and "spoil" not in args:
            nsfw = True
            spoiled = False
        elif "spoil" in args and "nsfw" not in args:
            nsfw = False
            spoiled = True
        for confession in revApproved:
            confessionChannel = client.get_channel(772794910826430494)
            nsfwChannel = client.get_channel(999349781879070730)
            if spoiled and nsfw:
                spoiledConfession = "|| " + confession + " || (spoiler tags typically indicate sensitive content)"
                await nsfwChannel.send(spoiledConfession)
            elif nsfw and not spoiled:
                await nsfwChannel.send(confession)
            elif not nsfw and spoiled:
                spoiledConfession = "|| " + confession + " || (spoiler tags typically indicate sensitive content)"
                await confessionChannel.send(spoiledConfession)
            else:
                await confessionChannel.send(confession)

async def pokedexCommand(msg):
    url = requests.get("https://pokeapi.co/api/v2/pokemon/" + args[0])
    try:
        urlJson = url.json()
    except:
        await msg.channel.send("Pokemon not found!")
        return
    pokemonSprite = urlJson["sprites"]["front_default"]
    pokemonName = urlJson["species"]["name"].capitalize()
    pokemonTypeOne = urlJson["types"][0]["type"]["name"].capitalize()
    try:
        pokemonTypeTwo = urlJson["types"][1]["type"]["name"].capitalize()
    except:
        pokemonTypeTwo = ""
    pokemonID = urlJson["id"]
    newUrl = requests.get("https://pokeapi.co/api/v2/pokemon-species/" + args[0])
    try:
        newUrlJson = newUrl.json()
    except:
        await msg.channel.send("Pokemon not found")
    pokemonFlavorText = newUrlJson["flavor_text_entries"][0]["flavor_text"]
    evolutionChain = requests.get(newUrlJson["evolution_chain"]["url"]).json()
    try:
        pokemonFirstStage = evolutionChain["chain"]["species"]["name"].capitalize()
    except:
        pokemonFirstStage = "-"
    try:
        pokemonSecondStage = evolutionChain["chain"]["evolves_to"][0]["species"]["name"].capitalize()
    except:
        pokemonSecondStage = "-"
    try:
        pokemonThirdStage = evolutionChain["chain"]["evolves_to"][0]["evolves_to"][0]["species"]["name"].capitalize()
    except:
        pokemonThirdStage = "-"
    pokemonNatDexNo = newUrlJson["pokedex_numbers"][0]["entry_number"]
    pokemonRegDexNo = newUrlJson["pokedex_numbers"][1]["entry_number"]
    pokemonHomeRegion = newUrlJson["pokedex_numbers"][1]["pokedex"]["name"].capitalize()

    bulbUrl = "https://bulbapedia.bulbagarden.net/wiki/" + pokemonName + "_(Pok%C3%A9mon)"

    types = pokemonTypeOne
    if pokemonTypeTwo != "":
        types += "/" + pokemonTypeTwo
        
    embed = discord.Embed()
    embed.set_thumbnail(url = pokemonSprite)
    embed.description = "[Bulbapedia](%s)"%bulbUrl
    embed.add_field(name="Name", value=pokemonName)
    embed.add_field(name="Type", value=types)
    embed.add_field(name="Home Region", value=pokemonHomeRegion, inline = False)
    embed.add_field(name="National Dex Number", value=pokemonNatDexNo)
    embed.add_field(name = "Regional Dex Number", value=pokemonRegDexNo)
    embed.add_field(name = "Description", value = pokemonFlavorText.replace("\n", " "), inline = False)
    embed.add_field(name = "Evolution Stage 1", value = pokemonFirstStage)
    embed.add_field(name = "Evolution Stage 2", value = pokemonSecondStage)
    embed.add_field(name = "Evolution Stage 3", value = pokemonThirdStage)
    await msg.channel.send(embed=embed)

async def joinCommand(msg):
    if msg.author.voice:
        global voiceChannel
        voiceChannel = msg.author.voice.channel  
        await voiceChannel.connect()
        await msg.channel.send("Succesfully joined the voice channel!")
    else:
        await msg.channel.send("You need to be in a voice channel.")

async def playCommand(msg):
    if msg.author.voice:
        global voiceChannel
        voiceChannel = msg.author.voice.channel  
        await voiceChannel.connect()
        print(type(voiceChannel))
        voiceChannel.play(discord.FFmpegPCMAudio('https://www.youtube.com/watch?v=Yk1HipdhdCU'), after=lambda e: print('done', e))
    else:
        await msg.channel.send("You need to be in a voice channel.")
        
async def svNameCommand(msg):
    try:
        os.rename('stop.txt', 'serverNames.txt')
    except:
        pass
    try:
        test = open('serverNames.txt')
        test.close()
    except:
        pass
    while True:
        if msg.author.id == 258582004738555904:
            with open('serverNames.txt') as file:
                potentialNames = file.readlines()
                pickedName = potentialNames[random.randint(0, len(potentialNames)-1)]
                nameAndID = pickedName.split(' ')
                #print(nameAndID[1])
                user = await client.fetch_user(379051592122499084)
                await msg.guild.edit(name=nameAndID[0])
                announceChan = client.get_channel(1000098358494515332)
                #await announceChan.send("Server name changed to: %s"%(pickedName))
                await asyncio.sleep(3600)
        pass
    else:
        await msg.channel.send("`Command not recognized! Try =help.`")

async def stopSvNameCommand(msg):
    if msg.author.id == 258582004738555904:
        os.rename('serverNames.txt', 'stop.txt')
    else:
        await msg.channel.send("`Command not recognized! Try =help.`")

async def testCommand(msg):
    while True:
        if msg.author.id == 258582004738555904:
            with open('serverNames.txt') as file:
                potentialNames = file.readlines()
                pickedName = potentialNames[random.randint(0, len(potentialNames)-1)]
                await msg.guild.edit(name=pickedName)
                announceChan = client.get_channel(1005539334541287525)
                await announceChan.send("Server name changed to: %s"%(pickedName))
                await asyncio.sleep(3600)
        pass
    else:
        await msg.channel.send("`Command not recognized! Try =help.`")

client.run(TOKEN)
