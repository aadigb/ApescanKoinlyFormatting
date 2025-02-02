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

# Print first few rows to inspect data
print("Sample Data:\n", df.head())

# Ensure 'DateTime (UTC)' column exists
if 'DateTime (UTC)' not in df.columns:
    print("Error: 'DateTime (UTC)' column not found in the CSV file. Exiting...")
    exit()

# Identify problematic values in 'DateTime (UTC)'
invalid_dates = df[~df['DateTime (UTC)'].astype(str).str.match(r'^\d{4}-\d{2}-\d{2}')]

if not invalid_dates.empty:
    print("Warning: Some rows have invalid DateTime values and will be removed.")
    print(invalid_dates[['DateTime (UTC)']].head())

# Convert 'DateTime (UTC)' column to datetime, handling errors
df['DateTime (UTC)'] = pd.to_datetime(df['DateTime (UTC)'], errors='coerce')

# Drop rows where datetime conversion failed (i.e., invalid entries)
df = df.dropna(subset=['DateTime (UTC)'])

# Create Koinly universal import format
koinly_format = pd.DataFrame()
koinly_format['Date'] = df['DateTime (UTC)'].dt.strftime('%Y-%m-%d %H:%M:%S UTC')
koinly_format['Sent Amount'] = df.get('Value_OUT(APE)', np.nan)
koinly_format['Sent Currency'] = 'APE'
koinly_format['Received Amount'] = df.get('Value_IN(APE)', np.nan)
koinly_format['Received Currency'] = 'APE'
koinly_format['Fee Amount'] = ''  # Not available in provided data
koinly_format['Fee Currency'] = ''  # Not available in provided data
koinly_format['Net Worth Amount'] = ''  # Not available in provided data
koinly_format['Net Worth Currency'] = ''  # Not available in provided data
koinly_format['Label'] = ''  # No tagging mint transactions as mining
koinly_format['Description'] = ''  # Not provided in original data
koinly_format['TxHash'] = df.get('Transaction Hash', '')

# Generate output file name
output_directory = os.path.dirname(file_path)
output_file = os.path.join(output_directory, "formatted_" + os.path.basename(file_path))

# Save the converted file
koinly_format.to_csv(output_file, index=False)
print(f"Converted data saved to {output_file}")
