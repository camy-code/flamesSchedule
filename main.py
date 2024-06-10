
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# This is where we setup the token shit
from dotenv import load_dotenv
import os

load_dotenv() # So I Guess this just brings the players into the game?
TOKEN = os.getenv('TOKEN')
print(TOKEN)



# A lot of this discord hierchy stuff is 
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        
        print(f'Message from {message.author}: {message.content}')

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)



# def main():
#     print("Hello world")


# if __name__ =="__main__":
#     main()