# Stegcrypt
An image steganography project where we can hide text in an image at a random channels of random pixels via the Least Siginifacnt Byte technique. Written in Python 3.7 using the Pillow package from PyPI and pymongo.

# Information
The project was an attempt to get myself started with coding, namely in Python, and to get acquainted with Steganography as a whole.
We take an image that we can use to hide the message inside of(Only images without compression are supported, namely not JPEG as LSB bits might get tampered during the compression phase) and use it to hide the message.

# Main Page
The master branch will serve as the main page for the tool. From here you can select the desired version/implementation by selecting the appropriate branch.

The branches are:
Python2:A version of the tool for python 2
Python3:A version of the tool for python 3
Database-Implementation:A version of the tool where we can use a database(i.e.: MongoDB) to store hashes of the keys to then decypher the message in the image.

# Sources
Pillow Package - https://pypi.org/project/Pillow/
pymongo - https://pypi.org/project/pymongo/
