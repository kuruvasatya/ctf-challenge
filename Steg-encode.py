from PIL import Image
import binascii
import optparse
import codecs
import numpy as np


#Reformats rgb value of pixel into hexadecimal
def rgb2hex(r, g, b):
  return '#{:02x}{:02x}{:02x}'.format(r, g, b)
def hex2rgb(hexcode):
  if hexcode is None:
    return None
  return tuple(codecs.decode(hexcode[1:], 'hex'))
        

#encodes message into byte form and then turns message into binary while ignoring the '0b' value in the beginning
def str2bin(message):
  binary = bin(int(binascii.hexlify(message.encode()), 16))
  return binary[2:]
        

#replaces last value of the rgb hexcode with the binary count of the message
def encode(hexcode, digit):
  if(hexcode[-1] in ('0','1','2','3','4','5')):
    hexcode = hexcode[:-1] + digit
    return hexcode
  else:
    return None
                
                    
def hide(filename, message):
  img = Image.open(filename)
  binary = str2bin(message)
        #adds a breakpoint so we know where to stop
  binary = binary  + '1111111111111110'
        
        #check if img is avaialble in rgba and convert it just in case
  if img.mode in ('RGBA'):
    img = img.convert('RGBA')
    datas = img.getdata()
    print(datas)
				
    newData = []
    temp = ''
    count = 0
                
                #item corresponds to pixels
    for item in datas:
                        #if counts is less than the binary length, create a new pixel and using encode method replace with corresponding position in binary value 
      if(count < len(binary)):
        newpix = encode(rgb2hex(item[0], item[1], item[2]), binary[count])
                                
                                #if failed just add pixel to the newdata
        if newpix == None:
          newData.append(item)
                                #if success change new pixel to rgb and add it to new data
        else:
          r, g, b = hex2rgb(newpix)
          newData.append((r,g,b,255))
          count += 1
                        #if we finished the length of the binary then just add back the normal pixels
      else:
        newData.append(item)

                #add the new data to the image
    img.putdata(newData)
    img.save(filename, 'PNG')
    return 'COMPLETED!'
                
  else:
    return 'Incorrect image mode, could not hide.'
                
def Main():
  parser = optparse.OptionParser('usage %prog -e/-d/-i/-u <target file>')
  parser.add_option('-e', dest='hide', type='string', help='target picture path to hide text')
          
  (option, args) = parser.parse_args()

  if(option.hide != None):
    text = input("Enter a message to hide: ")
    print (hide(option.hide, text))
  else:
    print (parser.usage)
    exit(0)

if __name__ == '__main__':
        Main()
