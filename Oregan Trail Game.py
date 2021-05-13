'''
World History
Oregano Trail
'''
# Preprocessor Directives
from random import randint
from random import randrange
def newDay(statsDictionary, difficulty):
    debuff1 = difficulty * randint(0, 10)
    debuff2 = difficulty * randint(0, 10)
    debuff3 = difficulty * randint(0, 10)
    debuff4 = difficulty * randint(0, 10)
    statsDictionary['food'] = statsDictionary['food'] - debuff1
    statsDictionary['water'] = statsDictionary['water'] - debuff2
    statsDictionary['durability'] = statsDictionary['durability'] - debuff3
    statsDictionary['morale'] = statsDictionary['morale'] - debuff4
    print(statsDictionary)
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
  if desiredItem not in list(dict1.keys()) or desiredItem == 'Silver':
      return False                  # This needs to be done before the first mention of dict1[thing] to make sure there are no errors
  
  # Checks if the user can trade the amount s/he wants to, and then manipulates if so
  # isIntable() is used here to make sure that the user entered a number, if it is not intable, then the program will go into the else catch
  elif dict1['Silver'] - silverAmount >= 0 and isIntable(silverAmount):
    scalar = randrange(0, 10)
    if scalar > 5:
        dict1[desiredItem] = dict1[desiredItem] + 2*(silverAmount/value[desiredItem])
    else:
        dict1[desiredItem] = dict1[desiredItem] + 0.5*(silverAmount/value[desiredItem])
    dict1['Silver'] = dict1['Silver'] - silverAmount
    return True
  # In all other cases False is return, indicating bad input(see first if catch)
  else:
    return False

# Uses the trade() method iteratively with a list to make multiple trades in one
def fullTrade(items, dict2, valueDict):
    # Initializes list which will be returned
    returnValue = []
    for item in items:
        isSuccesful = trade(item[0], item[1], dict2, value=valueDict)                  # isSuccesful is the True/False value returned by trade
        returnValue.append(isSuccesful)                  # This value is then appended to a list, the list will be used for error catching later
    print('Your inventory after the trade is ' + str(dict2))
    return returnValue

# Uses the previous methods to execute a trade based on direct user input
def stringTradeGenerator(dict1, valueDict, statsDict):
    # lines 47-54 are used to get user input and reformat it
    tradeString = input('Enter your trade in the following format(desiredItem:silverAmount desiredItem2:silverAmount)\n If you want to buy food enter the format (food:replenishing amount) ')
    splitTrade = tradeString.split()
    counter = 1
    statPositions = []
    falliabilityChecker = None
    for possibleFault in splitTrade:
        counter = counter + 1
        while ':' not in possibleFault:
            tradeString = input(f'Please reenter trade request {counter}')
            splitTrade[counter - 1] = tradeString
    counter = 0
    for element in splitTrade:
        newString = element.replace(':', ' ').split()
        splitTrade[counter] = newString
        splitTrade[counter][1] = int(splitTrade[counter][1])
        counter = counter + 1
    allStats = tuple(statsDict.keys())
    counter = 0
    for trade in splitTrade:
      if trade[0] in allStats:
        statsDict[trade[0]] = statsDict[trade[0]] + trade[1]
        dict1['Silver'] = dict1['Silver'] - (trade[1]/10)
        statPositions.append(counter)
      counter = counter + 1
    for position in statPositions:
      del splitTrade[position - 1]
    
    falliabilityChecker = fullTrade(splitTrade, dict1,valueDict=valueDict)                  # Executes full trade based on user input

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
        falliabilityChecker = fullTrade(splitTrade, dict1, valueDict=valueDict)
        

def weightOfThings(dict1):
    n = 0
    for i in list(dict1.keys()):
        n = dict1[i] + n
    return n


def totalValue(dict1, dict2):
    keys = list(dict1.keys())
    valueList = []
    for i in keys:
        valueList.append(dict1[i]*dict2[i])
    return sum(valueList)

def stagePrinter(stage):
    if stage == 0:
        print('constantinople')
        print('{O|-|-|-|-|-|-}')
    elif stage == 1:
        print('baghdad')
        print('{-|O|-|-|-|-|-}')
    elif stage == 2:
        print('rey')
        print('{-|-|O|-|-|-|-}')
    elif stage == 3:
        print('merv')
        print('{-|-|-|O|-|-|-}')
    elif stage == 4:
        print('samarkand')
        print('{-|-|-|-|O|-|-}')
    elif stage == 5:
        print('dunhuang')
        print('{-|-|-|-|-|O|-}')
    elif stage == 6:
        print("xi'an")
        print('{-|-|-|-|-|-|O}')

