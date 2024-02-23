# Importing necessary libraries 

import hashlib
import sys
import pyfiglet
import os
from colorama import Fore, Style
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Project Header
def Project():
    print(Fore.YELLOW + pyfiglet.figlet_format("Encryption and Decryption", font="slant") + Style.RESET_ALL)

# Printing Menu 
def menu():
    print("\n\n  Menu\n")
    print("\t 1. Encrypt")
    print("\t 2. Decrypt")
    print("\t 3. Exit")
    user = int(input())
    return user

#Exiting application
def Exit():
    print("Thank you for using the file encryptor")
    sys.exit(0)

#Encryption module 
def encryption():
    # Generating Randomly Initilization Vector
    def generateIV(length=16):
        return os.urandom(length)

    #Encrypting the File
    def encryptFile(file, IV, password):
        key = hashlib.sha256(password.encode()).digest()
        cipher = AES.new(key, AES.MODE_CBC, IV)
        with open(file, "rb") as f:
            data = f.read()
        paddedData = pad(data, AES.block_size)
        encryptedData = cipher.encrypt(paddedData)
        with open(file, "wb") as ef:
            ef.write(encryptedData)
        with open("IV_file.txt", "wb") as ivf:
            ivf.write(IV)

    #Taking input and error checking 
    file = input(Fore.YELLOW + "File to Encrypt:" + Style.RESET_ALL)
    if not os.path.isfile(file):
        sys.exit(Fore.RED + "\nError - File Not Found" + Style.RESET_ALL)
    if os.path.getsize(file) >= 52428800:
        sys.exit(Fore.RED + "Your File is Too Large. Max File Size is 50MB" + Style.RESET_ALL)

    password = input(Fore.YELLOW + "Choose a Strong Password:" + Style.RESET_ALL)
    
    #Calling modules 
    IV = generateIV()
    encryptFile(file, IV, password)
   
#Decrption module
def Decryption():

    #decrypting file
    def decrypt(file, password, IV):
        key = hashlib.sha256(password.encode()).digest()
        cipher = AES.new(key, AES.MODE_CBC, IV)
        with open(file, "rb") as f:
            data = f.read()
        decryptedData = cipher.decrypt(data)
        unpaddedData = unpad(decryptedData, AES.block_size)
        with open(file, "wb") as df:
            df.write(unpaddedData)

    #Taking input and error checking
    file = input(Fore.YELLOW + "File to Decrypt:" + Style.RESET_ALL)
    if not os.path.isfile(file):
        sys.exit(Fore.RED + "\nError - File Not Found" + Style.RESET_ALL)
    if os.path.getsize(file) >= 52428800:
        sys.exit(Fore.RED + "Your File is Too Large. Max File Size is 50MB" + Style.RESET_ALL)

    password = input(Fore.GREEN + "Enter Password used to Encrypt " + file + ": " + Style.RESET_ALL)
    ivfile_path = "IV_file.txt"
    if not os.path.isfile(ivfile_path):
        sys.exit(Fore.RED + "\nError - IV File Not Found" + Style.RESET_ALL)

    with open(ivfile_path, "rb") as ivf:
        IV = ivf.read()
    if len(IV) != 16:
        sys.exit(Fore.RED + "\nError - IV Length not correct, must be 16 bytes" + Style.RESET_ALL)
    #Calling module
    decrypt(file, password, IV)


#Running application
while True:
    Project()
    choice = menu()
    if choice == 1:
        encryption()
    elif choice == 2:
        Decryption()
    elif choice == 3:
        Exit()
