
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import datetime

from cgySCRAPE import * # Now 


# This is where we setup the token shit
from dotenv import load_dotenv
import os

load_dotenv() # So I Guess this just brings the players into the game?
TOKEN = os.getenv('TOKEN')


# We need to set a constant date here
class My_calender():
    def __init__(self):
        self.today_date = str(datetime.datetime.now())[:10]
        pass

    def getTime(self):
        return self.today_date

    def setTime(self, myDate):
        self.getTime = myDate

    def setTimeTODAY(self):
        self.today_date = str(datetime.datetime.now())[:10]

    def getDay(self):
        return self.today_date[8:10]
    def getMonth(self):
        return self.today_date[5:7]
    def getYear(self):
        return self.today_date[:4]

# This is how we are going to keep track of season
class My_season():
    def __init__(self):
        self.season = "2023-2024"
        pass

    def getSeason(self):
        return self.today_date

    def setSeason(self, season):
        self.getTime = season

# Now the following are our variable for the project
my_day = My_calender() # default is today
my_season = My_season() # default is 2023-2024 season
        # ^^ Flames most character building season ^^

# Maybe set a class to do all the functions and cleansing? 
# The code is not hard it is just how one wants to structure it.
# Useful link below 
# https://github.com/Rapptz/discord.py/tree/master/examples

"""The following is how our bot interacts with our code."""
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!') 
        

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        # So now we know the bot is not talking to itself! 

        # TODO: add a channel restriction but that doesnt seem to hard

        my_arr = [word for word in str(message.content).split(" ") if word !="" ] 
        res = ""
        # This line above is how we get all nonempty strings here
        if message.content.startswith("!update"): # ONE
            pass
        elif message.content.startswith("!setDay"): # TWO
            if len (my_arr) == 4 or len(my_arr) == 2:
                if len(my_arr) == 2 and my_arr[1] == "today":
                    my_day.setTimeTODAY()
                    return await message.channel.send("Date set to today")
                elif len(my_arr) == 2:
                    return await message.channel.send("\"today\" is how we set today")
                
                if len(my_arr) == 4:
                    pass 
                    # Now we need to check day and such but that will be fore later. 
                    # This is where we left off
                
            else:
                return await message.channel.send("Incorrect args: today or year month day")

            pass
        elif message.content.startswith("!lastGames"): # THREE
            pass
        elif message.content.startswith("!nextGames"): # FOUR
            pass
        elif message.content.startswith("!setSeason"): # FIVE
            pass
        elif message.content.startswith("!help"): # SIX
            pass
        
        print("What is this shit") 
        

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)

