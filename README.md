# Stegcrypt
An image steganography project where we can hide text in an image at a random channels of random pixels via the Least Siginifacnt Byte technique. Written in Python 3.7 using the Pillow package from PyPI.

# Information
The project was an attempt to get myself started with coding, namely in Python, and to get acquainted with Steganography as a whole.
We take an image that we can use to hide the message inside of(Only images without compression are supported, namely not JPEG as LSB bits might get tampered during the compression phase).

# Python Module
Text encoding:
We take input from the user in the form of a string and turn it to binary:
```
originalText = input('Please enter the message:')

textBinary = [format(ord(ch), '08b') for ch in originalText]
textBinary = [list(map(int, x)) for x in textBinary]
textBinary = sum(textBinary,[])
```
The binary then gets added to another string that contains the channel of a pixel(either R, G, or B) and the number of the pixel(starting from upper left and going to the bottom right).

Text Decoding:
Using the string we created during the encoding, we can then decipher both the channel and the pixel where the binary of the message is stored.
Image 
# Sources
Pillow Package - https://pypi.org/project/Pillow/
