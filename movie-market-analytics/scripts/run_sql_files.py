from src.db.mysql_helper import MySQLHelper

sql_files = [
    "sql/ddl/01_create_database.sql",
    "sql/ddl/02_create_tables.sql",
    "sql/ddl/03_create_indexes.sql",
]

db = MySQLHelper()

for f in sql_files:
    with open(f, encoding="utf-8") as file:
        sql = file.read()
    db.execute(sql)
    print(f"Executed {f}")