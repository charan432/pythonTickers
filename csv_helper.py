from pandas_datareader import data as pdr
from pymongo import MongoClient
import pandas as pd
import yfinance as yf
yf.pdr_override()  # <== that's all it takes :-)


# initiate empty tickers list
input_tickers_list = []
maxLengthList = 5  # Set maximum entry as 5

while len(input_tickers_list) < maxLengthList:
    item = input("Enter ticker name (Type `quit` to exit): ")
    if(item != 'quit'):
        input_tickers_list.append(item)
        print(input_tickers_list)
    else:
        break
print("That's your Tickers List")
print(input_tickers_list)

# Define the ticker list
tickers_list = input_tickers_list
data = pd.DataFrame(columns=tickers_list)

# Fetch the data
for ticker in tickers_list:
    data = pdr.get_data_yahoo(
        tickers_list, start="2017-01-01", end="2017-04-30")['Adj Close']

# Print first 5 rows of the data
print("First 5 rows of data")
print(data.head())


data.reset_index(inplace=True)
data_dict = data.to_dict("records")
print("Data Saved Successfully.........")

print("Fetching data from MongoDB")
# df = pd.DataFrame(data_from_db["data"])
# df.set_index("Date", append=True, inplace=True)

# print(df)
print("export to csv:")
fileName = input("Enter FileName to export  ")
data.to_csv("fav_quotes.csv", index=False)
print("exported to file " + fileName)
