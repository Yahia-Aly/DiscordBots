import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from jokeapi import Jokes # Import the Jokes class
import requests
import json

#This bot has a collection of commands that can be used in a game/activity server
#It includes generating random jokes and activities!
#Note: You need a .env file with a valid developer discord token and guild

def print_joke(categ="None"):
    joke = Jokes()  # Initialise the class
    if(categ=="None"):
        joke= joke.get_joke()
    elif (categ=="Programming" or categ=="Misc" or categ=="Dark" or categ=="Pun"  or categ=="Spooky" or categ=="Christmas" ):
        joke= joke.get_joke(category=[categ])  # Retrieve a random joke
    else:
        print (categ)
        raise ValueError('joke category does not exist ')
    if joke["type"] == "single": # Print the joke
        print(joke["joke"])
        return joke["joke"]
    else:
        print(joke["setup"])
        print(joke["delivery"])
        return (joke["setup"] + "\n" + joke["delivery"])

def get_activity(price="0", participants ="1"):
    if(price=="0" and participants=="1"):
        response = requests.get("http://www.boredapi.com/api/activity/").json()
        activity = response["activity"]
        return activity
    elif ( (price <= "1") and  (price > "0") and participants=="1"):
        response = requests.get("http://www.boredapi.com/api/activity?price="+price).json()
        activity = response["activity"]
        return activity
    elif ( (participants > "1") and price=="0"):
        response = requests.get("http://www.boredapi.com/api/activity?participants="+participants).json()
        activity = response["activity"]
        return activity
    else:
        print (price)
        print (participants)
        raise ValueError('an error occured with API query')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix = '!')


@bot.event
async def on_ready():
    print("Bot is Online")

#test command 
@bot.command()
async def greet(msg):
    await msg.send('Hi there!')
    

#help command 
@bot.command()
async def helpme(msg):
    await msg.send('There are 3 commands you can use besides the help command')
    await msg.send('1) The !greet command, which will say hi :)')
    await msg.send('2) The !joke command, which will generate a random joke for you')
    await msg.send('You can leave it blank or add a joke category, which includes: Misc, Programming, Dark, Pun, Spooky, and Christmas')
    await msg.send('3) The !bored command, which will suggest a random activity for you')
    await msg.send('You can leave it blank or add a price index to the activity (from 0 to 1) by writing !bored price=0.5 for example')
    await msg.send('You can also specify number of participants by writing !bored particpants=5 for example')
    await msg.send('Sometimes errors could happen because of external 3rd party APIs being down or not having a response for the option you requested, sorry about that :(')


#joke command 
@bot.command()
async def joke(msg, *, joke_type="None"):
    try:
        joke=print_joke(joke_type)
        await msg.send(joke)
    except Exception as e:
        print(e)
        await msg.send('invalid command ' + ' check !helpme')

#bored command 
@bot.command()
async def bored(msg, *, sentence="None"):
    try:
        print(sentence)
        if (sentence=="None"):
            action=get_activity("0","1")
            await msg.send(action)
        else:
            phrase = str(sentence).split('=')
            print(phrase)
            option = phrase[0]
            number = phrase[1]
            if (option=="price"):
                action=get_activity(number,"1")
                await msg.send(action)
            elif (option=="participants"):
                action=get_activity("0",number)
                await msg.send(action)
            else:
                await msg.send('invalid option ' + ' check !helpme')  
    except Exception as e:
        print(e)
        await msg.send('invalid command ' + ' check !helpme')

bot.run(TOKEN)
