from pydantic import BaseModel, Field, validator
from typing import Optional
from iso4217 import find_currency, CurrencyNotFoundError


class PaymentBase(BaseModel):
    payee: str
    amount: float = Field(
        gt=0, description="The amount must be greater than zero")
    currency: str = Field(min_length=3, max_length=3,
                          description="Three-letter ISO currency code, in lowercase. Must be a supported currency.")
    description: Optional[str] = Field(max_length=200)

    @validator('currency')
    def currency_must_be_iso4217(cls, v):
        assert v.isalpha(), 'must be alphabet'
        try:
            find_currency(alphabetical_code=v)
        except CurrencyNotFoundError:
            raise ValueError('Must be a valid ISO currency code.')

        return v


class PaymentCreate(PaymentBase):
    pass


class Payment(PaymentBase):
    id: int

    class Config:
        orm_mode = True
