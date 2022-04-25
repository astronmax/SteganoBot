from png import TextHider
import os

th = TextHider()
print("Enter the text to hide: ")
hiding_string = input()
th.encode(hiding_string,"stegano/png_images/car.png")
name = os.path.basename(r"stegano/png_images/car.png")
print("Text encoded into", name, sep = " ")
decode_result = th.decode("encoded.png")
if decode_result == None:
    print("The message was not found")
else:
    print("Hiden message: \"", decode_result, "\"", sep = "")