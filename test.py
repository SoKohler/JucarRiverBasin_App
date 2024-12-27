
### 0.Import functions and libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import openpyxl
#import Python System Dynamics library to run Vensim
import pysd
import time


start_time = time.time()
qecolAlar_value = 2
demandas =pd.read_excel("data.xlsx", sheet_name="Demandas",header=1)
column_name = "QecolAlar"
demandas[column_name]=qecolAlar_value
# Save the updated DataFrame back to the Excel file
with pd.ExcelWriter("data.xlsx", engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
    demandas.to_excel(writer, sheet_name="Demandas", index=False)
end_time = time.time()    
execution_time = end_time - start_time
print(f"Execution time: {execution_time:.4f} seconds")