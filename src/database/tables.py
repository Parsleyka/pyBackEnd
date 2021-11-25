from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from flask_jwt_extended import create_access_token
from datetime import timedelta
from passlib.hash import bcrypt

engine = create_engine("mysql+mysqlconnector://root:myrootpassword@localhost/mydb", echo=True)

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()


class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    nickname = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)
    surname = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(250), nullable=False)
    permissions = Column(String(250), nullable=False)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.surname = kwargs.get('surname')
        self.nickname = kwargs.get('nickname')
        self.email = kwargs.get('email')
        self.password = bcrypt.hash(kwargs.get('password'))
        self.permissions = 'user'

    def get_token(self, expire_time=1):
        expire_delta = timedelta(expire_time)
        token = create_access_token(identity=self.id, expires_delta=expire_delta)
        return token

    @classmethod
    def authentication(cls, email, password):
        user = cls.query.filter(cls.email == email).one()
        if not bcrypt.verify(password, user.password):
            raise Exception('No user')
        return user

    # def __repr__(self):
    #     return f"< User: {str(self.id)}, {self.nickname}, {self.name}, {self.surname}, " \
    #            f"{self.email}, {self.password}, {self.permissions} >"


class Event(Base):
    __tablename__ = 'Event'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(500), nullable=False)
    location = Column(String(250), nullable=False)
    date = Column(DateTime, nullable=False)

    # def __repr__(self):
    #     return f"< Event: {str(self.id)}, {self.name}, {self.description}, {self.location}, {str(self.date)} >"


class Ticket(Base):
    __tablename__ = 'Ticket'

    id = Column(Integer, primary_key=True)
    id_event = Column(Integer, ForeignKey("Event.id"), nullable=False)
    price = Column(DECIMAL, nullable=False)
    status = Column(String(250), nullable=False)

    Event = relationship("Event")

    # def __repr__(self):
    #     return f"< Ticket: {str(self.id)}, {str(self.id_event)}, {str(self.price)}, {self.status} >"


class BoughtTicket(Base):
    __tablename__ = 'Bought_Ticket'

    id = Column(Integer, primary_key=True)
    id_ticket = Column(Integer, ForeignKey("Ticket.id"), nullable=False)
    id_user = Column(Integer, ForeignKey("User.id"), nullable=False)

    Ticket = relationship("Ticket")
    User = relationship("User")

    # def __repr__(self):
    #     return f"< BoughtTicket: {str(self.id)}, {str(self.id_ticket)}, {str(self.id_user)} >"


class ReservedTicket(Base):
    __tablename__ = 'Reserved_Ticket'

    id = Column(Integer, primary_key=True)
    id_ticket = Column(Integer, ForeignKey("Ticket.id"), nullable=False)
    id_user = Column(Integer, ForeignKey("User.id"), nullable=False)

    Ticket = relationship("Ticket")
    User = relationship("User")

    # def __repr__(self):
    #     return f"< ReservedTicket: {str(self.id)}, {str(self.id_ticket)}, {str(self.id_user)} >"


# Base.metadata.create_all(engine)
