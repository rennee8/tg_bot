from sqlalchemy import Column, Integer, String, DateTime, BigInteger, func
from sqlalchemy.orm import declarative_base
from loader import engine

Base = declarative_base()


class Groups(Base):
    __tablename__ = 'groups'
    group = Column(String(10), unique=True, nullable=True, primary_key=True,
                   autoincrement=False)
    value_group = Column(Integer, nullable=True)


class Schedule(Base):
    __tablename__ = 'schedule'
    group = Column(String(10), unique=True, nullable=True, primary_key=True,
                   autoincrement=False)
    monday = Column(String(1000), nullable=True)
    tuesday = Column(String(1000), nullable=True)
    wednesday = Column(String(1000), nullable=True)
    thursday = Column(String(1000), nullable=True)
    friday = Column(String(1000), nullable=True)
    saturday = Column(String(1000), nullable=True)
    created_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)


class Users(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, autoincrement=False, unique=True)
    user_name = Column(String(50), nullable=False)
    group = Column(String(10), nullable=False)


class Users_Last_Message(Base):
    __tablename__ = "users_last_message"
    id = Column(BigInteger, primary_key=True, autoincrement=False, unique=True)
    message_id = Column(Integer, nullable=True)


class Update_Table_Date(Base):
    __tablename__: str = "update_table_date"
    table_name: str = Column(String(20), primary_key=True, autoincrement=False, unique=True)
    created_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=True)


Base.metadata.create_all(engine)
