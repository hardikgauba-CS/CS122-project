# TODO Include proper documentation in the form of docstrings for classes, functions, and methods.

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

#Base class for ORM models
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    money = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Book(id='{self.id}')>"

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False) # 'income' or 'expense'


    def __repr__(self):
        return f"<Transaction(id='{self.id}')>"

User.transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")

engine = create_engine('sqlite:///budgetBuddy_data.db')
Base.metadata.create_all(engine) # Creating the tables
Session = sessionmaker(bind=engine)

# DB functions
def add_user(user_id, user_name, user_money):
    # INSERT INTO
    session = Session()
    if session.query(User).filter(User.id == user_id).first():
        return False, "Book already exists!"
    new_user = User(id=user_id, name=user_name, money=0) # Money might start from 0 or user_money
    session.add(new_user)
    session.commit()
    session.close()
    return True, "User added Successfully!"

def update_user(user_id, user_name, user_money): # Maybe we just want to use this to update the money
    # UPDATE
    session = Session()
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        return False, "User not found!"
    user.name = user_name
    user.money = user_money
    session.commit()
    session.close()
    return True, "User updated successfully!"

def delete_user(user_id):
    # DELETE
    session = Session()
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        return False, "User does NOT exist!"
    session.delete(user)
    session.commit()
    session.close()
    return True, "User deleted successfully!"

def get_users():
    with Session() as session:
        users = session.query(User).all()
        for user in users:
            print(user)
        return users