import uvicorn
from typing import Callable
from fastapi import FastAPI, Depends, HTTPException, Request, Response, Body
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute
from sqlalchemy.orm import Session

from db import models, schemas
from db.crud import PaymentCrud
from db.database import engine, get_db


class ValidationErrorLoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except RequestValidationError as exc:
                body = await request.body()
                detail = {"errors": exc.errors(), "body": body.decode()}
                raise HTTPException(status_code=422, detail=detail)

        return custom_route_handler


app = FastAPI(
    title="Nutanix .NEXT Demo",
    description="Demo Payment API based on FastAPI with Swagger and Sqlachemy[postgres]",
    version="1.0.0"
)
app.router.route_class = ValidationErrorLoggingRoute

models.Base.metadata.create_all(bind=engine)


@app.post("/payments/", tags=["Payment"], response_model=schemas.Payment, status_code=201)
async def create_payment(payment_request: schemas.PaymentCreate = Body(), db: Session = Depends(get_db)):
    """
    Create a Payment and store it in the database
    """

    return await PaymentCrud.create(db=db, payment=payment_request)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
