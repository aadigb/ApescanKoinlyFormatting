import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog
import os

root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(title="Select the ApeChain Transaction CSV File", filetypes=[("CSV files", "*.csv")])

if not file_path:
    print("No file selected. Exiting...")
    exit()

try:
    df = pd.read_csv(file_path)
except Exception as e:
    print(f"Error reading the file: {e}")
    exit()


print("Sample Data:\n", df[['UnixTimestamp', 'DateTime (UTC)']].head(10))


if 'UnixTimestamp' not in df.columns:
    print("Error: 'UnixTimestamp' column not found. Exiting...")
    exit()


df['UnixTimestamp'] = pd.to_datetime(df['UnixTimestamp'], errors='coerce')


df = df.dropna(subset=['UnixTimestamp'])

koinly_format = pd.DataFrame()
koinly_format['Date'] = df['UnixTimestamp'].dt.strftime('%Y-%m-%d %H:%M:%S UTC')
koinly_format['Sent Amount'] = df.get('Value_OUT(APE)', np.nan)
koinly_format['Sent Currency'] = 'APE'
koinly_format['Received Amount'] = df.get('Value_IN(APE)', np.nan)
koinly_format['Received Currency'] = 'APE'
koinly_format['Fee Amount'] = ''
koinly_format['Fee Currency'] = ''
koinly_format['Net Worth Amount'] = ''
koinly_format['Net Worth Currency'] = ''
koinly_format['Label'] = ''
koinly_format['Description'] = ''
koinly_format['TxHash'] = df.get('Transaction Hash', '')


output_directory = os.path.dirname(file_path)
output_file = os.path.join(output_directory, "formatted_" + os.path.basename(file_path))

koinly_format.to_csv(output_file, index=False)
print(f"Converted data saved to {output_file}")
