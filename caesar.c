#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

char caesar_shift(char c, int n);

int main(int argc, string argv[])
{
    // Error if wrong number of inputs
    if (argc != 2)
    {
        printf("Usage: caesar k\n");
        return 1;
    }
    // Prompt user for input
    printf("plaintext:");
    string s = get_string();
    // encrypt with caesar cypher
    printf("ciphertext:");
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        printf("%c", caesar_shift(s[i], atoi(argv[1])));
    }
    printf("\n");
}

// maps letter and shift amount to new letter (mod alphabet), returns other characters without modification
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
