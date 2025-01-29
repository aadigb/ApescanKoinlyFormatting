# ApescanKoinlyFormatting
Collection of python scripts and instructions to generate wallet activity csv's from Apescan.io and format them for importing into Koinly.io.

Disclaimer. This may not work. Review uploaded transactions thoroughly.

Step 1. 
Go to apescan.io/exportData
Choose the export type, enter the address, and select the date range.
Download the CSV. Make sure you retain the default file name.
You will want to download the first 4 export types to capture all the token activities of the wallet.
(Transactions, Internal, Tokenn Transfers (ERC20), and NFT Transfers (ERC-721 & ERC-1155)

Step 2.
(This is not a python tutorial. There are many ways to run a python script)
Run each python script individually, and select the file associate with the script. (i.e. When you run koinlyApechainFormatTx.py, select the Transactions export, etc.)
New files will be saved in the same directory as the selected file, with the prefix "formatted_"

Step 3.
Go to koinly>wallets>add wallet and type in "Apechain"
Select the custom option
Select import from file
Upload all 4 "formatted_" files
Reconcile the rest within koinly.
