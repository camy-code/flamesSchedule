import requests
import os
from dotenv import load_dotenv
import json

from pathlib import Path
# load_dotenv()
# KEY = os.getenv('NHLKEY')
# year = "2023"
# print(KEY)
# url = f"https://api.sportradar.com/nhl/trial/v7/en/games/{year}/REG/schedule.json?api_key={KEY}"

# headers = {"accept": "application/json"}

# response = requests.get(url, headers=headers)
# data =(response.text)
# print("The response code is ",response.status_code)

#schedule = json.loads(data)

# Extract games involving Calgary Flames
#calgary_flames_games = [game for game in schedule['games'] if game['home']['name'] == 'Calgary Flames' or game['away']['name'] == 'Calgary Flames']

# Print the games involving Calgary Flames
# for game in calgary_flames_games:
#     print(json.dumps(game, indent=2))
    # print(game["away"]["name"])

    # This is good!

# Takes year as a string and will update a text file
 # or create a new file
# a text file with the year 
def update(season):
   
    # Check if the file exists
    my_test_file = Path(f"games/schedule{season}.txt")

    # This is creating a file in the case that it does not exist
    if (not my_test_file.is_file()):
        f = open(f"games/schedule{season}.txt", "x")
        f.close()

    start_year = str(season).split("-")[0]

    # So now we need to now make our call! 
    load_dotenv()
    KEY = os.getenv('NHLKEY')   
    url = f"https://api.sportradar.com/nhl/trial/v7/en/games/{start_year}/REG/schedule.json?api_key={KEY}"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)
    data =(response.text)
    print("The response code is ",response.status_code)

    if (response.status_code != 200):
        print("Error with the API")
        return "Error with the API"

    # This means that we are good to write to the file
    f = open(f"games/schedule{season}.txt", "w")
    f.write(data)
    f.close()
    return "The data has been UPDATED!"
    

# Takes a date and returns the last games played for the flames as of that date
# Includes the date in the count! 
# Cap num to something?
# Sometimes the API makes a mistake
def last_games(year,month, day, num):
    my_test_file = Path(f"games/schedule{year}.txt")

    # This is creating a file in the case that it does not exist
    if (not my_test_file.is_file()):
        return "Year is INVALID"
    
    # Now we can open
    f = open(f"games/schedule{year}.txt", "r")
    data = f.read()
    if data == "":
        print("error")
        return "Not in DB"

    f.close()
    schedule = json.loads(data)
    calgary_flames_games = [game for game in schedule['games'] if game['home']['name'] == 'Calgary Flames' or game['away']['name'] == 'Calgary Flames']
    # We now have an array of flames game dictionaries
    

    # print(calgary_flames_games[0]["scheduled"][:4]) # Year
    # print(calgary_flames_games[0]["scheduled"][5:7]) # Month
    # print(calgary_flames_games[0]["scheduled"][8:10]) # day
    # Remove all games that occur after this date 
    
    # You can make this cleaner but do later
    closed_games = [game for game in calgary_flames_games if game["status"]=="closed"]
    # before_year = [game for game in closed_games if (int(game["scheduled"][:4]) <= int(year))]
    before_month = [game for game in closed_games if (int(game["scheduled"][5:7]) <= int(month))]
    before_day = [game for game in before_month if (int(game["scheduled"][8:10]) <= int(day))]
    
    
    
    
    res = ""
    if num > len(before_day):
        res += "Not enough games for year\n"

        for i in range(len(before_day)):
            temp = before_day[i]["scheduled"]
            res += f"{temp}\n"

    else:
        for i in range(num):
            temp = before_day[i]["scheduled"]
            res += f"{temp}\n"

    print(res)

# update("2023") # We are going to assume that update now works corrects
# update("2023")
# last_games("2023-2024", "02", "15",5)

update("2023-2024")

# Make a note that this API can make errors


