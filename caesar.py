import sys
import cs50

def main():
    #  Error if wrong number of inputs
    if len(sys.argv) != 2:
        print("Usage: caesar k")
        return 1
    
    # Prompt user for input
    s = cs50.get_string("plaintext:")
    
    # calls encrypts and returns results
    print("cyphertext:" + caesar_cypher(s, sys.argv[1]))
    
    # need this?
    return 0
    
def caesar_cypher(string, amt):
    t = ""
    for i in range(len(string)):
        t = t + caesar_shift(string[i], int(amt))
    return t
    
def caesar_shift(char, amt):
    if char >= 'a' and char <= 'z':
        return chr(((ord(char) + amt - 97) % 26) + 97)
    elif char >= 'A' and char <= 'Z':
        return chr(((ord(char) + amt - 65) % 26) + 65)
    else:
        return char
        
if __name__ == "__main__":
    main()