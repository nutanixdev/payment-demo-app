from sqlalchemy import Column, Integer, String, Float

from .database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float(precision=2), nullable=False)
    currency = Column(String(3), nullable=False)
    payee = Column(String(200), nullable=False)
    description = Column(String(200))

    def __repr__(self) -> str:
        return super().__repr__(f'PaymentModel(amount={self.amount}, currency={self.currency})')
