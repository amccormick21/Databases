# Message In A Bottle Databases

## Database Tools
The `database_connector` package is a Python package designed to simplify database schema management and provide tools for interacting with MySQL databases. It includes modules for creating and managing the data in databases, allowing it to be inserted and queried. There are scripts to demonstrate the setup of a database from scratch, and test coverage (in progress)

## Features
- Schema Creation: Easily create databases with predefined schemas, either through code or using a `json` definition of the database schema.
- Relational database management: specify the database relations for easier querying of large datasets
- Table Management: Define and manage tables within your database.
- Data Management: Add and delete rows in the database and write custom queries
- Unit Testing: Write dedicated unit tests for your database-related functions.

# Usage
## Prerequisites
- You need the `mysql.connector` package installed
- Access to a database to modify and query

## Initialize the connector
```
import database_schema.schema as schema
import database_connector.connector as con

connection_info = con.SqlConnectionInfo(host="your_host",user="your_user",password="your_password")
settings = con.SqlConnectionSettings(auto_commit=False)
db = con.DatabaseConnector(connection_info, settings)
```

- The `SqlConnectionInfo` object contains your SQL login details. If you wish to hide your password, subclassing this object is completely valid.
- The `SqlConnectionSettings` is a place in which options can be added to control how the database is managed. The only option available at the moment is `auto_commit`, which controls whether data is committed to the database after every individual row insertion or whether data is committed to the database in a batch
- `DatabaseConnector` is an object which then provides methods for interacting with the database 

## Set Up the Database
```
db_schema.load_schema(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'path_to_schema.json'))
db.create_from_schema(db_schema)  
```
- `load_schema` loads a schema from a json file. A sample `json` is provided at `scripts/MessageBottleSchema.json`
- `create_from_schema` creates the database with the schema specified in the `json`

# Internal Documentation
## Schema
The `DatabaseConnector` maintains an internal schema which is unrelated to any schema objects provided to it. Testing of the database requires that the internal schema matches the intended schema, _and_ that the actual SQL database matches the internal schema at all times.

Many of the open issues related to removing any edge cases where this might go wrong.

The `database_schema` is not fully featured and is quite limited in scope and internal verification.

# Contributing
Contributions are welcome! If you find any issues or have suggestions, feel free to open an issue or submit a pull request.

There are several areas which would benefit from attention at the moment. See the `issues` in the repo for more information.

# License
Do whatever you want, to be honest.
Written by Alex McCormick as part of a demo/framework for the `Message In A Bottle` project authored by `Inguzl`
