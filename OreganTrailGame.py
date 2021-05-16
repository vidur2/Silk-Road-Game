'''
World History
Oregano Trail
'''
# Preprocessor Directives
from random import randint
import os
# Test
# Function that is used to apply debuffs to each stat each time 'trade' or 'proceed' action is taken
def newDay(statsDictionary, difficulty, weight, inventory):
    # Debuffs are randomly generated and multiplied by user-set difficulty
    debuff1 = difficulty/5 * randint(10, 20)
    debuff2 = difficulty/5 * randint(10, 20)
    debuff3 = difficulty/5 * randint(10, 20)
    debuff4 = difficulty/5 * randint(10, 20)
    # Debuffs are applied here
    statsDictionary['food'] = statsDictionary['food'] - debuff1
    statsDictionary['water'] = statsDictionary['water'] - debuff2
    statsDictionary['durability'] = statsDictionary['durability'] - debuff3
    statsDictionary['morale'] = statsDictionary['morale'] - debuff4
    print('Your current weight is ' + str(weightOfThings(inventory, weight)))
    # print(inventory)
    # print(weight)
    statsDictionary['speed'] = (20/3)*(statsDictionary['food'] + statsDictionary['water'] + statsDictionary['durability'])/weightOfThings(inventory, weight)
    # Each day the stats are printed back to the user
    print(statsDictionary)
    allStats = list(statsDictionary.keys())
    # Checks if any variable is less than or equal to 0
    for stat in allStats:
        if statsDictionary[stat] <= 0:
            return False
            print(False)
            break
    return True

# Uses try-except catch to determine whether a value can be casted into an integer
def isIntable(number):
    try:
        int(number)
        return True
    except:
        return False

# Basically executes a trade by subtracting values from the users inventory
def trade(desiredItem, silverAmount, dict1, value):
  # Makes sure that whatever the user is entering is an obtainable item in the game
  if desiredItem not in list(value.keys()) or desiredItem == 'silver':
      return False                  # This needs to be done before the first mention of dict1[thing] to make sure there are no errors
  
  # Checks if the user can trade the amount s/he wants to, and then manipulates if so
  # isIntable() is used here to make sure that the user entered a number, if it is not intable, then the program will go into the else catch
  elif dict1['silver'] - silverAmount >= 0 and isIntable(silverAmount):
    scalar = randint(0, 10)
    if scalar > 5:
        dict1[desiredItem] = dict1[desiredItem] + 2*(silverAmount/value[desiredItem])
    else:
        dict1[desiredItem] = dict1[desiredItem] + 0.5*(silverAmount/value[desiredItem])
    dict1['silver'] = dict1['silver'] - silverAmount
    return True
  # In all other cases False is return, indicating bad input(see first if catch)
  else:
    return False

def sell(sellingItem, amount, dict1, value):
    if sellingItem == 'silver' or sellingItem not in list(dict1.keys()):
        return False
    elif dict1[sellingItem] - amount >= 0:
        dict1[sellingItem] = dict1[sellingItem] - amount
        dict1['silver'] = dict1['silver'] + amount * value[sellingItem]/4
        return True
    else:
        return False

# Uses the trade() method iteratively with a list to make multiple trades in one
def fullTrade(items, dict2, valueDict, isSell):
    # Initializes list which will be returned
    returnValue = []
    isSuccesful = None
    for item in items:
        if isSell == False:
            isSuccesful = trade(item[0], item[1], dict2, value=valueDict)                  # isSuccesful is the True/False value returned by trade
        elif isSell == True:
            isSuccesful = sell(item[0], item[1], dict2, value=valueDict)
        returnValue.append(isSuccesful)                  # This value is then appended to a list, the list will be used for error catching later
    print('Your inventory after the trade is ' + str(dict2))
    return returnValue

def sellPossible(inventory):
    possibleItems = list(inventory.keys())
    possibleItems.remove('silver')
    itemValues = []
    for item in possibleItems:
        itemValues.append(inventory[item])
    if sum(itemValues) == 0:
        return False
    else:
        return True

