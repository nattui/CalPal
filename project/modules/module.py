#!/usr/bin/python3
"""
CalPal: A calorie tracking app.
Written by Nhat Nguyen and Albert Ong.
CMPE 131
Revision: 20.11.2018

module.py
A Python module for extraneous functions and variables.
"""

from calendar import month_name


def monthNameToNumber(month_name):
  """
  Takes the name of a month and returns its corresponding number.
  """
  
  # A dictionary that converts a month name to its 
  # corresponding number. 
  month_name_to_number = \
    {"January"   : 1,
     "February"  : 2, 
     "March"     : 3,
     "April"     : 4, 
     "May"       : 5,
     "June"      : 6, 
     "July"      : 7,
     "August"    : 8, 
     "September" : 9,
     "October"   : 10, 
     "November"  : 11,  
     "December"  : 12, }
     
  return month_name_to_number[month_name]


def monthNumberToName(month_number):
  """
  Takes a number between 1 and 12, represented as a string, 
  and returns the corresponing month name. 
  """
  month_index = int(month_number)
  return month_name[month_index]
  

def mergeHeight(feet, inches):
  """
  Takes two integer values, feet and inches, and calculates
  the total height in inches.
  """
  return (feet * 12) + inches


def splitHeight(total_height):
  """
  Takes a single integer value, the total height in inches, and
  returns a tuple of integers representing the total height
  in terms of feet and inches. 
  
  Example: 
    splitHeight(68) = (5, 8)
  """
  feet   = total_height // 12
  inches = total_height % 12
  
  return (feet, inches)
  

#=======================================================================

if __name__ == "__main__":
  
  # The total height in inches. 
  total_height = 68
  print("total_height = ", total_height, "inches\n")
  
  # Splits the total height into feet and inches. 
  split_height = splitHeight(total_height)
  feet = split_height[0]
  inches = split_height[1]
  
  # Prints the total height represented in feet and inches. 
  print("splitHeight(total_height) = ", feet, "feet", inches, "inches")
  
  # Merges the feet and inches into inches.
  # This values will be the same as total_height. 
  merged_height = mergeHeight(feet, inches)
  print("mergeHeight(feet, inches) = ", merged_height, "inches")



