from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker, relationship
import time
from db_constants import MYSQL_INFO
from item import Item

"""Long-term memory module. """


class LTM(object):

    # Initialize the STM object
    def __init__(self):
        self.engine = None
        self.items_table = None
        self.sql_session = None
        self.sql_connection = None
        self.score_constant = 0.00001
        self.initialize_sql_connection()

    # Initialize the MySQL connection using the connection string provided in db_constants.py.
    def initialize_sql_connection(self):
        self.engine = create_engine(MYSQL_INFO["connection_string"])
        metadata = MetaData()
        self.items_table = Table('items', metadata, autoload=True, autoload_with=self.engine)
        self.sql_session = sessionmaker(bind=self.engine)()
        self.sql_connection = self.engine.connect()

    # Store a pair of items received from STM as a row in MySQL.
    def store_items(self, items):
        for items_tuple in items:
            row = self.get_items_using_connection(items_tuple)
            if row is None:
                self.insert_items(items_tuple)
            else:
                self.increment_score(items_tuple, row["score"])

    # Get a pair of items from LTM.
    def get_items(self, items_tuple):
        item1, item2, time_diff = items_tuple
        result = self.engine.execute(self.items_table.select().where(item1=item1, item2=item2))
        for row in result:
            pass
        rows = result.fetchall()
        result.close()
        return rows

    # Get an item given an associated item.
    def retrieve_item_using_connection(self, item):
        string_query = text("SELECT item2 FROM items where item1 = :item order by score desc")
        first_row = self.sql_connection.execute(string_query, {'item': item}).fetchone()
        if first_row is not None:
            return first_row['item2']
        return None

    # Get multiple items given an associated item. Same as the function above except that it returns many items.
    def retrieve_items_using_connection(self, items):
        results = []
        print(items)
        for item in items:
            list_of_items = []
            string_query = text("SELECT item2 FROM items where item1 = :item order by score desc limit 5")
            returned_list = self.sql_connection.execute(string_query, {'item': item}).fetchall()
            print(returned_list)
            if returned_list is not None and len(returned_list) > 0:
                for row in returned_list:
                    list_of_items.append(row[0])
                if returned_list is not None:
                    results.append(list_of_items)
        print(results)
        return self._find_intersection(results)

    # Find the set intersection of the lists provided.
    @staticmethod
    def _find_intersection(lists):
        if len(lists) > 0:
            intersection = set(lists[0])
            for elist in lists:
                intersection = intersection & set(elist)
            return list(intersection)
        else:
            return []

    # Get items but using the connection object in SQLAlchemy.
    def get_items_using_connection(self, items_tuple):
        item1, item2, time_diff = items_tuple
        string_query = text("SELECT * FROM items where item1 = :item1 and item2 = :item2 order by score desc")
        first_row = self.sql_connection.execute(string_query, {'item1': item1, 'item2': item2}).fetchone()
        if first_row:
            return first_row
        return None

    # Insert a pair of items in the LTM as a row.
    def insert_items(self, items_tuple):
        item1, item2, time_diff = items_tuple
        result = self.engine.execute(self.items_table.insert().values(item1=item1,
                                                                      item2=item2,
                                                                      score=self.score_constant / time_diff,
                                                                      last_updated=time.time()))

    # Increment the score of a pair of items in the LTM.
    def increment_score(self, items_tuple, current_score):
        item1, item2, time_diff = items_tuple
        result = self.engine.execute(self.items_table.update().where(self.items_table.c.item1 == item1).where(self.items_table.c.item2 == item2).values(
                                                                      score=current_score + (self.score_constant / time_diff),
                                                                      last_updated=time.time()))

    # Close the SQL connection and free the resources.
    def close_sql_connection(self):
        self.sql_connection.close()
        self.sql_session.close()
        self.engine.dispose()





