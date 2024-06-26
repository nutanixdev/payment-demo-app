import uvicorn
import config
import httpx
from typing import Callable
from typing_extensions import Annotated
from fastapi import FastAPI, Depends, HTTPException, Request, Response, Body
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from functools import lru_cache



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
    title="Nutanix Cloud Native Demo",
    description="Demo Payment API based on FastAPI with Swagger and Sqlachemy[postgres]",
    version="1.0.0"
)
app.router.route_class = ValidationErrorLoggingRoute

models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.post("/payments/", tags=["Payment"], response_model=schemas.Payment, status_code=201)
async def create_payment(payment_request: schemas.PaymentCreate = Body(), db: Session = Depends(get_db)):
    """
    Create a Payment and store it in the database
    """

    return await PaymentCrud.create(db=db, payment=payment_request)

# Load config just once
@lru_cache
def get_settings():
    return config.Settings()

# Read .env
@app.get("/info", include_in_schema=False)
async def info(settings: Annotated[config.Settings, Depends(get_settings)]):
    return {
        "account_name": settings.account_name,
        "currencies": settings.currencies,
    }

# index page, welcome
@app.get("/", include_in_schema=False)
async def index(request: Request, settings: Annotated[config.Settings, Depends(get_settings)]):
    return templates.TemplateResponse(
        name="index.html", context={
            "request": request, 
            "currencies": settings.currencies.split(","), 
            "account_name": settings.account_name
        }
    )

class FormData(BaseModel):
    payee: str
    currency: str
    amount: float
    description: str

@app.post("/process_form_data", include_in_schema=False)
async def process_form_data(form_data: FormData):
    print(form_data.dict())
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post("http://localhost:8000/payments/", json=form_data.dict())
            response.raise_for_status()
            return JSONResponse(content={"message": "Form data processed successfully"})
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
