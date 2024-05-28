# calculate BMI.. weight=150, height=1.6
from test1 import *
bmi(150,1.6)
odd(5)

# sp 

from test import *
sp(10000,1.5,6)


# assignment
# write a function to generate 6 random numbers eg.123456
import random
def generate_random_numbers(count=6):
    return [random.randint(1, 100) for _ in range(count)]
random_numbers = generate_random_numbers()
print(random_numbers)



# function to check if phone number is in correct format eg.+254789345234
import re

def is_valid_phone_number(phone_number):
    pattern = r'^\+254\d{9}$'
    if re.match(pattern, phone_number):
        return True
    return False

# Test the function
phone_number = "+254789345234"
print(is_valid_phone_number(phone_number))  # Should print: True

phone_number = "+25478934523"  # Incorrect length
print(is_valid_phone_number(phone_number))  # Should print: False

phone_number = "254789345234"  # Missing '+'
print(is_valid_phone_number(phone_number))  # Should print: False



