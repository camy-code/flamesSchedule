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
def game_format_future(my_dict): # This is the format for the last X games
    home_team = my_dict["home"]["alias"]
    away_team = my_dict["away"]["alias"]


    my_date = my_dict["scheduled"][:10]

    res = ""
    if my_dict["home"]["alias"] == "CGY":   # This means flames are home
        res = f"{away_team} at {home_team}:\t {my_date}"
    else:                                   # This means flames are away
        res = f"{away_team} at {home_team}\t {my_date}"
   

    return res # This is where 



def game_format(my_dict): # This is the format for the last X games
    home_team = my_dict["home"]["alias"]
    away_team = my_dict["away"]["alias"]

    home_score = my_dict["home_points"]
    away_score = my_dict["away_points"]

    my_date = my_dict["scheduled"][:10]

    res = ""
    if my_dict["home"]["alias"] == "CGY":   # This means flames are home
        if home_score > away_score:
            res = f"{away_team} at {home_team}:\tFLAMES WIN:\t{home_score}-{away_score} \t {my_date}"
        else:
            res = f"{away_team} at {home_team}:\tFLAMES LOSS:\t{home_score}-{away_score} \t {my_date}"
    else:                                   # This means flames are away
        if home_score > away_score:
            res = f"{away_team} at {home_team}:\tFLAMES LOSS:\t{away_score}-{home_score} \t {my_date}"
        else:
            res = f"{away_team} at {home_team}:\tFLAMES WIN:\t{away_score}-{home_score} \t {my_date}"

    return res # This is where 
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
def last_games(season,year,month, day, num):
    my_test_file = Path(f"games/schedule{season}.txt")
    # This is creating a file in the case that it does not exist
    if (not my_test_file.is_file()):
        return "Season is INVALID or not in DB"
    
    # Now we can open
    f = open(f"games/schedule{season}.txt", "r")
    data = f.read()
    if data == "":
        print("error")
        return "Not in DB"

    f.close()
    schedule = json.loads(data)
    calgary_flames_games = [game for game in schedule['games'] if game['home']['name'] == 'Calgary Flames' or game['away']['name'] == 'Calgary Flames']
    # We now have an array of flames game dictionaries
    
    closed_games = [game for game in calgary_flames_games if game["status"]=="closed"] # This is ensuring we ar getting only past games
    # print(calgary_flames_games[0]["scheduled"][:4]) # Year
    # print(calgary_flames_games[0]["scheduled"][5:7]) # Month
    # print(calgary_flames_games[0]["scheduled"][8:10]) # day
    # Remove all games that occur after this date 
    my_op_comp = f"{str(year)}{str(month)}{str(day)}"
    
    #before_day = [game for game in calgary_flames_games if (int(my_op_comp)  >= int(f"{game["scheduled"][:4]}{game["scheduled"][5:7]}{game["scheduled"][8:10]}"))]
    before_day = [
    game for game in closed_games
    if int(my_op_comp) >= int(f"{game['scheduled'][:4]}{game['scheduled'][5:7]}{game['scheduled'][8:10]}")
]
    before_day.reverse()

    res = ""
    if len(before_day) < num:
        res += "\t\tNot enough games\n"
        for i in before_day:
            res += f"{game_format(i)}\n"
    else:
        for i in range(num):
            res += f"{game_format(before_day[i])}\n"
    # Arguements need to be fixed here but this is a start
    return res


# Same args    
def next_games(season, year, month, day, num):
    my_test_file = Path(f"games/schedule{season}.txt")
    # This is creating a file in the case that it does not exist
    if (not my_test_file.is_file()):
        return "Season is INVALID or not in DB"
    
    # Now we can open
    f = open(f"games/schedule{season}.txt", "r")
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
    my_op_comp = f"{str(year)}{str(month)}{str(day)}"
    
    #before_day = [game for game in calgary_flames_games if (int(my_op_comp)  >= int(f"{game["scheduled"][:4]}{game["scheduled"][5:7]}{game["scheduled"][8:10]}"))]
    after_day = [
    game for game in calgary_flames_games
    if int(my_op_comp) <= int(f"{game['scheduled'][:4]}{game['scheduled'][5:7]}{game['scheduled'][8:10]}")
]
    if after_day == []:
        return f"No upcoming games for {season}"
    

    res = ""
    if len(after_day) < num:
        res += "\t\tNot enough games\n"
        for i in after_day:
            res += f"{game_format_future(i)}\n"
    else:
        for i in range(num):
            res += f"{game_format_future(after_day[i])}\n"
    # Arguements need to be fixed here but this is a start
    return res



#update("2023-2024")
#print(last_games("2023-2024", "2023", "11", "01",100))

print("upcoming games")
print(next_games("2023-2024", "2024", "04", "10",100))



# Make a note that this API can make errors


