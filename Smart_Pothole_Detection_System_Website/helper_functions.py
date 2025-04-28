from sqlalchemy import inspect


# extra functions to help me debug and test my website


def print_all_data(db):
    # Get the inspector
    inspector = inspect(db.engine)

    # Get all table names
    table_names = inspector.get_table_names()

    # Iterate over all tables
    for table_name in table_names:
        # Get the table
        table = db.metadata.tables[table_name]

        # Query all records
        records = db.session.query(table).all()

        print(f"\nTable: {table_name}")
        print("-" * 20)

        # Print column names
        columns = [column.key for column in table.columns]
        print(" | ".join(columns))
        print("-" * len(" | ".join(columns)))

        # Print each record
        for record in records:
            record_data = [str(getattr(record, column)) for column in columns]
            print(" | ".join(record_data))

        print("\n")