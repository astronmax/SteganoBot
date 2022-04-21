import numpy
import PIL.Image


class TextHider:
    '''
    This class provides encode and decode methods text information.
    Works with PNG images.
    '''

    def __init__(self, stop_indicator="$STOP$") -> None:
        self.stop_indicator = stop_indicator

    def encode(self, secret: str, filename: str, out: str) -> None:
        '''
        Method encodes text into given image using LSB.
        secret: text information to hide
        filename: image in which we want to encode secret
        out: name of encoded image
        '''

        # open image, get basic info and data
        image = PIL.Image.open(filename, 'r')
        width, height = image.size
        img_arr = numpy.array(image.getdata())  # data of image

        if image.mode == "P":
            raise ValueError("Unsupported type of PNG image")

        channels = 4 if image.mode == "RGBA" else 3
        pixels = img_arr.size // channels
        secret += self.stop_indicator

        # get bytes of secret
        byte_msg = ''.join(f"{ord(c):016b}" for c in secret)
        bits = len(byte_msg)
        if bits > pixels:
            raise ValueError("Not enought space in PNG image")

        # write bytes into image data
        index = 0
        for i in range(pixels):
            for j in range(0, 3):
                if index < bits:
                    img_arr[i][j] = int(
                        bin(img_arr[i][j])[-1] + byte_msg[index], 2)
                    index += 1

        # create encoded image usign changed data
        img_arr = img_arr.reshape((height, width, channels))
        result = PIL.Image.fromarray(img_arr.astype('uint8'), image.mode)
        result.save(out)

    def decode(self, filename: str) -> str:
        '''
        Method decodes text from given image which is encoded with "encode" method.
        Returns encoded message or None if image isn't encoded.
        filename: encoded image
        '''

        # open image, get basic info and data
        image = PIL.Image.open(filename, 'r')
        img_arr = numpy.array(image.getdata())
        channels = 4 if image.mode == "RGBA" else 3
        pixels = img_arr.size // channels

        # get secret bits from least significant bits of color channels
        secret_bits = [bin(img_arr[i][j])[-1]
                       for i in range(pixels) for j in range(0, 3)]
        secret_bits = ''.join(secret_bits)
        secret_bits = [secret_bits[i:i+8]
                       for i in range(0, len(secret_bits), 8)]

        # decode bits into text
        secret = [chr(int(secret_bits[i] + secret_bits[i+1], 2))
                  for i in range(0, len(secret_bits), 2)]
        secret = ''.join(secret)

        # check if stop indicator in secret
        if self.stop_indicator in secret:
            return secret[:secret.index(self.stop_indicator)]
        else:
            return None