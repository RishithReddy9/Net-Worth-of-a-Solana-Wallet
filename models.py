from sqlalchemy import Column, Integer, String, Float
from database import Base


class Wallet(Base):
    __tablename__ = "wallets"
    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float)
