FROM python:3.10-alpine3.15

WORKDIR /code
COPY ./requirements.txt .

# packages for numpy and pillow
RUN apk add --no-cache musl-dev linux-headers g++ git
RUN apk add --no-cache tiff-dev jpeg-dev openjpeg-dev zlib-dev freetype-dev lcms2-dev \
    libwebp-dev tcl-dev tk-dev harfbuzz-dev fribidi-dev libimagequant-dev \
    libxcb-dev libpng-dev

RUN pip3 install -r requirements.txt

CMD ["sh"]