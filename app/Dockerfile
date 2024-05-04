FROM mcr.microsoft.com/vscode/devcontainers/python:3.12-bookworm

LABEL org.opencontainers.image.source=https://github.com/nutanixdev/payment-demo-app
LABEL org.opencontainers.image.description="Payment Demo App"
LABEL org.opencontainers.image.licenses=MIT

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY ./requirements.txt ./
 
RUN pip install --no-cache-dir --upgrade -r requirements.txt

USER 1001

COPY . ./

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]