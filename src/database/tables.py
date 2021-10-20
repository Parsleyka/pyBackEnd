from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

engine = create_engine("mysql+mysqlconnector://root:myrootpassword@localhost/mydb", echo=True)

Base = declarative_base()


class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    nickname = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)
    surname = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    permissions = Column(String(250), nullable=False)

    def __repr__(self):
        return "<User( '%s', '%s', '%s', '%s', '%s', '%s', '%s')>" % (str(self.id), self.nickname, self.name,
                                                                      self.surname, self.email, self.password,
                                                                      self.permissions)


class Event(Base):
    __tablename__ = 'Event'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(500), nullable=False)
    location = Column(String(250), nullable=False)
    date = Column(DateTime, nullable=False)

    def __repr__(self):
        return "<User( '%s', '%s', '%s', '%s', '%s')>" % (str(self.id), self.name, self.description, self.location,
                                                          str(self.date))



class Ticket(Base):
    __tablename__ = 'Ticket'

    id = Column(Integer, primary_key=True)
    id_event = Column(Integer, ForeignKey("Event.id"), nullable=False)
    price = Column(DECIMAL, nullable=False)
    status = Column(String(250), nullable=False)

    Event = relationship("Event")

    def __repr__(self):
        return "<User( '%s', '%s', '%s', '%s')>" % (str(self.id), str(self.id_event), str(self.price), self.status)


class BoughtTicket(Base):
    __tablename__ = 'Bought_Ticket'

    id = Column(Integer, primary_key=True)
    id_ticket = Column(Integer, ForeignKey("Ticket.id"), nullable=False)
    id_user = Column(Integer, ForeignKey("User.id"), nullable=False)

    Ticket = relationship("Ticket")
    User = relationship("User")

    def __repr__(self):
        return "<User( '%s', '%s', '%s')>" % (str(self.id), str(self.id_ticket), str(self.id_user))

class ReservedTicket(Base):
    __tablename__ = 'Reserved_Ticket'

    id = Column(Integer, primary_key=True)
    id_ticket = Column(Integer, ForeignKey("Ticket.id"), nullable=False)
    id_user = Column(Integer, ForeignKey("User.id"), nullable=False)

    Ticket = relationship("Ticket")
    User = relationship("User")

    def __repr__(self):
        return "<User( '%s', '%s', '%s')>" % (str(self.id), str(self.id_ticket), str(self.id_user))


Base.metadata.create_all(engine)
