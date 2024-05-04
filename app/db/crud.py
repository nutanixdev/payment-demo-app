from sqlalchemy.orm import Session

from . import models, schemas


class PaymentCrud:

    async def create(db: Session, payment: schemas.PaymentCreate):
        db_payment = models.Payment(
            amount=payment.amount,
            currency=payment.currency,
            description=payment.description,
            payee=payment.payee
        )

        db.add(db_payment)
        db.commit()
        db.refresh(db_payment)
        return db_payment
