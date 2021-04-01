#!/usr/bin/env python3

""" Este script encripta un archivo .txt con el algoritmo AFIN x n """
""" Para invocarlo con bash la sintaxis es: $ ./encryptPage.py <file.txt> <a> <b> <xn (opcional)> """

from encryptAFINxn import *
import sys
import os
import re

# Ingresar el archivo como un argumento en bash
text_path = os.path.abspath( sys.argv[1] )

# Encriptar por defecto en AFINx4 a menos que se indique lo contrario
if len(sys.argv) == 5:
    xn =int( sys.argv[4] )
else:
    xn = 4

# Abrir el archivo .txt y leerlo como una variable de tipo str
with open(text_path, 'r') as f:
    text_r = f.readlines()            #Leer el archivo por párrafos

#Por cada párrafo dejar solo el contenido literario
dicc_tildes = {'á':'a', 'é':'e', 'í':'i', 'ó':'o', 'ú':'u'}
signos_regex = r'[\¡\!\(\)\-\—\[\]\{\}\;\:\"\,\<\>\«\»\.\/\¿\?\@\#\$\%\^\&\*\_\~]'
puntuacion = '''¡!()-—[]{};:'"\,<>«»./¿?@#$%^&*_~'''
text = []
    # Quitar caracteres \n y \ufeff
for paragraph in text_r:
    # Lista de palabras del parrafo resultante
    p_parrafo = []

    paragraph = paragraph[ re.search(r'[A-Z]', paragraph).start() : -1]
    paragraph_words = paragraph.split()
    
    # Quitar caracteres que no hagan parte del diccionario por palabra
    for word in paragraph_words:
        word = word.lower()
        if ( ( not word[0].isalpha() ) or (word[0] in puntuacion)):
            primera_letra = re.search(r'[a-zñ]', word)
            if primera_letra != None:
                word = word[primera_letra.start():]
            else:
                continue
        for char in word:
            # Cambiar vocales con tildes
            if (char in dicc_tildes):
                tilde = re.search(r'[áéíóú]', word)
                if tilde != None:
                    word = word[:tilde.start()] + dicc_tildes[char] + word[tilde.start()+1:]
            # Quitar signos de puntuacion
            if (( not char.isalpha() ) or ( char in puntuacion )):
                signo_cerrar = re.search(signos_regex, word)
                if signo_cerrar != None:
                    word = word[:signo_cerrar.start()]
        # Agregar la palabra al parrafo
        p_parrafo.append(word)


    # Unir las palabras del parrafo y agregarlo a la liste 'text'
    parrafo = ' '.join(p_parrafo)
    text.append(parrafo)


print(text)

''' INICIO DE ENCRIPCION '''

encrypt_par = []

# Por cada párrafo dividir los caracteres en grupos de tamaño xn
for par in text:
    par_list = group_char(par, xn)
    encrypt_list = []

    # Por cada agrupacion del párrafo encriptar en AFINxn
    for grupo in par_list:
        e_n_grupo = encryptAFIN( chars_to_num(grupo), int(sys.argv[2]), int(sys.argv[3]), xn)
        e_grupo = num_to_chars(e_n_grupo, xn = xn) # Num encriptado a caracteres del alfabeto
        encrypt_list.append(e_grupo)
    # Unir los encriptados y ponerlos como un solo parrafo
    encrypt_par.append( ''.join(encrypt_list) + '\n')

encrypt_file_name = sys.argv[1]
encrypt_file_name = encrypt_file_name[: re.search(r'\.txt', encrypt_file_name).start()] + '_Encrypted.txt'
with open(encrypt_file_name, 'w') as f:
    f.writelines(encrypt_par)
