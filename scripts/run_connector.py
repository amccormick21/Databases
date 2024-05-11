import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import database_schema.schema as schema
import database_connector.connector as con

connection_info = con.SqlConnectionInfo(host="localhost",user="root",password="password")
settings = con.SqlConnectionSettings(auto_commit=False)
db_schema = schema.DatabaseSchema("MessageInABottle_Persist")
db_schema.load_schema(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'MessageBottleSchema.json'))

db = con.DatabaseConnector(connection_info, settings)
db.create_from_schema(db_schema)  
