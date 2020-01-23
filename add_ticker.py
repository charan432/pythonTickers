from pandas_datareader import data as pdr
from pymongo import MongoClient
import pandas as pd
import yfinance as yf
yf.pdr_override() # <== that's all it takes :-)


#initiate empty tickers list
input_tickers_list = [] 
maxLengthList = 5 # Set maximum entry as 5

while len(input_tickers_list) < maxLengthList:
	item = input("Enter ticker name (Type `quit` to exit): ")
	if(item!='quit'):
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
	data = pdr.get_data_yahoo(tickers_list, start="2017-01-01", end="2017-04-30")['Adj Close']
	
# Print first 5 rows of the data
print(data.head())
print("Insert data into MongoDB....")

#Step 1: Connect to Local MongoDB - Note: Change connection string as needed
#myclient = MongoClient("mongodb://localhost:27017/")
#mydb = myclient["finance"]
#mycol = mydb["mycollection"]


# DB Connection to Atlas Cluster
client = MongoClient("mongodb://charan:Test1234@cluster0-shard-00-00-zaekm.mongodb.net:27017,cluster0-shard-00-01-zaekm.mongodb.net:27017,cluster0-shard-00-02-zaekm.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
my_database = client.finance
mycol = my_database.tickersdb

try:
    print("MongoDB version is %s" % client.server_info()['version'])
except pymongo.errors.OperationFailure as error:
    print(error)
    quit(1)
# End of DB Connection


# Step 2: Insert Data into DB
data.reset_index(inplace=True)
data_dict = data.to_dict("records")
mycol.insert_one({"index":"multipletickers","data":data_dict})
print("Data Saved Successfully.........")

# Step 3: Get data from DB
data_from_db = mycol.find_one({"index":"multipletickers"})
df = pd.DataFrame(data_from_db["data"])
df.set_index("Date",append=True,inplace=True)
print("Fetching data from MongoDB")
print(df)