from typing import List
import json

class DatabaseColumn:

    def __init__(self, column_name, column_type, key):

        self.column_name = column_name
        self.column_type = column_type
        self.key = key


class DatabaseSchemaTable:

    def __init__(self, table_name):
        
        self.table_name = table_name
        self.columns = []

    def add_column(self, column: DatabaseColumn):
        self.columns.append(column)

    def add_columns(self, columns: List[DatabaseColumn]):
        [self.add_column(c) for c in columns]

    def has_column(self, column_name):
        return column_name in self.columns
    
    def query_string_create_table(self) -> str:
        """
        Generate the CREATE TABLE statement to create this table
        """
        column_definitions = []
        for col in self.columns:
            column_definitions.append(f"{col.column_name} {col.column_type}{' PRIMARY KEY' if col.key else ''}")

        create_table_sql = f"CREATE TABLE {self.table_name} ({', '.join(column_definitions)})"
        return create_table_sql


class DatabaseRelation:

    def __init__(self, tableA, colA, tableB, colB):

        self.tableA = tableA
        self.colA = colA
        self.tableB = tableB
        self.colB = colB

    
    def connection_clause(self):
        return "WHERE " + self.tableA + "." + self.colA + " = " + self.tableB + "." + self.tableB

class DatabaseSchema:

    def __init__(self, database_name):

        self.database_name = database_name
        # TODO: dictionaries here
        self.tables = []
        self.relations = []

    def load_schema(self, json_data):
        try:
            schema_file = open(json_data)
            data = json.load(schema_file)
            for table_info in data.get("tables", []):
                table = DatabaseSchemaTable(table_info.get("table_name"))
                table.add_columns([DatabaseColumn(**col) for col in table_info.get("columns", [])])
                self.add_table(table)

            for relation_info in data.get("relations", []):
                self.relations.append(DatabaseRelation(**relation_info))

        except json.JSONDecodeError:
            print("Error parsing JSON data.")

    
    def add_table(self, table: DatabaseSchemaTable):
        self.tables.append(table)

    def add_relation(self, relation: DatabaseRelation):
        # Check that both tables in the relation exist
        tableA = [t for t in self.tables if t.table_name == relation.tableA]
        tableB = [t for t in self.tables if t.table_name == relation.tableA]

        if (tableA and tableB):
            if not tableA.has_column(relation.colA):
                raise ValueError("Could not find " + relation.colA + " in " + relation.tableA)
            if not tableB.has_column(relation.colB):
                raise ValueError("Could not find " + relation.colB + " in " + relation.tableA)
            
            # If we get here, we can go ahead and add the relation
            self.relations.append(relation)