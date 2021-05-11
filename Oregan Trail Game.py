'''
World History
Oregano Trail
'''
from random import randint
def inventory():
  pass
def trade(thing, count, dict1):
  newValue = dict1[thing] - 1
  if newValue > 0:
    dict1[thing] = dict1[thing] - 1
    return True
  else:
    return False
def weightOfThings(dict1):
    n = 0
    for i in dict1:
        i = i + n
    return n
def totalValue(dict1, dict2):
    keys = list(dict1.keys())
    valueList = []
    for i in keys:
        valueList.append(dict1[i]*dict2[i])
    return sum(valueList)
def main():
  yourInventory = {}
  itemEntry = []
  valueMatrix = {}
  for i in range(5):
    item = 'item' + str(i + 1)
    itemEntry.append(item)
  for i in itemEntry:
    yourInventory[i] = randint(1, 10)
    valueMatrix[i] = randint(1, 10)
  print(yourInventory)
  print(valueMatrix)
  print(totalValue(yourInventory, valueMatrix))

if __name__ == '__main__':
  main()