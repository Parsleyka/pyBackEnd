from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tables import *

session = sessionmaker(bind=engine)
s = session()

new_user = User(nickname="Parsley", name="N", surname="S", email="@", password="pass", permissions="Admin")
new_user1 = User(nickname="Chel", name="C", surname="S", email="@", password="pass", permissions="User")
new_event = Event(name="Concert", description="Big Concert", location="Lviv", date="2021-10-06 17:12:00")
new_ticket = Ticket(id_event=1, price=100.0, status="Valid")
new_ticket2 = Ticket(id_event=1, price=100.0, status="Reserved")
new_ticket3 = Ticket(id_event=1, price=100.0, status="Bought")
new_bought = BoughtTicket(id_ticket=3, id_user=2)
new_reserved = ReservedTicket(id_ticket=2, id_user=1)

s.add(new_user)
s.add(new_user1)
s.add(new_event)
s.add(new_ticket)
s.add(new_ticket2)
s.add(new_ticket3)
s.add(new_bought)
s.add(new_reserved)

s.commit()

# res = s.query(User).filter(User.id >= 0)
#
# for row in res:
#     print(row)
