from pymongo import MongoClient

# Base de datos local
#db_client = MongoClient().local

#Base de datos remota
db_client = MongoClient("mongodb+srv://termicelis:termicelis@cluster0.gjhuyzj.mongodb.net/?retryWrites=true&w=majority").test