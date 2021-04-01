#!/usr/bin/env python3

""" Este script desencripta un archivo .txt encriptado con el algoritmo AFIN x n """
""" Para invocarlo con bash la sintaxis es: $ ./encryptPage.py <file.txt> <a> <b> <xn (opcional)> """

from encryptAFINxn import *
import sys
import os
import re

# Ingresar el archivo como un argumento en bash
text_path = os.path.abspath( sys.argv[1] )

# Desencriptar por defecto en AFINx4 a menos que se indique lo contrario
if len(sys.argv) == 5:
    xn = int( sys.argv[4] )
else:
    xn = 4

# Abrir el archivo .txt y leerlo como una variable de tipo str
with open(text_path, 'r') as f:
    text_e = f.readlines()            #Leer el archivo por párrafos

# Quitar el caracter de salto de línea '\n'
encrypted_text = []
for paragraph in text_e:
    paragraph = paragraph[:-1]
    encrypted_text.append(paragraph)

print(encrypted_text)

''' INICIO DE ENCRIPCION '''

decrypt_par = []

# Por cada párrafo dividir los caracteres en grupos de tamaño xn
for par in encrypted_text:
    par_list = group_char(par, xn)
    decrypt_list = []

    # Por cada agrupacion del párrafo encriptar en AFINxn
    for grupo in par_list:
        d_n_grupo = decryptAFIN( chars_to_num(grupo), int(sys.argv[2]), int(sys.argv[3]), xn)
        d_grupo = num_to_chars(d_n_grupo, xn = xn) # Num desencriptado a caracteres del alfabeto
        decrypt_list.append(d_grupo)
    # Unir los desencriptados y ponerlos como un solo parrafo
    decrypt_par.append( ''.join(decrypt_list) + '\n')

decrypt_file_name = sys.argv[1]
decrypt_file_name = decrypt_file_name[: re.search(r'\.txt', decrypt_file_name).start()] + '_Decrypted.txt'
with open(decrypt_file_name, 'w') as f:
    f.writelines(decrypt_par)
