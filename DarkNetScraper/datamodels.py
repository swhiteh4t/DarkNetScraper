from io import StringIO
from pymongo import MongoClient
import json
from DarkNetScraper.output.colors import ColoredText
from DarkNetScraper.output.file_handlers import save_json
from .time.getime import get_formatted_time
import pandas as pd


class DBConnector:
    client = None
    collection = None
    entries = []

    def __init__(self) -> None:
       # Provide the mongodb atlas url to connect python to mongodb using pymongo
       CONNECTION_STRING = "mongodb://admin:password@127.0.0.1:27017/"
    
       # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
       self.client = MongoClient(CONNECTION_STRING)
       # Specify the name of the database you want to create
       DB_NAME = "DarkNetScraper"

       #Get database names
       databases = self.client.list_database_names()
       # Check if the database exists
       if DB_NAME not in databases:
            # Create the database
            self.db = self.client[DB_NAME]
            print(f"Database '{DB_NAME}' created.")
       else:
            # Database already exists
            self.db = self.client[DB_NAME]
            print(f"Database '{DB_NAME}' already exists.")

       self.collection_name = "Search-" + get_formatted_time()
       self.collection = self.db[self.collection_name]

    def add_entry_generate(self,title,content,category,verbose=False):
        if verbose:
            print(ColoredText("Added entry to collection " + self.collection_name,'white'))
        entry = {
            'title' : title,
            'content' : content,
            'category' : category,
        }
        self.entries.append(entry)



    def add_entry(self,title="",link="",content="",category="",summary="", emails="", address="", phone="", ipv4="", ipv6="", cloud="",verbose=False):
        entry = {
            "Title" : title,
            "Link" : link,
            "Category" : category,
            "Content" : content,
            "Summary" : summary,
            "Email" : emails,
            "Address" : address,
            "Phone" : phone,
            "IPv4" : ipv4,
            "IPv6" : ipv6,
            "CloudDomains" : cloud,
        }
        if verbose:
            print(ColoredText("Added entry to collection " + self.collection_name,'white'))
        self.entries.append(entry)

    def save_db(self):
        if len(self.entries):
            self.collection.insert_many(self.entries)

    def save_to_file(self):
        save_json(self.collection_name + ".json", self.entries)
        df = pd.read_json(StringIO(json.dumps(self.entries)))
        df.to_csv(self.collection_name + ".csv", index=False)