def postCheck(stage, valueMatrix):
    counter = 0
    keyList = list(valueMatrix.keys())
    keyList.remove('Silver')
    while(counter < stage):
        for key in keyList:
            valueMatrix[key] = valueMatrix[key] * 0.9
        counter = counter + 1

def attack(inventory, statsDict):
    fendOffAbility = (statsDict['morale'] + statsDict['speed'])/800
    attackSuccess = (0.25-fendOffAbility) * (100 - randint(0, 100))
    inventory['Silver'] = attackSuccess * inventory['Silver']

def nextAction(inventory, value, stage, hasHit, statsDictionary, difficulty, chineseMarkets):
    if stage == 6:
      value.update(chineseMarkets)
    elif hasHit == True:
      chineseItems = list(chineseMarkets.keys())
      for item in chineseItems:
        value.pop(item)
    possibleActions = ('map', 'trade', 'proceed', 'price check', 'inventory')
    action = input('\nEnter your next action: ')
    while action not in possibleActions:
        action = input('\nInvalid input \nReenter your next action: ')
    if action == 'map':
        stagePrinter(stage)
    elif action == 'trade':
        stringTradeGenerator(inventory, value, statsDictionary)
        newDay(statsDictionary=statsDictionary, difficulty = difficulty)
    elif action == 'proceed':
        probabilityOfAttack = randint(0, 10)
        if probabilityOfAttack > 6:
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
        if hasHit == False:
            stage = stage + 1
        elif hasHit == True:
            stage = stage - 1
        newDay(statsDictionary=statsDictionary, difficulty=difficulty)
        stagePrinter(stage)
        postCheck(stage, value)
        print(value)
        if stage == 1:
          print("Welcome to Baghdad. ETC ETC")
        if stage == 2:
          print("Welcome to Rey. ETC ETC")
    elif action == 'price check':
        print(value)
    elif action == 'inventory':
      print(inventory)
    if stage == 6:
        return stage, True
    return stage, False

def main():
  stage = 0
  hasHappened = False

  print("The Oregano Trail: a Silk Road Simulator \nby Vidur Modgil and Daniel Chen \n")
  print("Info: The Silk Road was a trading network that connected the West with China. \nGoods such as textiles, porcelain, and silk traveled along the overland route. You are a trader about to attempt a journey to China. You have 200 silver to spend. You may purchase supplies for your upcoming journey in your starting city, in any of the numerous cities along the route, or in China. Keep in mind that location and luck affects prices and goods available. Be wary of your food, water, caravan morale, weight of goods, and equipment durability.\n")
  input('Press enter when you are ready to play: ')
  difficulty = float(input('\nEnter any difficulty (can be decimal), where 1 = Pax Mongolica, 100 = Sudden Death Syndrome: '))
  if stage == 0:
      print("\nYou are in Constantinople, a Western city at the start of the Silk Road. Here you should purchase items for your upcoming journey. Remember to acquire goods for trading, food, water, spare equipment, entertainment, and defensive items. You can do the following actions: map, price check, trade, inventory, and proceed. Map checks your location. Price check displays prices in the following format: 'Good': Cost in silver. Trade allows you to buy and sell; trades should be input in format [TBD]. Inventory displays what goods you own, and proceed lets you leave the city and proceed to the next one.")
  
  yourInventory = {
      'Silver': 200, 
      'Silk': 0, 
      'Honey': 0,
      'Ivory': 0,
      'Textiles': 0,
      'Gold': 0,
      'Paper': 0,
      'Tea': 0,
      'Gunpowder': 0,
      'Porcelain': 0
      }

  valueMatrix = {
      'Silver': 1,
      'Silk': 20,
      'Honey': 10,
      'Ivory': 20,
      'Textiles': 10,
      'Gold': 30,
  }
  valueChecker = {
    'Silver': 1,
    'Silk': 20,
    'Honey': 10,
    'Ivory': 20,
    'Textiles': 10,
    'Gold': 30,
    'Tea': 10,
    'Gunpowder': 20,
    'Porcelain': 20,
  }
  chineseMarket = {
    'Tea': 5,
    'Gunpowder': 5,
    'Porcelain': 10,
  }
  stats = {
      'food': 100,
      'water': 100,
      'morale': 100,
      'durability': 100
  }

  while (stage <= 6):
      stage, hasHappened = nextAction(yourInventory, valueMatrix, stage, hasHappened, stats, difficulty, chineseMarket)
  while (stage >= 0):
      stage, hasHappened = nextAction(yourInventory, valueMatrix, stage, hasHappened, stats, difficulty = difficulty, chineseMarkets= chineseMarket)

if( __name__ == '__main__'):
  main()
