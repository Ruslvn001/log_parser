from sqlalchemy import Column, String, TIMESTAMP, Index, Integer
from .database import Base

class Message(Base):
    __tablename__ = 'message'

    created = Column(TIMESTAMP, nullable=False)
    id = Column(String, primary_key=True)
    int_id = Column(String(16), nullable=False)
    str = Column(String, nullable=False)

    __table_args__ = (
        Index('message_created_idx', 'created'),
        Index('message_int_id_idx', 'int_id'),
    )


class Log(Base):
    __tablename__ = 'log'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created = Column(TIMESTAMP, nullable=False)
    int_id = Column(String(16), nullable=False)
    str = Column(String)
    address = Column(String)

    __table_args__ = (
        Index('log_address_idx', 'address', postgresql_using='hash'),
    )