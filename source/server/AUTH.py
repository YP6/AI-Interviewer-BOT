
from .models import yp6AuthenticationToken, User
from django.utils import timezone
from cryptography.fernet import Fernet
import hashlib


def CheckAuthorization(request):
    try:
        tokenData = yp6AuthenticationToken.objects.get(token = request.headers['Authorization'])
        if tokenData.expiry < timezone.now():
            tokenData.delete()
            return False

        if not (request.user.username == tokenData.userID.username):
            return False

        if not (request.headers["MAC"] == tokenData.macAddress):
            return False
    except:
        return False

    tokenData.expiry = timezone.now() + timezone.timedelta(days=7)
    tokenData.save()
    return True


def RemoveAuthorization(request):
    try:
        tokenData = yp6AuthenticationToken.objects.get(token = request.headers['Authorization'])

        if not (request.user.username == tokenData.userID.username):
            return False

        if not (request.headers["MAC"] == tokenData.macAddress):
            return False
    except:
        return False
    
    tokenData.delete()
    return True




def write_key():
    # """
    # notes*
    # 1- this function used one time
    # 2- key is already saved in file after this function
    # 3- we will use this key to decrypt Variables
    # """
    key = Fernet.generate_key()  # Generates the key
    with open("dfenck.key", "wb") as key_file:  # Opens the file the key is to be written to
        key_file.write(key)  # Writes the key


def load_key():
    # """
    # notes*
    # 1- this function used in each run.
    # 2- used only to read the file.
    # :return: The key will be used in (enc & dec)
    # """
    return open("dfenck.key", "rb").read()  # Opens the file, reads and returns the key stored in the file


def Hash(data):

    # Creating Salt
    salt = "6b521811193112801d690e4ed9fd6d46327b33c38ba5e037f9b765167ac3252a"
    # Adding salt at the last of the data
    data = data + salt
    # Encoding the data
    hashed = hashlib.sha256(data.encode(), usedforsecurity=True)
    # Returning the Hash
    return hashed.hexdigest()


def Encrypt(Var):
    # """
    # :param Var: the value which will be encrypted

    # notes*
    # 1- value must be string
    # 2- value must convert to bytes
    # 3- the key must keep save      //important
    # 4- we will use the key in decryption //important
    # 5- this function can encrypt same variable twice.

    # :return: token -> the same value but after encryption
    # """
    #Variable = bytes(Var, 'utf-8')
    Variable=Var.encode()
    token = f.encrypt(Variable)
    return token


def Decrypt(token):
    """
    :param token: the encrypted variable
    :return: decrypted variable
    """
    d = f.decrypt(token)
    return d.decode()