# Uses the previous methods to execute a trade based on direct user input
def stringTradeGenerator(dict1, valueDict, statsDict):
    # lines 47-54 are used to get user input and reformat it
    buyOrSell = input('Would you like to buy using silver or sell an item for silver? Enter either "buy" or "sell": ')
    canSell = sellPossible(dict1)
    possibleBuySell = ('buy', 'sell')
    while buyOrSell not in possibleBuySell:
        buyOrSell = input('Please enter a valid input for buying or selling silver: ')
    while canSell == False and buyOrSell != 'buy':
        buyOrSell = input('Please enter a valid input, you cannot sell any items. Enter buy to continue: ')
    tradeString = input('Enter your trade in the following format(desiredItem:silverAmount desiredItem2:silverAmount)\n If you want to buy food enter the format (food:replenishing amount)\n If you are selling an item enter the format(itemBeingSold:AmountOfItemSold) ')
    splitTrade = tradeString.split()
    counter = 0
    statPositions = []
    falliabilityChecker = None
    for possibleFault in splitTrade:
        while ':' not in possibleFault:
            possibleFault = input(f'Please reenter trade request {counter + 1}: ')
            splitTrade[counter] = possibleFault
        counter = counter + 1
    counter = 0
    for element in splitTrade:
        newString = element.replace(':', ' ').split()
        splitTrade[counter] = newString
        splitTrade[counter][1] = int(splitTrade[counter][1])
        counter = counter + 1
    statsDict.pop('speed')
    allStats = tuple(statsDict.keys())
    counter = 0
    for trade in splitTrade:
      if trade[0] in allStats:
        statsDict[trade[0]] = statsDict[trade[0]] + trade[1]
        dict1['silver'] = dict1['silver'] - (trade[1]/10)
        statPositions.append(counter)
      counter = counter + 1
    counter = 0
    for position in statPositions:
      del splitTrade[position-counter]
      counter = counter + 1
    
    falliabilityChecker = None
    if buyOrSell == 'buy':
        falliabilityChecker = fullTrade(splitTrade, dict1, valueDict=valueDict, isSell=False)                  # Executes full trade based on user input
    elif buyOrSell == 'sell':
        falliabilityChecker = fullTrade(splitTrade, dict1, valueDict=valueDict, isSell=True)
    
      # The error catching from earlier is applied here
    while False in falliabilityChecker:
        manipulatableList = falliabilityChecker.copy()                  # Makes a copy of the list which is being used as a condition in the while loop
        errorPositions = []                  # Records the positions of where False is
        stringBuilder = 'Please reenter your '                  # Initializes new user input
        hasIterated = 0                  # Used later to determine singular/plural
          
        # Since the .index() function only finds the first variable with the name, we need to record the index, replace it with a diff value, and then repeat
        while False in manipulatableList:
            error = manipulatableList.index(False)
            errorPositions.append(error)
            manipulatableList[error] = 'Fixed'

        # Used to build the string which will be asking for user input later
        for error in errorPositions:
            truePosition = None
              
            if error + 1 == 1:
                truePosition = str(error + 1) + 'st'
            elif error + 1 == 2:
              truePosition = str(error + 1) + 'nd'
            elif error + 1 == 3:
                truePosition = str(error + 1) + 'rd'
            else:
                truePosition = str(error + 1) + 'th'
              
            # If/Else is used to determine initial value, and then all values after
            if hasIterated == 0:
                stringBuilder = stringBuilder + truePosition
            else:
                stringBuilder = stringBuilder + '/' + truePosition
            hasIterated = hasIterated + 1

          # If there are more than 1 element following 'Please reenter your', then trade is plural, otherwise, it is singular
        if hasIterated > 1:
            stringBuilder = stringBuilder + ' trades, there was an error processing your input: '
        else:
            stringBuilder = stringBuilder + ' trade, there was an error processing your input: '
          
          # Same function as before the error catch in the loop, just repeated until there are no errors in input
        tradeString = input(stringBuilder)
        splitTrade = tradeString.split()
        counter = 0
          
        for element in splitTrade:
            newString = element.replace(':', ' ').split()
            splitTrade[counter] = newString
            splitTrade[counter][1] = int(splitTrade[counter][1])
            counter = counter + 1
        if buyOrSell == 'buy':
            falliabilityChecker = fullTrade(splitTrade, dict1, valueDict=valueDict, isSell=False)
        elif buyOrSell == 'sell':
            falliabilityChecker = fullTrade(splitTrade, dict1, valueDict=valueDict, isSell=True)
        

