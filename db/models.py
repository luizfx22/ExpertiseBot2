from sqlalchemy import Column
from sqlalchemy.types import Integer, Text, String

class Role(db.Model):
    id = Column(type=Integer, primary_key=True, nullable=False)
    
