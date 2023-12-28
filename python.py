                    
                    # CALCULATOR IN PYTHON:

# ADDITION
# SUBTRACTION
# MULTIPLICATION
# DIVISION

print("select an operatin to perform:")
print("1 Add")
print("2 subtract")
print("3 multiply")
print("4 divide")


operation = input()
if operation == "1":
    num1 = input("enter the first number ")
    num2 = input("enter the second number ")
    #validation
    if(num1.isnumeric() and num2.isnumeric()):
        sum = int(num1) + int(num2)
        print("the sum of 2 numbers is " +str(sum))
    else:
        print("please type a valid number ")
elif operation == "2":
    num1 = input("enter the first number ")
    num2 = input("enter the secnd umber ")
    #validation
    if(num1.isnumeric() and num2.isnumeric()):
         sub = int(num1) - int(num2)
         print("the difference between 2 numbers is " +str(sub))
    else:
        print("please type a valid number")
elif operation == "3":
    num1 = input("enter the first number ")
    num2 = input("enter the second number ")
    #validation
    if(num1.isnumeric() and num2.isnumeric()):
        mul = int(num1) * int(num2)
        print("the multiplication of 2 values is " +str(mul))
    else:
        print("please type a valid number")
elif operation == "4":
    num1 = input("enter the first number ")
    num2 = input("enter the second number ")
    #validation
    if(num1.isnumeric() and num2.isnumeric()):
        div = int(num1) / int(num2)
        print("the division of 2 numbers is " +str(div))
    else:
        print("please type a valid number")
else:
    print("please enter a valid operation!")

    
    

    
    