import time

from sqlalchemy import String, Integer, Float, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, Query

Base = declarative_base()
Session = scoped_session(sessionmaker(query_cls = Query))

class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key = False)
    sido = Column(String)
    sigungu = Column(String)
    reportedTime = Column(Float)

    def __init__(self, sido, sigungu):
        self.sido = sido
        self.sigungu = sigungu
        self.reportedTime = time.time()
