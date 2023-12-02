from pymongo import MongoClient

class MongoDBConnection:
    """
    A class to represent mongodb connection.

    ...

    Attributes
    ----------
    host : str
        host of the mongodb
    port : int
        port of the mongodb
    db_name : str
        database name of the mongodb
    client : MongoClient
        mongodb client
    db : Database
        mongodb database

    Methods
    -------
    connect()
        Connects to mongodb.
    disconnect()
        Disconnects from mongodb.
    
    """
    def __init__(self, host='localhost', port=27017, db_name='ayberk_deringoz'):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.client = None
        self.db = None

    def connect(self):
        self.client = MongoClient(self.host, self.port)
        self.db = self.client[self.db_name]

    def disconnect(self):
        if self.client:
            self.client.close()

class CollectionManager:
    """
    A class to represent collection manager.

    ...

    Attributes
    ----------
    db_connection : MongoDBConnection
        mongodb connection
    collection : Collection
        mongodb collection

    Methods
    -------
    insert_data(data)
        Inserts data to mongodb.
    """
    def __init__(self, db_connection, collection_name):
        self.db_connection = db_connection
        self.collection = self.db_connection.db[collection_name]

    def insert_data(self, data):
        result = self.collection.insert_one(data)
        return result.inserted_id
    
    def show_news_collections(self):
        for news in self.collection.find().sort('update_date', -1):
            print(news)



