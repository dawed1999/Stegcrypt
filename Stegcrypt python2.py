from PIL import Image
import random
import re
import io

while True:
    print('Please select an operation:' '\n' '1. Encode' '\n' '2. Decode' '\n' '0. Exit program')
    option = raw_input('Input:')
    
    if option == '1':
        print('1')
        originalText = raw_input('Please enter the message:')
        channelDataLength = len(originalText)*8

        textBinary = [format(ord(ch), '08b') for ch in originalText]
        textBinary = [list(map(int, x)) for x in textBinary]
        textBinary = sum(textBinary,[])

        image_input = raw_input("Please input an image:")
        image = open(image_input, 'rb')
        carrierImage = Image.open(image)
        size = width, height = carrierImage.size
        pixelsInImage = width*height

        def ChannelBinary(channel):
            ChannelBinary = [format(pix, '08b') for pix in channel]
            ChannelBinary = [list(map(int, n)) for n in ChannelBinary]
            return ChannelBinary

        RedChannel = list(carrierImage.getdata(band=0))
        RedChannelBinary = ChannelBinary(RedChannel)
        GreenChannel = list(carrierImage.getdata(band=1))
        GreenChannelBinary = ChannelBinary(GreenChannel)
        BlueChannel = list(carrierImage.getdata(band=2))
        BlueChannelBinary = ChannelBinary(BlueChannel)

        randomPixelList = random.sample(range(pixelsInImage), channelDataLength)
        randomPixelList = [format(pixel ,'')for pixel in randomPixelList]
        randomPixelList = [int(pixel)for pixel in randomPixelList]
        randomChannelList = [random.choice('rgb') for _ in range(channelDataLength)]
        combinedList = [[randomChannelList[n]] + [randomPixelList[n]] + [textBinary[n]] for n in range(channelDataLength)]

        channels = {'r': RedChannelBinary, 'g': GreenChannelBinary, 'b': BlueChannelBinary}
        for channel, pix, lsb in combinedList:
            channels[channel][pix].pop(-1)
            channels[channel][pix].append(lsb)



        RedChannelBinary = [''.join(map(str, pix)) for pix in RedChannelBinary]
        RedChannelBinary = [int(pix, 2) for pix in RedChannelBinary]
        GreenChannelBinary = [''.join(map(str, pix)) for pix in GreenChannelBinary]
        GreenChannelBinary = [int(pix, 2) for pix in GreenChannelBinary]
        BlueChannelBinary = [''.join(map(str, pix)) for pix in BlueChannelBinary]
        BlueChannelBinary = [int(pix, 2) for pix in BlueChannelBinary]



        newRedLayer = Image.new("RGB", size).convert('L')
        newRedLayer.putdata(RedChannelBinary)
        newGreenLayer = Image.new("RGB", size).convert('L')
        newGreenLayer.putdata(GreenChannelBinary)
        newBlueLayer = Image.new("RGB", size).convert('L')
        newBlueLayer.putdata(BlueChannelBinary)

        encipheredImage = Image.merge("RGB", (newRedLayer, newGreenLayer, newBlueLayer))
        encipheredImage.save('secrettest1.png')
        del encipheredImage

        randomPixelList = [str(pixel)for pixel in randomPixelList]
        key = [[randomPixelList[(n)]] + [randomChannelList[n]] for n in range(channelDataLength)]
        key = ''.join(''.join(n) for n in key)
        print('Key:'+str(key)+'\n')



    elif option == '2':
        print('2')
        key = raw_input('Enter Key:')
        print("Please select an image:")
        image_input = raw_input("Please input an image:")
        image = open(image_input, 'rb')
        encipheredImage = Image.open(image)

        RedChannel = list(encipheredImage.getdata(band=0))
        GreenChannel = list(encipheredImage.getdata(band=1))
        BlueChannel = list(encipheredImage.getdata(band=2))

        index = [match for match in re.findall('[^rgb]+?[rgb]', key)]

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

        lsb = ''.join(lsb)
        lsb = [lsb[i:i+8] for i in range(0, len(lsb), 8)]
        HiddenMessage = [int(binary, 2) for binary in lsb]
        HiddenMessage = [chr(value) for value in HiddenMessage]
        HiddenMessage = ''.join(HiddenMessage)
        print('Message:'+str(HiddenMessage))



    elif option == '0':
        exit()
        
    else:
        print('Invalid input, Please try again')
