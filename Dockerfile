FROM python:3.10-alpine3.15

WORKDIR /code
COPY ./requirements.txt .
RUN apk add --no-cache musl-dev linux-headers g++ gcc make libffi-dev openssl-dev bash capstone git
RUN pip3 install -r requirements.txt

CMD ["sh"]