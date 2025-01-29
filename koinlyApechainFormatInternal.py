import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog
import os

# Open file dialog for user to select a file
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(title="Select the ApeChain Transaction CSV File", filetypes=[("CSV files", "*.csv")])

if not file_path:
    print("No file selected. Exiting...")
    exit()

# Read the CSV file
try:
    df = pd.read_csv(file_path)
except Exception as e:
    print(f"Error reading the file: {e}")
    exit()

# Prepare the data
# Creating Koinly universal import format
koinly_format = pd.DataFrame()
koinly_format['Date'] = pd.to_datetime(df['DateTime (UTC)']).dt.strftime('%Y-%m-%d %H:%M:%S UTC')
koinly_format['Sent Amount'] = df['Value_OUT(APE)']
koinly_format['Sent Currency'] = 'APE'
koinly_format['Received Amount'] = df['Value_IN(APE)']
koinly_format['Received Currency'] = 'APE'
koinly_format['Fee Amount'] = ''  # Not available in provided data
koinly_format['Fee Currency'] = ''  # Not available in provided data
koinly_format['Net Worth Amount'] = ''  # Not available in provided data
koinly_format['Net Worth Currency'] = ''  # Not available in provided data
koinly_format['Label'] = ''  # No tagging mint transactions as mining
koinly_format['Description'] = ''  # Not provided in original data
koinly_format['TxHash'] = df['Transaction Hash']



# Generate output file name
output_directory = os.path.dirname(file_path)
output_file = os.path.join(output_directory, "formatted_" + os.path.basename(file_path))

# Save the converted file
koinly_format.to_csv(output_file, index=False)
print(f"Converted data saved to {output_file}")
