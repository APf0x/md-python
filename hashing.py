'''
Library made by APf0x

distributed under the MIT licence
'''
# we need a mask because python does not like allocating 32 bits to functions so we make it allocate 32 bits
# careful because python variables are dynamic meaning that if not careful python might remove the mask after an poeration to save space
MASK = 0xFFFFFFFF
T = [
    0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee, 0xf57c0faf, 0x4787c62a,
    0xa8304613, 0xfd469501, 0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
    0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821, 0xf61e2562, 0xc040b340,
    0x265e5a51, 0xe9b6c7aa, 0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
    0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed, 0xa9e3e905, 0xfcefa3f8,
    0x676f02d9, 0x8d2a4c8a, 0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
    0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70, 0x289b7ec6, 0xeaa127fa,
    0xd4ef3085, 0x04881d05, 0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
    0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039, 0x655b59c3, 0x8f0ccc92,
    0xffeff47d, 0x85845dd1, 0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
    0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391
]

# the confusing names are just the constants for the hashing i wrote them here just so i didnt need to redefine them every single time, it a little bit more messy but its going to be faster

first_first = [i for i in range(16)]

first_second = [i for i in range(7,23,5)]*4 # i couldve done i%4 in the call function but this one is slightly faster

second_first = [(1+i*5)%16 for i in range(16)]

second_second = [5,9,14,20]*4

third_second = [4,11,16,23]*4

third_first = [(5+i*3)%16 for i in range(16)]

fourth_first = [(i*7)%16 for i in range(16)]

fourth_second = [6,10,15,21]*4

class Hash():


    def __init__(self, text):
        self.bytetext = bytearray(text.encode('utf-8'))

    @staticmethod
    def print_bytes(codice):
        b = codice
        hex_str = ' '.join(f'{byte:02x}' for byte in b)
        print(hex_str)


    def padding_len(self):
        zeros_needed = len(self.bytetext)
        zeros_needed = (55-zeros_needed)%64
        return (zeros_needed)
    
    def bit_64 (self):
        original_length_bits = len(self.bytetext) * 8
        length_64 = original_length_bits & 0xFFFFFFFFFFFFFFFF
        # to be honest idk if md5 workds on big or little endian imma just put little
        # figured out that it works only on little endian
        length_bytes = length_64.to_bytes(8, byteorder='little')

        return length_bytes

    def padding(self):
        #ok quindi a quanto pare se non fai [:] tu non stai facendo una copia ma stai creando tipo un pointer a self.text
        #è cosi stupida sta roba non capisco perche non crea una copia subito ma devo specificarlo io
        final = self.bytetext[:]
        final.extend(b'\x80'+b'\x00' * (self.padding_len()))
        final.extend(self.bit_64())
        return final
    
    @staticmethod
    def digest_first(X,Y,Z):
        return ((X & Y) | ((~X) & Z)) & MASK
    
    @staticmethod
    def digest_second(X,Y,Z):
        return  ((X & Z) | (Y & (~Z))) & MASK
    
    @staticmethod
    def digest_third(X,Y,Z):
        return (X ^ Y ^ Z) & MASK
    
    @staticmethod
    def digest_fourth(X,Y,Z):
        return (Y ^ (X | (~Z))) & MASK
    # why ad A if youre not going to ues it?
    # idk i saw it in one of the many frangmented tutorials

    # tnx chat gpt fuck python and his << function
    # nvm chat gpt you completely wrongly interpreted the md5 algorythms wasted 30 min of my life
    @staticmethod
    def leftrotate(x, n):
        x &= MASK
        return ((x << n) | (x >> (32 - n))) & MASK

    @staticmethod
    def digest_chunk(message_bit, A, B, C, D):
        AA = A & MASK
        BB = B & MASK
        CC = C & MASK
        DD = D & MASK

        digest_first = Hash.digest_first
        digest_second = Hash.digest_second
        digest_third = Hash.digest_third
        digest_fourth = Hash.digest_fourth

        leftrotate = Hash.leftrotate

        message_list = [int.from_bytes(message_bit[i:i+4], 'little') for i in range(0, 64, 4)]
        

        # first digest
        for i in range(16):
            A = B + leftrotate((A + digest_first(B,C,D)+ message_list[first_first[i]] + T[i]), first_second[i]) & MASK
            A, B, C, D = D, A, B, C

        # second digest
        for i in range(16):
            A = B + leftrotate((A + digest_second(B,C,D)+message_list[second_first[i]]+ T[i+16]), second_second[i] ) & MASK
            A, B, C, D = D, A, B, C
        
        # third digest
        for i in range(16):
            A = B + leftrotate((A + digest_third(B,C,D)+message_list[third_first[i]]+ T[i+32]), third_second[i]) & MASK
            A, B, C, D = D, A, B, C

        # fourth digest
        for i in range(16):
            A = B + leftrotate((A + digest_fourth(B,C,D)+message_list[fourth_first[i]]+T[i+48]), fourth_second[i]) & MASK
            A, B, C, D = D, A, B, C

        
        A = (A + AA) & MASK
        B = (B + BB) & MASK
        C = (C + CC) & MASK
        D = (D + DD) & MASK

        return A,B,C,D
    def master(self):
        A = 0x67452301 & MASK
        B = 0xEFCDAB89 & MASK
        C = 0x98BADCFE & MASK
        D = 0x10325476 & MASK
        final_message = self.padding()
        chunk_amount = len(final_message)//64 # we are going to divide it by 64 since we are diviging it by the amout of bytes not bits

        for i in range(0, chunk_amount):
            pos = i*64
            A,B,C,D = self.digest_chunk(final_message[pos:pos+64], A, B, C, D)
        

        digest = (
        A.to_bytes(4, byteorder='little') +
        B.to_bytes(4, byteorder='little') +
        C.to_bytes(4, byteorder='little') +
        D.to_bytes(4, byteorder='little')
        ).hex()

    
        return digest



if __name__ == "__main__":
    text = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    #print(Hash(text).print_bytes())
    
    #print(Hash(text).padding_len())
    #print(Hash(text).padding())
    print(Hash(text).master())
    print(Hash("a").master())
    print(Hash("abc").master())


