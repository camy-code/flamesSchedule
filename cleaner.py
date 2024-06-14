import re
# The following will act as a way to clean our data so we do not give our bot faulty arguements
"""Takes a string and returns true if it is a string of a 4 digit year
returns false otherwise. 
ie \"2003\" >> True """
def checkYear(year):
    if not (isinstance(year, str)):
        return False # if we do not have a string we leave

    is_valid_expression = bool(re.search("^[0-9][0-9][0-9][0-9]$",str(year))    )
    return is_valid_expression
    

"""Takes a string and returns true if we have a valid year format"""
def checkSeason(season):
    if not (isinstance(season, str)):
        return False # returns false if we dont have a proper string
    
    my_arr = str(season).split("-") # So this will give us the split array
    if  (len(my_arr)!=2):
        return False 
    
    if not (checkYear(my_arr[0]) and checkYear(my_arr[1])):
        return False
    
    return int(my_arr[0])+1 == int(my_arr[1])

    
"""Takes a string and returns true if it is in range:
1 <=num <=82, false otherwise"""
def checkNum(num):
    is_my_str = isinstance(num, str)
    if is_my_str: # Do we have a string
        if str(num).isdigit(): # is the string an int?
            return 1<= int(num) <=82 # Is it in the proper range?
        else:
            return False
    else:
        return False # This means that we are not dealing with a valid arguement!

def checkDay(day):
    if not (isinstance(day,str)):
        return False
    
    x = re.search("^[0-3][0-9]$",str(day))
    if not x:
        return False
    
    return int(day) <32

def checkMonth(month):
    if not (isinstance(month,str)):
        return False
    
    x = re.search("^[0-3][0-9]$",str(month))
    if not x:
        return False
    
    return int(month) <13

# I think everything works here but best to debug in the case 
# that it does not fully work as intended