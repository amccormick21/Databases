from typing import List
import mysql.connector
import database_schema.schema

class SqlConnectionInfo:

    def __init__(self, host, user, password):
        """
        Initialize the connection information.

        Args:
            host (str): The hostname or IP address.
            user (str): The username.
            password (str): The password.
        """
        self.host = host
        self.user = user
        self.password = password

class SqlConnectionSettings:

    def __init__(self, auto_commit=False):
        """
        Set important settings for interacting with the database.

        Args:
            auto_commit (bool): True if each change to the connector
                                should be automatically committed to the
                                database
        """
        self.auto_commit = auto_commit


class DatabaseConnector:

    def __init__(self,
                 info: SqlConnectionInfo,
                 settings: SqlConnectionSettings=SqlConnectionSettings()):

        # Establish a connection to MySQL server
        self.db = mysql.connector.connect(
            host=info.host,
            user=info.user,
            passwd=info.password
        )

        # Create a cursor object
        self.cursor = self.db.cursor()
        self.settings = settings
        self.schema = database_schema.schema.DatabaseSchema('')

    def cleanup(self):
        self.cursor.close()
        self.db.close()


    def create_database(self, db_name):

        # Check whether we already have this database
        self.cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")

        if self.cursor.fetchone():
            print('Databse already exists, no need to create')
            self.cursor.execute('USE ' + db_name)
        else:
            # Execute the SQL command to create a new database
            sql = 'CREATE DATABASE ' + db_name
            self.cursor.execute(sql)
        
        # Update the schema
        self.schema.database_name = db_name


    def add_table_to_database(self, table: database_schema.schema.DatabaseSchemaTable):
        
        # Check whether we already have this database
        self.cursor.execute(f"SHOW TABLES LIKE '{table.table_name}'")

        if self.cursor.fetchone():
            print('Table already exists, dropping to recreate')
            self.cursor.execute(f"DROP TABLE {table.table_name}") 

        query = table.query_string_create_table()
        self.cursor.execute(query)


    def create_table_from_schema(self, table: database_schema.schema.DatabaseSchemaTable):

        # Add the table to the database
        self.add_table_to_database(table)

        # Add to the internal schema
        self.schema.add_table(table)


    def create_table(self, table_name, columns: List[database_schema.schema.DatabaseColumn]):

        # Add this table to our internal schema
        table = database_schema.schema.DatabaseSchemaTable(table_name)
        table.add_columns(columns)
        self.schema.add_table(table)

        # Add the table to the database
        self.add_table_to_database(table)

        # Commit the change
        if self.settings.auto_commit:
            self.db.commit()


    def insert_row(self, table_name, values):

        placeholders = ', '.join(['%s'] * len(values))
        query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        self.cursor.execute(query, values)
        if self.settings.auto_commit:
            self.db.commit()


    def delete_row(self, table_name, condition_column, condition_value):

        query = f"DELETE FROM {table_name} WHERE {condition_column} = %s"
        self.cursor.execute(query, (condition_value,))
        if self.settings.auto_commit:
            self.db.commit()

    def run_query(self, query):

        # TODO: use self.relations to apply appropriate WHERE clauses

        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result
    
    def commit(self):
        """
        Commit changes to the database
        This should be called once all row updates are complete
        if not using auto_commit"""
        self.db.commit()


    def add_tables_from_schema(self, schema: database_schema.schema.DatabaseSchema):
        """
        Add the tables specified in the schema given that the database
        already exists
        """
        for table in schema.tables:
            self.create_table_from_schema(table)

        self.schema.relations = schema.relations


    def create_from_schema(self, schema: database_schema.schema.DatabaseSchema):
        """
        Create the database from a specified schema and build
        all of the necessary elements, before committing"""

        self.create_database(schema.database_name)
        self.add_tables_from_schema(schema)

        self.commit()
        self.cleanup()