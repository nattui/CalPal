#!/usr/bin/python3
"""
CalPal: A calorie tracking app.
Written by Nhat Nguyen and Albert Ong.
CMPE 131
Revision: 01.12.2018

ExerciseReader.py
Reads data from exercise_database.xlsx
"""

# Imports from DatabaseReader depending on whether or not the function 
# is being run from ExerciseReader.py or app.py
if __name__ == "__main__":
    from DatabaseReader import getDatabase
else:
    from modules.DatabaseReader import getDatabase


def getExerciseDatabase():
  """
  Returns the entire exercise database.
  """
  exercise_database_columns = ("Exercise Name", "Calories per minute")
  return getDatabase(getExerciseDatabasePath(), exercise_database_columns)


def getExerciseDatabasePath():
  """
  Returns the path of the exercise database depending on whether or not this
  file is being run on reader.py or app.py. 
  """
  if __name__ == "__main__":
    database_path = "../../database/exercise_database.xlsx"
  else:
    database_path = "../database/exercise_database.xlsx"
      
  return database_path


def getExerciseCalories(exercise_name, minutes, weight):
  """
  Calculates the number of calories burned given an exercise name, 
  the number of minutes exercising, and the user's weight.
  """
  # Retrieves the exercise and calories per minute columns from
  # exercise_databast.xlsx
  exercise_column = getExerciseDatabase()[0]
  calorie_column = getExerciseDatabase()[1]
  
  # Retrieves the index associated with the exercise name.
  exercise_index = exercise_column.index(exercise_name)
  
  # Retrieves the calories per minute of the given exercise. 
  calories_per_minute = calorie_column[exercise_index]
  
  # Calculates the number of calories burned, which is the 
  # # of minutes exercising * # of calories per minute * the user's weight
  calories_burned = minutes * calories_per_minute * weight
  
  # Returns the number of calories burned. 
  return calories_burned
  

#=======================================================================


if __name__ == "__main__":
  pass
