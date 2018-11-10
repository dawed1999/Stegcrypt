from PIL import Image
import random
import re

#The text we want hide in the image and it's length in 8-bit binary:
message = input('Please enter the message:')
channelDataLength = len(message)*8

#Converting the text in "message" to binary:
text2binary = [format(ord(ch), '08b') for ch in message]
text2binary = [list(map(int, x)) for x in text2binary]
text2binary = sum(text2binary,[])


#The image, a tuple of it's dimensions and the amount of it's pixels:
carrier_image = Image.open('Jake.jpg')
size = width, height = carrier_image.size
pixelsInImage = width*height

#Declaring a function that gets a band of color from the image and turns it to a list with the bands bianry:
def ChannelBinary(channel):
    ChannelBinary = [format(pix, '08b') for pix in channel]
    ChannelBinary = [list(map(int, n)) for n in ChannelBinary]
    return ChannelBinary

#Retriving each band from the image and using the "ChannelBinary" function:
RedChannel = list(carrier_image.getdata(band=0))
RedChannelBinary = ChannelBinary(RedChannel)
GreenChannel = list(carrier_image.getdata(band=1))
GreenChannelBinary = ChannelBinary(GreenChannel)
BlueChannel = list(carrier_image.getdata(band=2))
BlueChannelBinary = ChannelBinary(BlueChannel)

#Creating two sets of lists. The first is a random number generator that selects a pixel and the second selects a random letter for the sub-channel.Then their combind and used to append the bits from "text2binary" to the modified RGB bands:
randomPixelList = random.sample(range(pixelsInImage), channelDataLength)
randomPixelList = [format(pixel ,'')for pixel in randomPixelList]
randomPixelList = [int(pixel)for pixel in randomPixelList]
randomChannelList = [random.choice('rgb') for _ in range(channelDataLength)]
combinedList = [[randomChannelList[n]] + [randomPixelList[n]] + [text2binary[n]] for n in range(channelDataLength)]

#A dictionary of the sub-channels and the replacment of the original LSB from"jake.jpg" with the binary from "message":
channels = {'r': RedChannelBinary, 'g': GreenChannelBinary, 'b': BlueChannelBinary}
for channel, pix, lsb in combinedList:
    channels[channel][pix].pop(-1)
    channels[channel][pix].append(lsb)

#Converting the moddified band values of each band from binary to decimal:
RedChannelBinary = [''.join(map(str, pix)) for pix in RedChannelBinary]
RedChannelBinary = [int(pix, 2) for pix in RedChannelBinary]
GreenChannelBinary = [''.join(map(str, pix)) for pix in GreenChannelBinary]
GreenChannelBinary = [int(pix, 2) for pix in GreenChannelBinary]
BlueChannelBinary = [''.join(map(str, pix)) for pix in BlueChannelBinary]
BlueChannelBinary = [int(pix, 2) for pix in BlueChannelBinary]

#Appending the the modified band lists to a new grayscale image to then merge them to an RGB image:
newRedLayer = Image.new("RGB", size).convert('L')
newRedLayer.putdata(RedChannelBinary)
newGreenLayer = Image.new("RGB", size).convert('L')
newGreenLayer.putdata(GreenChannelBinary)
newBlueLayer = Image.new("RGB", size).convert('L')
newBlueLayer.putdata(BlueChannelBinary)

#The new image:
encipheredImage = Image.merge("RGB", (newRedLayer, newGreenLayer, newBlueLayer))
encipheredImage.save('secrettest1.png')
#del encipheredImage

#A string used for decoding the encoded image:
randomPixelList = [str(pixel)for pixel in randomPixelList]
key = [[randomPixelList[(n)]] + [randomChannelList[n]] for n in range(channelDataLength)]
key = ''.join(''.join(n) for n in key)
print('Key:', key, '\n', sep="")
