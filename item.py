from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# SQLAlChemy related object to properly use the library.


class Item(Base):
    __tablename__ = "items"
    id = Column('id', Integer, primary_key=True)
    item1 = Column('item1', String)
    item2 = Column('item2', String)
    last_updated = Column('last_updated', Integer)
    score = Column('score', Integer)
