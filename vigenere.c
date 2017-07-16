#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

char caesar_shift(char c, int n);
bool only_letters(string s);


int main(int argc, string argv[])
{
    // Error if wrong number or type of inputs, end program
    if (argc != 2 || !only_letters(argv[1]))
    {
        printf("Usage: ./vigenere k\n");
        return 1;
    }
    // Prompt user for input to be encrypted
    printf("plaintext:");
    string s = get_string();
    
    // For each element of plaintext, apply caesar cypher based on corresponding vig letter (mod by len(vig) for unequal lengths)
    printf("ciphertext:");
    for (int i = 0, j = 0, n = strlen(s), m = strlen(argv[1]); i < n; i++)
    {
        if (isalpha(s[i]))
        {
            printf("%c", caesar_shift(s[i], toupper(argv[1][(i - j) % m]) - 65));
        }
        else
        {
            printf("%c", s[i]);
            j++;
        }
    }
    printf("\n");
}

// Shifts letters by int n, otherwise returns input
char caesar_shift(char c, int n)
{
    if (c >= 'a' && c <= 'z')
    {
        return ((c + n - 'a') % 26) + 'a';
    } 
    else if (c >= 'A' && c <= 'Z')
    {
        return ((c + n - 'A') % 26) + 'A';
    }
    else
    {
        return c;
    }
}

// Tests whether a given string contains only alphabetical characters
bool only_letters(string s)
{
    for (int i = 0, n = strlen(s); i < n; i++)
    {
    if (!isalpha(s[i]))
        {
            return false;
        }
    }
        return true;
}