def weightOfThings(inventory, weightDict):
    finalWeight = 0
    counter = 0
    for i in list(inventory.keys()):
        finalWeight = (inventory[i]*weightDict[i] + finalWeight)
        counter = counter + 1
    return finalWeight


def totalValue(dict1, dict2):
    keys = list(dict1.keys())
    valueList = []
    for i in keys:
        valueList.append(dict1[i]*dict2[i])
    return sum(valueList)

def stagePrinter(stage):
    if stage == 0:
        print('\nYou are in Constantinople')
        print('{O|-|-|-|-|-|-}')
    elif stage == 1:
        print('\nYou are in Baghdad')
        print('{-|O|-|-|-|-|-}')
    elif stage == 2:
        print('\nYou are in Rey')
        print('{-|-|O|-|-|-|-}')
    elif stage == 3:
        print('\nYou are in Merv')
        print('{-|-|-|O|-|-|-}')
    elif stage == 4:
        print('\nYou are in Samarkand')
        print('{-|-|-|-|O|-|-}')
    elif stage == 5:
        print('\nYou are in Dunhuang')
        print('{-|-|-|-|-|O|-}')
    elif stage == 6:
        print("\nYou are in Xi'an")
        print('{-|-|-|-|-|-|O}')

def postCheck(stage, valueMatrix):
    counter = 0
    keyList = list(valueMatrix.keys())
    keyList.remove('silver')
    while(counter < stage):
        for key in keyList:
            valueMatrix[key] = valueMatrix[key] * 0.9
        counter = counter + 1

def attack(inventory, statsDict):
    fendOffAbility = (statsDict['morale'] + statsDict['durability'])/800
    attackSuccess = 0.25-fendOffAbility
    inventory['silver'] = inventory['silver'] - (attackSuccess * inventory['silver'])

