# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 09:42:09 2024

@author: sophi
"""


### 0.Import functions and libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import openpyxl
#import Python System Dynamics library to run Vensim
import pysd
import time

workbook = openpyxl.load_workbook("data_initial.xlsx")
workbook.save("data.xlsx")
start_time = time.time()
qecolAlar_value = 2
workbook = openpyxl.load_workbook("data.xlsx")
sheet = workbook["Demandas"]
column_name = "QecolAlar"
#change only until the max row of the column QecoAlar
# First, find the index of column "QecolAlar
column_index = None
for col in sheet[2]:  # Check header row 2
    if col.value == column_name:
        column_index = col.column  
        break
  #find max index
# Technic : find the last row not empty of the column
last_row = 2  
for row in range(3, sheet.max_row+1): 
    if sheet.cell(row=row, column=column_index).value is not None:
        last_row = row  
# change the values of column QecoAlar with the value wanted and save it into data.xlsx to keep data_initial intact
# Update values in the column
for row in range(3, last_row + 1):
    sheet.cell(row=row, column=column_index).value = qecolAlar_value
workbook.save("data.xlsx")
end_time = time.time()    
execution_time = end_time - start_time
print(f"Execution time: {execution_time:.4f} seconds")


