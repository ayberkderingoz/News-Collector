from MongoDBConnection import MongoDBConnection
from MongoDBConnection import CollectionManager

def main():
    mongo_connection = MongoDBConnection()
    mongo_connection.connect()
    collection_manager = CollectionManager(mongo_connection, 'news')
    collection_manager.show_news_collections()

if __name__ == "__main__":
    main()