def nextAction(inventory, value, stage, hasHit, statsDictionary, difficulty, chineseMarkets, weekCounter, weight):
    isAlive = True
    speed = statsDictionary['speed']
    if stage == 6:
      value.update(chineseMarkets)
    elif hasHit == True:
      chineseItems = list(chineseMarkets.keys())
      for item in chineseItems:
        value.pop(item)
    possibleActions = ('map', 'trade', 'proceed', 'price check', 'inventory', 'help commands', 'help info')
    action = input('\nEnter your next action: ')
    while action not in possibleActions:
        action = input('\nInvalid input \nReenter your next action: ')
    if action == 'map':
        print('\nMap:')
        stagePrinter(stage)
    elif action == 'trade':
        stringTradeGenerator(inventory, value, statsDictionary)
        isAlive = newDay(statsDictionary=statsDictionary, difficulty = difficulty, weight=weight, inventory=inventory)
        weekCounter = weekCounter + 1
    elif action == 'proceed':
        negativeEvent = randint(0, 10)
        if weekCounter < 3:
            print(f'You must stay at least {str(6/speed)} weeks at a city before traveling with your current speed\nYou have burned a turn')
        if negativeEvent >= 8:
            possibleAttackText = [
                'Enter Attack Texts', 
                'Formatted Like so', 
                'You can have different', 
                'one for each stage', 
                'placeholder text attack', 
                'placeholder text attack', 
                'placeholder text attack'
                ]
            attack(inventory=inventory, statsDict=statsDictionary)
            print(possibleAttackText[stage])
            currency = inventory['silver']
            print(f'You now have {str(currency)} silver left')
        
        if hasHit == False and weekCounter == 6/speed and negativeEvent < 5 or negativeEvent > 8:
            stage = stage + 1
            weekCounter = 0
        elif hasHit == True and weekCounter == 6/speed and negativeEvent < 5 or negativeEvent > 8:
            stage = stage - 1
            weekCounter = 0
        elif negativeEvent > 5 and negativeEvent <= 8:
            print('An extreme weather event has occoured, you must wait an extra week before traveling.')
            weekCounter = weekCounter + 1

        isAlive = newDay(statsDictionary=statsDictionary, difficulty=difficulty, weight=weight, inventory=inventory)
        print('Your Current Speed is ' + str(speed))
        stagePrinter(stage)
        postCheck(stage, value)
        print(value)

        if stage == 1:
          print("\n{-|O|-|-|-|-|-}\nYou are now entering Baghdad, the first major centre of trade of 6 you will encounter on your journey to Xi'an, China. With the large distance to China, Eastern goods are ratger expensive here, while Western goods and local specialties such as textiles are cheap here.")
        elif stage == 2:
          print("\n{-|-|O|-|-|-|-}\nYou are now entering Rey. ETC ETC")
        elif stage == 3:
          print("\n{-|-|-|O|-|-|-}\nYou are now entering Merv. ETC ETC")
        elif stage == 4:
          print("\n{-|-|-|-|O|-|-}\nYou are now entering Samarkand. ETC ETC")
        elif stage == 5:
          print("\n{-|-|-|-|-|O|-}\nYou are now entering Dunhuang. ETC ETC")
        elif stage == 6:
          print("\n{-|-|-|-|-|-|O}\nYou are now entering Xi'an. ETC ETC")
    
    elif action == 'price check':
        print('\nPrices:')
        print(value)
    elif action == 'inventory':
      print('\nInventory:')
      print(inventory)
    elif action == 'help commands':
        print("Map checks your location. \nPrice check displays prices in the following format: 'Good': Cost in silver. \nTrade allows you to buy and sell; trades should be input in format [TBD]. \nInventory displays what goods you own. \nProceed lets you leave the city and proceed to the next one.")
    elif action == 'help info':
        print("Supplies may be purchased at any of the 7 major cities (including Constantinople and Xi'an) along the route. \nLocation affects prices and goods available. \nBe wary of your food, water, caravan morale, weight of goods, and equipment durability, and your caravan speed. Speed is calculated off of factors like chance events, health of your caravan, good weight, and your caravan equipment condition. \nThe longer you spend between cities, the higher chance you have of being raided or encountering malignant conditions. \nDue to the high weight of silver, players are incentivized to take advantage of regional prices, trade, and carry goods rather than liquid assets, which can be lost easier in raids. \nTime is divided into units of half a month per turn, and the journey for an average trader should take around 2 years round trip. \nCities are spaced around a month and a half of travel apart from each other.")
    if stage == 6:
        return stage, True, isAlive
    return stage, False, isAlive

def scoreCalculator(inventory, value):
    allItems = list(inventory.keys())
    valueReturnable = 0
    for item in allItems:
        valueReturnable = inventory[item]*value[item] + valueReturnable
    return valueReturnable 

