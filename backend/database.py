# TODO Include proper documentation in the form of docstrings for classes, functions, and methods.

from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import datetime

# ----------Database tables----------
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    money = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Book(id='{self.id}', ' name='{self.name}', ' money={self.money}')>"

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False) # 'income' or 'expense'
    date = Column(Date, default=datetime.date.today(), nullable=False)

    def __repr__(self):
        return f"<Transaction(id='{self.id}', ' amount={self.amount}, type={self.type})>"

User.transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")

engine = create_engine('sqlite:///budgetBuddy_data.db')
Base.metadata.create_all(engine) # Creating the tables
Session = sessionmaker(bind=engine)


# ----------Database functions for user----------
def add_user(user_id, user_name, user_money):
    # INSERT INTO
    with Session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            return False, "User already exists!"
        new_user = User(id=user_id, name=user_name, money=0) # Money might start from 0 or user_money
        session.add(new_user)
        session.commit()
        return True, f"User ({User.name},{User.id}) added Successfully!"

def update_user(user_id, user_name, user_money): # Maybe we just want to use this to update the money
    # UPDATE
    with Session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return False, "User not found!"
        user.name = user_name
        user.money = user_money
        session.commit()
        return True, f"User ({User.name},{User.id}) updated successfully!"

def delete_user(user_id):
    # DELETE
    with Session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return False, f"User:{user_id} does NOT exist!"
        session.delete(user)
        session.commit()
        return True, f"User ({User.name},{User.id}) deleted successfully!"

def get_users():
    with Session() as session:
        users = session.query(User).all()
        for user in users:
            print(user)
        return users

# ----------Database functions for transactions----------
def add_trans(trans_id, trans_user_id, new_amount, trans_type, trans_date):
    # INSERT INTO
    with Session() as session:
        if session.query(Transaction).filter(Transaction.id == trans_id, Transaction.user_id == trans_user_id).first():
            return False, "Transaction already exists!"
        new_trans = Transaction(id=trans_id, user_id=trans_user_id, amount=new_amount, type=trans_type, date=trans_date) # Money might start from 0 or user_money
        session.add(new_trans)
        session.commit()
        return True, f"Transaction {trans_id} added Successfully!"

def delete_trans(trans_id, trans_user_id): #TODO make sure that trans_user_id does not have to be inputted from a user's pov(Under the hood)
    # DELETE
    with Session() as session:
        transaction = session.query(Transaction).filter(Transaction.id == trans_id, Transaction.user_id == trans_user_id).first()
        if not transaction:
            return False, "Transaction does NOT exist!"
        session.delete(transaction)
        session.commit()
        return True, f"Transaction {trans_id} deleted successfully!"

def get_users_transactions(user_id):
    with Session() as session:
        transactions = []
        #TODO implement function
        return transactions