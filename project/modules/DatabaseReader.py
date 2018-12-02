#!/usr/bin/python3
"""
CalPal: A calorie tracking app.
Written by Nhat Nguyen and Albert Ong.
CMPE 131
Revision: 30.11.2018

DatabaseReader.py
"""

import pandas as pd


def getDatabase(database_path, columns):
  """
  Returns a database given the path to the database file and a list
  of the names of the columns
  """
  # Create a Pandas dataframe from the excel file
  df = pd.read_excel(database_path, sheet_name="Sheet1")
  
  # A list that will store all the values in the database.
  # This will be the final output. 
  database = []
  
  # Uses a for loop to iterate each column of the database. 
  for column_name in columns:
    
    # Retrieves the database column. 
    database_column = convert(df[column_name])
    
    # Appends the column to the final output. 
    database.append(database_column)
  
  # Returns the final output. 
  return database


def convert(df_column):
  """
  Converts a DataFrame column to list
  """
  data_list = []
  
  for element in df_column:
    data_list.append(element)
      
  return data_list
