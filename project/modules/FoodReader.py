"""
Last Revised by Nhat Nguyen: 24.27.2018 
"""

# Relative imports
if __name__ == "__main__":
    from DatabaseReader import DatabaseReader
else:
    from modules.DatabaseReader import DatabaseReader

class FoodReader(DatabaseReader):

    def __init__(self):
        """
        Constructor.
        """
        self.category_column = self.getFoodDatabase()[0]
        self.food_column = self.getFoodDatabase()[1]
        self.calorie_column = self.getFoodDatabase()[2]

    def getFoodDatabase(self):
        """
        Returns the entire food database.
        """
        food_database_columns = ("Category", "Food name", "Calories per oz")
        return self.getDatabase(self.getFoodDatabasePath(), food_database_columns)

    def getFoodDatabasePath(self):
        """
        Returns the path of the food database depending on whether or not this
        file is being run on reader.py or app.py. 
        """
        if __name__ == "__main__":
            database_path = "../../database/food_database.xlsx"
        else:
            database_path = "../database/food_database.xlsx"
            
        return database_path

    def getCalories(self, food, ounces):
        ounces = int(ounces)
        try:
            food_index = self.food_column.index(food)
            calories = self.calorie_column[food_index]
            cal_per_oz = ounces * calories
            print(int(cal_per_oz))
            return (int(cal_per_oz))
        except:
            return -1


if __name__ == "__main__":
    food_obj = FoodReader()

    for food_name in food_obj.food_column:
      print(food_name)

    print()
    print(food_obj.food_column[0])

    num = food_obj.getCalories("Chapatis", 100)
    print(num)


    if (num < -1):
        print("is dig")
    else:
        print("not")