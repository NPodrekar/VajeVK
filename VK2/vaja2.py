import os
def string_to_bits(data):
    bytes = ""
    for n in range(len(data)):
        bytes+='{0:08b}'.format(ord(data[n]))
    return bytes

def file_to_bits(file_path):
    try:
        with open(file_path, 'rb') as file:
            # Read the entire file content
            file_content = file.read()

            # Convert each byte to a binary string and concatenate them
            bits_string = ''.join(format(byte, '08b') for byte in file_content)

            return bits_string
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    


def rol(n, b):
    return ((n << b) | (n >> (32 - b))) & 0xffffffff    


def split2words(data):
    words = chunks(data, 32)
    w = [0]*80
    for n in range(0, 16):
        w[n] = int(words[n], 2)
    for i in range(16, 80):
        w[i] = rol((w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16]), 1)  
    return w


def chunks(podatki, dolzina_bloka):
    ### dopolnite funkcijo chunks, ki razbije podatke na bloke dolzine dolzina_bloka
    bloki = [podatki[i:i + dolzina_bloka] for i in range(0, len(podatki), dolzina_bloka)]
                                                        
    return bloki




def sha1(bytes):
    ####dopolnite
    
    bytes += '1' 
    originalLen = len(bytes)
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0
    
    while ((len(bytes)%512) !=448):
        bytes += '0'

    bytes += '{0:064b}'.format(originalLen-1)

    for c in chunks(bytes,512):
        w = split2words(c)
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
  
        for i in range(0, 80):
            if(0<=i<=19):
                k = 0x5A827999
                f = (b & c) | ((~b) & d)
            elif (20 <=i<=39):
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif (40 <=i<=59):
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            elif (60 <=i<=79):
                f = b ^ c ^ d
                k = 0xCA62C1D6

            T = rol(a, 5) + f + e + k + w[i] & 0xffffffff
            e = d
            d = c
            c = rol(b,30)
            b = a
            a = T

        h0 = h0 + a & 0xffffffff
        h1 = h1 + b & 0xffffffff
        h2 = h2 + c & 0xffffffff
        h3 = h3 + d & 0xffffffff
        h4 = h4 + e & 0xffffffff

    return '{:08x}{:08x}{:08x}{:08x}{:08x}'.format(h0,h1,h2,h3,h4)

bytes = string_to_bits("")
print(bytes)

print(sha1(bytes)) 
print(len(sha1(bytes)))

bytes = file_to_bits("Izpitna vprašanja Varkom2011.pdf")
print(sha1(bytes)) 

# PR WINDOWSU JE TREBA \ ZAMENJAT Z / NA NASLOVU
naslov = "C:/Users/npnik/OneDrive/Namizje"
for file in os.listdir(naslov):
     file_path = os.path.join(naslov, file)
     bytes = file_to_bits(file_path)
     if bytes is not None:
        print(sha1(bytes))

