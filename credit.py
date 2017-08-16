import math
import cs50


def main():
    # get credit card number from user
    number = cs50.get_int("Number: ")

    if number > 0 and luhn_pass(number):
        print(card_type(number))
    else:
        print("INVALID")
    # do I need this in Python version?
    return 0    


def luhn_pass(n):
    sub = 0
    even_dig = 0
    while(n > 0):
        if even_dig == 0:
            sub += n % 10
            even_dig = 1
        else:
            sub += sum_digits((n % 10) * 2)
            even_dig = 0
        n = n // 10    
    return sub % 10 == 0

    
def num_digits(n):
    return math.ceil(math.log(n,10))
    
    
def sum_digits(n):
    sub = 0
    while n > 0:
        sub += n % 10
        n = n //10
    return sub


def card_type(n):
    if amex_match(n):
        return "AMEX"
    elif mastercard_match(n):
        return "MASTERCARD"
    elif visa_match(n):
        return "VISA"
    else:
        return "INVALID"

    
def amex_match(n):
    return num_digits(n) == 15 and (n // 10000000000000 == 34 or n // 10000000000000 == 37)


def visa_match(n):
    return (num_digits(n) == 13 or num_digits(n) == 16) and (n // 1000000000000000 == 4 or n // 1000000000000 == 4)    
    

def mastercard_match(n):
    return num_digits(n) == 16 and (n // 100000000000000 == 51 or n // 100000000000000 == 52
                                       or n // 100000000000000 == 53 or n // 100000000000000 == 54 or n // 100000000000000 == 55)    
    
    
if __name__ == "__main__":
    main()

