from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tables import *

session = sessionmaker(bind=engine)
s = session()

# new_user = User(nickname="Parsley", name="N", surname="S", email="@", password="pass", permissions="Admin")
# s.add(new_user)
# s.commit()

res = s.query(User).filter(User.id >= 0)

for row in res:
    print(row)
