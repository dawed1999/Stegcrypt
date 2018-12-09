# Stegcrypt
An image steganography project where we can hide text in an image at a random channels of random pixels via the Least Siginifacnt Byte technique. Written in Python 3.7 and MongoDB using the Pillow and pymongo packages from PyPI.

# Information
The project was an attempt to get myself started with coding, namely in Python, and to get acquainted with Steganography as a whole.
We take an image that we can use to hide the message inside of(Only images without compression are supported, namely not JPEG as LSB bits might get tampered during the compression phase) and use it to hide the message.
This version employes a database which allows for the encryption of the `key` string and for a username and password to be set so that only users that are known by the database can recive the message. 

# Python Module
## Database
We connect to the database, the `client` table and the `hashtable` collection:
```
client = MongoClient('localhost', 27017)
db = client.table
collection = db.hashtable
```
**During Encoding:**

After the encoding is done(which will be explained in the next section) the key generated will be hashed and will be inserted to the database.
```
hasher = hashlib.sha256()
hasher.update(key.encode('utf-8'))
print('Key(Hash):',hasher.hexdigest(), '\n', sep="")

collection.insert_one({"hash":hasher.hexdigest(), "key":key})
```

**During Decoding:**

We check the collection for the `hashkey` and from there we check for the `key`:
```
doc = collection.find({"hash":hashkey})
for value in doc:
    value=str(value)[2:-2]
value = value.replace(" ", "")
value = value.replace("'", "")
value = value.split(',')
for x in value:
    if "key:" in x:
        key = x[4:]

```
## Text encoding:
We take input from the user in the form of a string and turn it to binary:
```
originalText = input('Please enter the message:')

textBinary = [format(ord(ch), '08b') for ch in originalText]
textBinary = [list(map(int, x)) for x in textBinary]
textBinary = sum(textBinary,[])
```
The binary then gets added to another string that contains the channel of a pixel(either R, G, or B) and the number of the pixel(starting from upper left and going to the bottom right).


## Image manipulation:

**During Encoding:**

Using Pillow, we can take an image and crate 3 lists. Each containing the values(that are stored as decimals) of each channel(R, G, or B) in the image:
```
RedChannel = list(carrierImage.getdata(band=0))
GreenChannel = list(carrierImage.getdata(band=1))
BlueChannel = list(carrierImage.getdata(band=2))
```
Then, convert them to binary as well as store them as their own lists(We use the function"ChannelBinary" to achive this):
```
def ChannelBinary(channel):
    ChannelBinary = [format(pix, '08b') for pix in channel]
    ChannelBinary = [list(map(int, n)) for n in ChannelBinary]
    return ChannelBinary
```
We can now remove from each binary value the lsb(which is the last byte of a binary) and append one from the binary of the message. We use a dictionary to define red, green and blue channles as 'r', 'g', and 'b' accordingly as 'channels' and an `if` statment to append the lsb to the value's binary:
```
channels = {'r': RedChannelBinary, 'g': GreenChannelBinary, 'b': BlueChannelBinary}
for channel, pix, lsb in combinedList:
    channels[channel][pix].pop(-1)
    channels[channel][pix].append(lsb)
    
RedChannelBinary = ChannelBinary(RedChannel)
GreenChannelBinary = ChannelBinary(GreenChannel)
BlueChannelBinary = ChannelBinary(BlueChannel)
```

Since the moddified lists are now done, we can convert them again to decimal values and store them:
```
RedChannelBinary = [''.join(map(str, pix)) for pix in RedChannelBinary]
RedChannelBinary = [int(pix, 2) for pix in RedChannelBinary]
GreenChannelBinary = [''.join(map(str, pix)) for pix in GreenChannelBinary]
GreenChannelBinary = [int(pix, 2) for pix in GreenChannelBinary]
BlueChannelBinary = [''.join(map(str, pix)) for pix in BlueChannelBinary]
BlueChannelBinary = [int(pix, 2) for pix in BlueChannelBinary]
```
Now we need to create 3 greyscale images and give them the values of each list, merge them and save the image:
```
newRedLayer = Image.new("RGB", size).convert('L')
newRedLayer.putdata(RedChannelBinary)
newGreenLayer = Image.new("RGB", size).convert('L')
newGreenLayer.putdata(GreenChannelBinary)
newBlueLayer = Image.new("RGB", size).convert('L')
newBlueLayer.putdata(BlueChannelBinary)

encipheredImage = Image.merge("RGB", (newRedLayer, newGreenLayer, newBlueLayer))
encipheredImage.save('secrettest1.png')
```

