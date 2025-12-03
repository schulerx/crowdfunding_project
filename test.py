from sqlalchemy import create_engine, inspect
 
engine = create_engine("sqlite:///./ crowdfunding.db")
inspector = inspect(engine)
 
print("Таблицы в базе данных:")
for table_name in inspector.get_table_names():
    print(f"- {table_name}")
 
    print(" Колонки:")
    for column in inspector.get_columns(table_name):
        print(f" - {column['name']} ({column['type']})")
 