def main():
  stage = 0
  hasHappened = False
  weekCounter = 0
  isAlive = True
  replay = True
  print("The Oregano Trail: a Silk Road Simulator \nby Vidur Modgil and Daniel Chen \n")
  print('The Silk Road was a trading network that connected the West with China. \nGoods such as textiles, porcelain, and silk traveled along the overland route. You are a trader about to attempt a journey to China. You have 200 silver to spend. You may purchase supplies for your upcoming journey in your starting city, in any of the numerous cities along the route, or in China. Keep in mind that location affects prices and goods available. Be wary of your food, water, caravan morale, weight of goods, and equipment durability, and your caravan speed, which is based off of factors like chance events, health of your caravan, good weight, and your caravan equipment condition. The longer you spend between cities, the higher chance you have of being raided or encountering malignant conditions. Due to the high weight of silver, players are incentivized to take advantage of regional prices, trade, and carry goods rather than liquid assets, which can be lost easier in raids. Time is divided into units of half a month per "turn", and the journey for an average trader should take around 2 years round trip. Cities are spaced around a month and a half of travel apart from each other. \n')
  input('Press enter when you are ready to play: ')
  difficulty = float(input('\nEnter any difficulty (can be decimal), where <1 = "Dying is illegal", 5 = "Pax Mongolica", 10 = "Recommended", >100 = "Sudden Death Syndrome": '))
  if stage == 0:
      print("\nYou are in Constantinople, a Western city at the start of the Silk Road. Here you should purchase items for your upcoming journey. Remember to acquire goods for trading, food, water, spare equipment, entertainment, and defensive items. You can do the following actions: map, price check, trade, inventory, and proceed. Map checks your location. Price check displays prices in the following format: 'Good': Cost in silver. Trade allows you to buy and sell; trades should be input in format [TBD]. Inventory displays what goods you own, and proceed lets you leave the city and proceed to the next one.")
      print('You can access the list of commands and their explanations and a brief explanation of game principles by inputting "help commands" and "help info", respectively")')

  while(replay == True):
    stage = 0
    hasHappened = False
    weekCounter = 0
    winCondition = False
    yourInventory = {
      'silver': 200, 
      'silk': 0, 
      'honey': 0,
      'ivory': 0,
      'textiles': 0,
      'gold': 0,
      'paper': 0,
      'tea': 0,
      'gunpowder': 0,
      'porcelain': 0
      }

    valueMatrix = {
      'silver': 1,
      'silk': 20,
      'honey': 10,
      'ivory': 20,
      'textiles': 10,
      'gold': 30,
    }
    valueChecker = {
      'silver': 1,
      'silk': 20,
      'honey': 10,
      'ivory': 20,
      'textiles': 10,
      'gold': 30,
      'tea': 10,
      'gunpowder': 20,
      'porcelain': 20,
    }
    chineseMarket = {
      'tea': 5,
      'gunpowder': 5,
      'porcelain': 10,
    }
    stats = {
      'food': 100,
      'water': 100,
      'morale': 100,
      'durability': 100,
      'speed': 1
    }
    weights = {
      'silver': 10, 
      'silk': 1, 
      'honey': 0.5,
      'ivory': 5,
      'textiles': 0.5,
      'gold': 8,
      'paper': 1,
      'tea': 3,
      'gunpowder': 4,
      'porcelain': 4
    }
    while (stage <= 6):
        if isAlive == False:
            break
        stage, hasHappened, isAlive = nextAction(yourInventory, valueMatrix, stage, hasHappened, stats, difficulty, chineseMarket, weekCounter, weight=weights)
    while (stage >= 0):
        if isAlive == False:
            break
        stage, hasHappened, isAlive = nextAction(yourInventory, valueMatrix, stage, hasHappened, stats, difficulty = difficulty, chineseMarkets= chineseMarket, weekCounter=weekCounter, weight=weights)
    if stage == 0 and hasHappened == True:
        print(f'You have completed the silk road\n Your final score is {scoreCalculator(yourInventory, valueChecker)}')
        print('Thank you for playing Oregano Trail: A Silk Road Simulator')
        replay = False
    else:
        replayComparation = input('Press 1 to replay, 2 to quit: ')
        while replayComparation not in ('1', '2'):
            replayComparation = input('Please either enter 1 or 2 for replay or quitting respectively: ')
        if replayComparation == '1':
            replay = True
        elif replayComparation == '2':
            replay = False
            print('Thank you for playing Oregano Trail: A Silk Road Simulator')

if( __name__ == '__main__'):
  main()