**During Decoding:**

We can now remove from each binary value the lsb and append one from the binary of the message.

(Since Pillow can only accept the position of a pixel in a tuple of(X,Y). The function'coordinates' is being used to turn the position of a pixel written as(1, 2, 3, ...) to (X,Y) notation using the pixel's value and the width of the image):
```
def coordinates(pixel): 
    width = encipheredImage.width
    coord = x, y = pixel%width, int(pixel/width)
    return coord

lsb = []
for value in index:
    if 'r' in value:
        redPix = int(value[:-1])
        redPixCoord = coordinates(redPix)
        redPix = encipheredImage.getpixel(redPixCoord)[0]
        redPixBinary = [format(redPix, '08b')]
        redPixBinary = [list(map(str, n)) for n in redPixBinary]
        redPixBinary = sum(redPixBinary, [])
        lsb.append(redPixBinary[-1])

    elif 'g' in value:
        greenPix = int(value[:-1])
        greenPixCoord = coordinates(greenPix)
        greenPix = encipheredImage.getpixel(greenPixCoord)[1]
        greenPixBinary = [format(greenPix, '08b')]
        greenPixBinary = [list(map(str, n)) for n in greenPixBinary]
        greenPixBinary = sum(greenPixBinary, [])
        lsb.append(greenPixBinary[-1])

    elif 'b' in value:
        bluePix = int(value[:-1])
        bluePixCoord = coordinates(bluePix)
        bluePix = encipheredImage.getpixel(bluePixCoord)[2]
        bluePixBinary = [format(bluePix, '08b')]
        bluePixBinary = [list(map(str, n)) for n in bluePixBinary]
        bluePixBinary = sum(bluePixBinary, [])
        lsb.append(bluePixBinary[-1])
```
## Text Decoding:

We retrive the bands from the image:
```
RedChannel = list(encipheredImage.getdata(band=0))
GreenChannel = list(encipheredImage.getdata(band=1))
BlueChannel = list(encipheredImage.getdata(band=2))
```

Using the string we created during the encoding, we can then decipher both the channel and the pixel where the binary of the message is stored.

We use a regular expression to break up the string into smaller pieces that are seperated by the channels and are written as 'r' for red, 'g' for green and 'b' for blue:
`index = [match for match in re.findall('[^rgb]+?[rgb]', key)]`

Then, using loops, we store the binary of the message from the lsb of each pixel in `lsb = []`:
```
lsb = []
for value in index:
    if 'r' in value:
        redPix = int(value[:-1])
        redPixCoord = coordinates(redPix)
        redPix = encipheredImage.getpixel(redPixCoord)[0]
        redPixBinary = [format(redPix, '08b')]
        redPixBinary = [list(map(str, n)) for n in redPixBinary]
        redPixBinary = sum(redPixBinary, [])
        lsb.append(redPixBinary[-1])

    elif 'g' in value:
        greenPix = int(value[:-1])
        greenPixCoord = coordinates(greenPix)
        greenPix = encipheredImage.getpixel(greenPixCoord)[1]
        greenPixBinary = [format(greenPix, '08b')]
        greenPixBinary = [list(map(str, n)) for n in greenPixBinary]
        greenPixBinary = sum(greenPixBinary, [])
        lsb.append(greenPixBinary[-1])

    elif 'b' in value:
        bluePix = int(value[:-1])
        bluePixCoord = coordinates(bluePix)
        bluePix = encipheredImage.getpixel(bluePixCoord)[2]
        bluePixBinary = [format(bluePix, '08b')]
        bluePixBinary = [list(map(str, n)) for n in bluePixBinary]
        bluePixBinary = sum(bluePixBinary, [])
        lsb.append(bluePixBinary[-1])
```

Now, we can take `lsb` and manipulate it to convert the binary to decimal and it to characters using `int(binary, 2)` and `chr(value)` and print out the message:
```
lsb = ''.join(lsb)
lsb = [lsb[i:i+8] for i in range(0, len(lsb), 8)]
HiddenMessage = [int(binary, 2) for binary in lsb]
HiddenMessage = [chr(value) for value in HiddenMessage]
HiddenMessage = ''.join(HiddenMessage)
print('Message:', HiddenMessage, sep="")
```

# Sources
Pillow Package - https://pypi.org/project/Pillow/
Pymongo Package - https://pypi.org/project/pymongo/
