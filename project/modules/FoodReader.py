#!/usr/bin/python3
"""
CalPal: A calorie tracking app.
Written by Nhat Nguyen and Albert Ong.
CMPE 131
Revision: 30.11.2018

FoodReader.py
Reads data from food_database.xlsx
"""

# Imports from DatabaseReader depending on whether or not the function 
# is being run from FoodReader.py or app.py
if __name__ == "__main__":
    from DatabaseReader import getDatabase
else:
    from modules.DatabaseReader import getDatabase


def getFoodDatabase():
  """
  Returns the entire food database.
  """
  food_database_columns = ("Category", "Food name", "Calories per oz")
  return getDatabase(getFoodDatabasePath(), food_database_columns)


def getFoodDatabasePath():
  """
  Returns the path of the food database depending on whether or not \
  this file is being run on reader.py or app.py. 
  """
  if __name__ == "__main__":
      database_path = "../../database/food_database.xlsx"
  else:
      database_path = "../database/food_database.xlsx"
      
  return database_path


def getFoodCalories(food, ounces):
  """
  Calclates the number of calories gained given a food name and 
  the number of ounces consumed. 
  """
  
  # Retrieves the food and calories per ounce columns from 
  # food_database.xlsx 
  food_column = getFoodDatabase()[1]
  calorie_column = getFoodDatabase()[2]
  
  # Retrieves the index associated with the given food name.
  food_index = food_column.index(food)
  
  # Retrieves the number of calories per ounce for the given food name.
  calories_per_ounce = calorie_column[food_index]
  
  # Calculated the number of calories gained, which is the
  # # of ounces consumed * # of calories per ounce
  calories_gained = ounces * calories_per_ounce
  
  # Returns the # of calories gained. 
  return calories_gained


#=======================================================================


if __name__ == "__main__":
    print(getFoodCalories("Bagel", 12.5))
