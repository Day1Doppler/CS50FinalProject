#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(void)
{
    // prompt user for input
    string s = get_string();

    // print and capitalize  first character in string if it is not a space
    if (s[0] != ' ')
    {
        printf("%c", toupper(s[0]));
    }
    // prints and capitalizes remaining elements of input if they are not spaces but are preceded by a space
    for (int i = 1, n = strlen(s); i < n; i++)
    {
        if (s[i-1] == ' ' && s[i] != ' ')
        {
            printf("%c", toupper(s[i]));
        }
    }
    // print newline
    printf("\n");
}

