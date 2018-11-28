"""
Last Revised by Nhat Nguyen: 24.27.2018 
"""

# Relative imports
if __name__ == "__main__":
    from DatabaseReader import DatabaseReader
else:
    from modules.DatabaseReader import DatabaseReader

class ExerciseReader(DatabaseReader):

    def __init__(self):
        """
        Constructor.
        """
        self.exercise_column = self.getExerciseDatabase()[0]
        self.calorie_column = self.getExerciseDatabase()[1]

    def getExerciseDatabase(self):
        """
        Returns the entire exercise database.
        """
        exercise_database_columns = ("Exercise Name", "Calories per minute")
        return self.getDatabase(self.getExerciseDatabasePath(), exercise_database_columns)

    def getExerciseDatabasePath(self):
        """
        Returns the path of the exercise database depending on whether or not this
        file is being run on reader.py or app.py. 
        """
        if __name__ == "__main__":
            database_path = "../../database/exercise_database.xlsx"
        else:
            database_path = "../database/exercise_database.xlsx"
            
        return database_path


if __name__ == "__main__":
    exercise_obj = ExerciseReader()

    for exercise_name in exercise_obj.exercise_column:
      print(exercise_name)