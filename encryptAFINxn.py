#!/usr/bin/env python3

import math

def group_char(text: str, n: int = 4):
    # text is the string that is going to be split by groups of n char
    # n is the number of characters per agrupation, default is 4
    
    # check if the inserted values are valid
    assert type(text) == str, "text must be a string"
    assert type(n) == int, "n must be an integer"

    # if n is 0 or less, give it a value of len(text)
    if (n <= 0):
        raise ValueError('n value must be at least 1')
    
    #Check if the total length of the string is a multiple of n
    while (len(text) % n != 0):
        text += ' '                 # padding as spaces

    #group the string by n chars
    group_list = []
    for char_pos in range(0, len(text)-1, n):
        group_list.append(text[char_pos : char_pos+n])
    
    return group_list

def dict_clase():
    # Create the dictionary used in class
    letras = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'ñ', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ']

    indices = []
    for x in range(28):
        indices.append(x)

    dicc = dict(zip(letras, indices))
    return dicc

def chars_to_num(char_group: str, dicc: dict = dict_clase()):
    # Infer information to make de AFIN encryption
    x_n = len(char_group)-1         # size of char agrupation
    
    # Make the calculation from the formula
    num = 0
    for x in range( len(char_group) ):
        num += ( dicc[ char_group[x] ] * ( len(dicc)**x_n ) )
        if x_n != 0:
            x_n -= 1

    return num

def primos_relativos(n: int):
    # Relative primes from of a Z_n dictionary

    resultado = []
    for x in range(n):
        if math.gcd(x, n) == 1:
            resultado.append(x)
    return resultado

def encryptAFIN(num: int, a: int, b: int, xn: int = 4, dicc: dict = dict_clase()):
    # Encrypt the incoming number based on values a and b from AFIN algorithm
    # e(num) = ( (num*a)+b ) % len(dicc)**(len(group_char)) 
    # n is 28^4 by default

    if ( (type(a) != int) or (type(b) != int) ):
        raise TypeError('a and b must be integers')
    
    # check if a and b are valid for Z_n
    # a must be a relative prime and b < len(dicc)^n
    if (a not in primos_relativos( len(dicc)**xn ) ):
        raise ValueError('a must be a prime releative of Z_{}, inserted value = {}'.format(len(dicc)**xn, a))
    elif (b >= (len(dicc)**xn) ):
        raise ValueError('b must be less than {}, inserted value = {}'.format(len(dicc)**xn, b))

    e_num = ( (num*a) + b ) % ( len(dicc)**xn)

    return e_num

def GetKey(val: int, dicc: dict = dict_clase()):
    for key, value in dicc.items():
        if val == value:
            return str(key)
    if (val not in dicc.values()):
        raise ValueError('{} is not asigned to a character in the used dictionary'.format(val))

def num_to_chars(num: int, dicc: dict = dict_clase(), xn: int = 4):
    # Convert a number to its corresponding string of characters on a dictionary

    # Get the corresponding numeric code for each character on num
    result_str = ''
    if xn > 1:
        pol_grade = xn-1                              # Grade of the polinomy

        i_char = int( num / (len(dicc)**pol_grade) )  # Initial character
        result_str += GetKey(i_char)

        if xn > 2:                                    # Middle characters
            char_pos = 1
            while (char_pos < xn-1):
                char_code = int( ( num % (len(dicc)**pol_grade) ) / (len(dicc)**(pol_grade-1)) )
                result_str += GetKey(char_code)
                pol_grade -= 1
                char_pos += 1

    f_char = num % len(dicc)                           # Final character
    result_str += GetKey(f_char)

    return result_str

''' DECRYPT FUNCTIONS '''

def find_RP_inverse( a: int, xn: int = 4,dicc = dict_clase() ):
    # Function to find the inverse relative prime numbers of 'a' in Z_n
    
    rp_list = primos_relativos( len(dicc) ** xn ) 

    for RP in rp_list:
        if (a*RP)%(len(dicc)**xn) == 1:
            return RP
        
    raise ValueError( 'The given value of a ({}) is not a prime relative of Z_{}'.format(a, len(dicc)**xn) )

def decryptAFIN(num: int, a: int, b: int, xn: int = 4, dicc: dict = dict_clase() ):
    # From 'num' and having a^-1 and b, decrypt the incoming chars number

    # Find the inverse (a^-1) of the incoming relative prime 'a'
    inverse_a = find_RP_inverse(a, xn)
    
    d_num = ( (num - b) * inverse_a ) % ( len(dicc) ** xn)

    return d_num
