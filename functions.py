# generate 6 random number
# function defination,takes no arguments
def generate_random():
    import random 
 # random is used to generate random numbers and make random selection
    import string 
# provides a colection of string constance , digits ,letters
# initialize the size of string 
    N = 6
# N is set to six,specifies the length oof the string to be six
# genetare random strings 
    res = ''.join(random.choices(string.digits,k=N))
# ''.join() it concatenates the random strigs to a single string 

# print the results
    print('The generated string is:'+ str(res))
    return str(res)

# generate_random()

# check phone validity 

import re 
# its a module which provides support for working with regular expressions
def check_phone(phone):
# the function take one argument phone
    regex ="^\+254\d{9}"
    # ^ it asserts the strat of the string 
    # \+254 it matches the literal string +254 
    # /d{9} it matches exactly 9 digits
    if not re.match(regex,phone) or len(phone) !=13: 
        print("phone is not valid")
        return False
    else:
        print("phone is valid,OK")
        return(True)
    
# check_phone("+254757776370")


# check password validity
import re
def passwordvalidity(password):
# check if password is less than 8
    if len(password) < 8:
        return("password is less than 8 characters")
    elif not re.search("[A-Z]",password):
        return("password must contain at least one uppercase letter")
    elif not re.search("[a-z]",password):
        return("password must contain at least one lowercase letter")
    elif not re.search("[0-9]",password):
        return("password must contain at least one digit")
    elif not re.search("[_@#$%!]",password):
        return("password must contain at least one special character")
    else :
        return True
# passwordvalidity(input("Enter your password: "))


# sending an sms
import africastalking
africastalking.initialize(
username="joe2022",
api_key="aab3047eb9ccfb3973f928d4ebdead9e60beb936b4d2838f7725c9cc165f0c8a"
#justpaste.it/1nua8
)
sms = africastalking.SMS

def send_sms (phone, message):
    recipients =[phone]
    sender = "AFRICASTALKING"
    try:
        response =sms.send(message,recipients)
        print(response)
    except Exception as error:
        print("Error is", error)
# send_sms("+254714338332","This is my message")


# hash password
import bcrypt 
# bcrypt its a module for hashing and cheking passwords
# its very secure

def hash_password(password):
    bytes = password.encode("utf-8")
    # password is encorded in to bytes
    # it is necessary becoz bcrypt library wors well with byte data 
    # print (bytes)
    salt = bcrypt.gensalt()
    # using a unique salt for each password ensures that even if two users have the same password , 
    # there hashed password will be diffrent
    # print(salt)
    hash = bcrypt.hashpw(bytes,salt)
    # print(hash)
    return hash.decode("utf-8")
# hash_password(input("Enter your password: "))
# verify password 
def hash_verify(password,hashed_password):
    bytes = password.encode("utf-8")
    result=bcrypt . checkpw(bytes, hashed_password.encode("utf-8"))
    print(result)
    return(result)

# hash_verify("12345678","$2b$12$cbU4TWDBTOtz2y5CLmXTFewcW7GwTRWfIwngvfcRuyAF9MUE1pYya")

# encrypt data 
from cryptography.fernet import Fernet
# we import fernet class 
# the module is used for encrypion and decryption
# we need to generate a key for encryption and decryption
# Fernet is a symmetric encryption algorithm that uses a 32-byte key to encrypt and decrypt data.
def gen_key ():
    # its a function that is used to generate a new encription key 
    key = Fernet.generate_key()
#     print(key)
# gen_key()
    with open("key.key","wb") as key_file:
    # with open its opens a new file if it exists
    # creates a new file if it dosent exist
    # wb-write binary is used to write binary ,ensures the file is properly closed after writing on it 
         key_file.write(key)
# gen_key()

# load key 
def load_key():
    return open ("key.key","rb").read()
# it reads the  entire content of the file
# load_key()

# encrypt data 

def encrypt (data):
    key =load_key()
    f = Fernet(key)
    # print (f)
    # this creates a fernet object for encryption
    encrypted_data = f.encrypt(data.encode())
    print(encrypted_data.decode())
    

# encrypt("1234")

# decrypt data
def decrypt (encrypted_data):
    key =load_key()
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data)
    print(decrypted_data.decode())

decrypt("gAAAAABmUEKZY7i-ntk8LwEL4npwrdgnLrBIjc6s8e98h8c0ONUlD0hZMou-9XqiSW_KZEgeT99RXgqRw-cuh9nXw4X2hg1KwA==")








    









