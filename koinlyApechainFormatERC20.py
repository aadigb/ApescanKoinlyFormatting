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

# Extract filename from path
filename = os.path.basename(file_path)

# Find the starting index of the address (assuming it starts with "0x")
start_index = filename.find("0x")

# Extract Ethereum address if found
if start_index != -1:
    eth_address = filename[start_index:].replace(".csv", "")
else:
    eth_address = None  # No address found in filename
    print(f"Error in filename. Does not contain address.: {e}")

# Read the CSV file
try:
    df = pd.read_csv(file_path)
except Exception as e:
    print(f"Error reading the file: {e}")
    exit()

# Convert Data
koinly_format = pd.DataFrame()

# Format date
koinly_format['Date'] = pd.to_datetime(df['DateTime (UTC)'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S UTC')

# Determine sent/received transactions
koinly_format['Received Amount'] = df['TokenValue'].where(df['To'].str.lower() == eth_address.lower(), '')
koinly_format['Received Currency'] = df['TokenSymbol'].where(df['To'].str.lower() == eth_address.lower(), '')

koinly_format['Sent Amount'] = df['TokenValue'].where(df['From'].str.lower() == eth_address.lower(), '')
koinly_format['Sent Currency'] = df['TokenSymbol'].where(df['From'].str.lower() == eth_address.lower(), '')

# Fees
koinly_format['Fee Amount'] = df['TxnFee(APE)'] if 'TxnFee(APE)' in df.columns else ''
koinly_format['Fee Currency'] = 'APE' if 'TxnFee(APE)' in df.columns else ''

# Other Columns
koinly_format['Net Worth Amount'] = ''
koinly_format['Net Worth Currency'] = ''
koinly_format['Label'] = ''
koinly_format['Description'] = ''
koinly_format['TxHash'] = df['Transaction Hash']


# Generate output file name
output_directory = os.path.dirname(file_path)
output_file = os.path.join(output_directory, "formatted_" + os.path.basename(file_path))

# Save the converted file
koinly_format.to_csv(output_file, index=False)
print(f"Converted data saved to {output_file}")
