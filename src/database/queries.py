from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tables import *

engine = create_engine("mysql+mysqlconnector://root:myrootpassword@localhost/mydb", echo=True)

session = sessionmaker(bind=engine)
s = session()

new_user = User(nickname="Parsley", name="N", surname="S", email="@", password="pass", permissions="Admin")
s.add(new_user)
s.commit()
