
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import datetime

from cgySCRAPE import * # Now 
from cleaner import * # This is our cleansing functions


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
        self.today_date = str(myDate)

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
        

    def getSeason(self):
        return self.season

    def setSeason(self, season):
        self.season = season

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
        
        # This line above is how we get all nonempty strings here
        if message.content.startswith("!update"): # ONE, this seems to work too
            if len(my_arr) == 2:
                if checkSeason(my_arr[1]):
                    temp = update(my_arr[1])
                    return await message.channel.send(temp)
                    
                else:
                    return await message.channel.send("Invalid season try \"2023-2024\"")

        
            else:
                return await message.channel.send("ERROR !update SEASON")

            
        elif message.content.startswith("!setDay"): # TWO, we think this one works
            if len (my_arr) == 4 or len(my_arr) == 2:
                if len(my_arr) == 2 and my_arr[1] == "today":
                    my_day.setTimeTODAY()
                    return await message.channel.send("Date set to today")
                elif len(my_arr) == 2:
                    return await message.channel.send("ERROR \"today\" is how we set today")
                
                if len(my_arr) == 4:
                    if not checkYear(my_arr[1]):
                        return await message.channel.send(f"Year {my_arr[1]} incorrect")
                    elif not checkMonth(my_arr[2]):
                        return await message.channel.send(f"Month {my_arr[2]} incorrect")
                    elif not checkDay(my_arr[3]):
                        return await message.channel.send(f"Day {my_arr[3]} incorrect")
                    
                    else:
                        my_day.setTime(f"{my_arr[1]}-{my_arr[2]}-{my_arr[3]}")
                        return await message.channel.send(f"Day set to {my_arr[1]}-{my_arr[2]}-{my_arr[3]}")
                    

                else:
                    return await message.channel.send("ERROR set as YEAR MONTH DAY") 

            else:
                return await message.channel.send("Incorrect args: today or year month day")


        elif message.content == "!getDay": # So we know that this one works
            temp = my_day.getTime()
            return  await message.channel.send(f"{temp}")

        elif message.content.startswith("!lastGames"): # THREE
            if len(my_arr) == 2:
                if checkNum(my_arr[1]):
                    res = last_games(my_season.getSeason(), my_day.getYear(), my_day.getMonth(), my_day.getDay(), int(my_arr[1]))
                    return await message.channel.send(res)
                else:
                    return await message.channel.send("Not an number!")
                
            else:
                return await message.channel.send("Incorrects args: enter integer between 1 and 82")
            
        elif message.content.startswith("!nextGames"): # FOUR
            if len(my_arr) == 2:
                if checkNum(my_arr[1]):
                    res = next_games(my_season.getSeason(), my_day.getYear(), my_day.getMonth(), my_day.getDay(), int(my_arr[1]))
                    return await message.channel.send(res)
                else:
                    return await message.channel.send("Not an number!")
                
            else:
                return await message.channel.send("Incorrects args: enter integer between 1 and 82")            
            
        elif message.content.startswith("!setSeason"): # FIVE, complete
            if len(my_arr) == 2:
                if checkSeason(my_arr[1]):
                    my_season.setSeason(my_arr[1])
                    return await message.channel.send(f"Season updated to {my_season.getSeason()}")
                    
                else:
                    return await message.channel.send("Incorrect SEASON, try \"2023-2024\"")
                    

                
            else:
                return await message.channel.send("Incorrect args, needs !setSeason SEASON")
            

        elif message.content == "!getSeason":
            return await message.channel.send(f"{my_season.getSeason()}")
        elif message.content.startswith("!help"): # SIX
            pass
        
        
        

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)

