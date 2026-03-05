# Message Digest 5 in Python

this project was done in a little less than 4 days.

The goal was to code the MD5 hashing algorithm in python, without the aid of libraries, just to flex my skill on others.

The implementation was written from scratch by following the official specification described in [RFC 1321](https://www.rfc-editor.org/rfc/rfc1321).

# How MD5 works

md5 has 2 different phases unlike other tutorials might tell you.

1) Padding the message
2) Digesting the padded message

## Padding

Padding is the process of adding to a message of length N bits enough bits to reach a multiple of 512 bits, from there we have 2 more components.

first is the actual padding, second is the message length field, which is a 64 bit long number that indicates the length of the original message.

it looks like this

`[message]+[padding]+[message length field]`

The whole message has to be stored in little-endian format.

The padding is just to fill space in, the first value is a 1 and all the rest are 0s.

The message length field is a 64 bit long number that just entails the amount of bits in the original message.

When you are searching for the padding length you need to take in consideration 2 factors.

1) the padding must be at least one byte because the first byte must be 1, represented by the byte 0x80 followed by zeros
2) the message length parameter is always 64 bits, so you need to add 64 to the amount of bits in the message when youre fetching the padding length

An example

if he has 1000 bits and you search for the closest multiple of 512 it will find `1024` so 24 bits, you cant fit the 64 bit long message in the 24 bits available, idk why im explaining this but it might not be obvious to someone.

just do 1000+64 you'll find 1536 as closest multiple of 512 then you just fill it up with 0s.

## digest

[consult the original documentation - like i did - for more information](https://www.rfc-editor.org/rfc/rfc1321)

ok so once we did the padding in little endian - very important later on - well need to define the functions and constants that will actually hash the message.

first we have

A = 0x67452301

B = 0xEFCDAB89

C = 0x98BADCFE

D = 0x10325476

these might look like some very serious numbers as if they where chosen totally not random to hash all of your data they are indeed so mathematically perfect that when you reorder them into big endian you will get 0123456789abcdef, they did not try that hard.

then we will need to define the 4 following functions

>F(X,Y,Z) = (X AND Y) OR (NOT X AND Z)

>G(X,Y,Z) = XZ v Y not(Z)

>H(X,Y,Z) = X xor Y xor Z

>I(X,Y,Z) = Y xor (X v not(Z))

the operations are meant to be performed bitwise.

the message will get digested in 512 bit chunks and each chunk will be divided in 16 parts of which they will be up under 64 operations, 16 operations per every function that we just defined.

meaning that every part will be "hashed" 4 times

the exact formula for the digest is

a = b + ((a + F(b,c,d) + X[k] + T[i]) <<< s)

### **very important info while youre running this in a for loop you will need to change the values of ABCD between them like this**

### `A,B,C,D = B,C,D,A`

Where:

    a, b, c, d are the four 32‑bit registers (the current state).

    F is one of the non‑linear boolean functions (F, G, H, I) depending on the round.

    X[k] is the k‑th 32‑bit word of the message (one of the 16 words the 512‑bit chunk is divided into).

    T[i] is the i‑th predefined constant (derived from the sine function).

    <<< s is a left circular rotation by s bits.

    + is addition modulo 2³².

if you want to understand what k i s are they are arbitrary values they change during the 4 digests.

S is just a value that does from 1 to 64.

while K is a strange value that can be described only with maths.

the index k is defined as:

### digest 1

$\sum_{x=0}^{63} i$

### digest 2

$\sum_{x=0}^{63} (1 + 5i) \bmod 16$

### digest 3

$\sum_{x=0}^{63} (5 + 3i) \bmod 16$

### digest 4

$\sum_{x=0}^{63} (7i) \bmod 16$

if you dont know what $\sum_{x=0}^{63} i$ is its the same as writing `[i for i in range(64)]` in python

After processing each block, the new values are added to the old ones:

A = a + A

B = b + B

C = c + C

D = d + D

Then we move to the next 512‑bit block.

After the last block, the concatenation of A, B, C, D (in little‑endian order) is the final 128‑bit hash.

i dont feel like explaining it in detail anymore im tired so imma do it later.