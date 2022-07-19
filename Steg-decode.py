from PIL import Image
import binascii
import optparse
import codecs
import sys

def rgb2hex(r, g, b):
  return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def hex2rgb(hexcode):
        return tuple(map(ord,hexacode[1:].decode('hex')))
		
def bin2str(binary):
        try:
                binary = int(('0b' + binary), 2)
                message = binary.to_bytes((binary.bit_length() + 7) // 8, 'big').decode()
                return message
        except:
                print("Invalid image :( ")
                sys.exit()
		
def decode(hexcode):
        if hexcode[-1] in ('0', '1'):
                return hexcode[-1]
        else:
                return None
				
def retr(filename):
        img = Image.open(filename)
        binary = ''
        
        if img.mode in ('RGBA'):
                img = img.convert('RGBA')
                datas = img.getdata()
                
                for item in datas:
                        digit = decode(rgb2hex(item[0], item[1], item[2]))
                        if digit == None:
                                pass
                        else:
                                binary = binary + digit
                                if((binary[-16:]) == '1111111111111110'):
                                        return bin2str(binary[:-16])
                
                return bin2str(binary)
                
        else:
                return 'Incorrect image mode, could not retrieve.'
				
				
def secure():
        password = input("Enter the key: ")
        required = 'c87c538f2142e1be3f6ac8f69f1b4fb8c801d06819b3a2d49f57e9000887be10'
        if(password == required):
                print("Key Verified successfully")  
        else:
                print("Integrity check failed, looks like image is corrupted!")
                sys.exit()
                
           
def Main():
        parser = optparse.OptionParser('usage %prog -d <target file>') 
        parser.add_option('-d', dest='decode', type='string', help='target picture path to retrieve text')
       
        (option, args) = parser.parse_args()
        isLoggedIn = secure()
                      
        if(option.decode != None):
            print (retr(option.decode))
        
        else:
            print ()
            sys.exit()

if __name__ == '__main__':
        Main()
