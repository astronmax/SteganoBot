FROM python:3.10-alpine3.15
COPY ./requirements.txt .
COPY ./src/stegano-bot/ .

ENV token=29e2bdd91405a6cb1f2d35bc02edf0d089725d24a38f2c5deba73eaa8cb6a6e4ca6b589485940fbb1240c

# packages for numpy and pillow
RUN apk add --no-cache musl-dev linux-headers g++ git
RUN apk add --no-cache tiff-dev jpeg-dev openjpeg-dev zlib-dev freetype-dev lcms2-dev \
    libwebp-dev tcl-dev tk-dev harfbuzz-dev fribidi-dev libimagequant-dev \
    libxcb-dev libpng-dev

RUN apk add  --no-cache ffmpeg

RUN pip3 install -r requirements.txt

CMD ["python", "-u", "main.py"]