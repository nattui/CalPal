#!/usr/bin/python3
"""
CalPal: A calorie tracking app.
Written by Nhat Nguyen and Albert Ong.
CMPE 131
Revision: 17.11.2018

module.py
A Python module for extraneous functions. 
"""

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



