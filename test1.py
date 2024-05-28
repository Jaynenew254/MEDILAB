# functions with parameters
# add two numbers 
def add(x, y):
    add=x + y
    print (add) 
add(2,3)
add(60,90)

# bmi
def bmi(w, h):
    bmi=w/h*h
    print(bmi)

bmi(60,1)

# area

def area (p,r):
    area=p*r*r
    print(area)

area(3.14,7)

# function to get which number is greater than the other
def greater(a,b):
    if a>b:
        print(a,"is greater than",b)
    else:
        print(b,"is greater than",a)
greater(20,3)

# given 3 numbers which one  is greater 
def greater(a,b,c):
    if a>b and a>c:
        print(a,"is greater than",b,"and",c)
    elif b>c:
        print(b,"is greater than",a,"and",c)

    else:
        print(c,"is greater than",a,"and",b)
greater(20,30,40)



# write a function to check if a number is odd

def odd(a):
    if a%2==0:
        print(a,"is odd")
odd(2)


def even(a):
    if a%2!=0:
        print(a,"is even")
even(2)
        













