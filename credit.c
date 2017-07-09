#include <cs50.h>
#include <stdio.h>
#include <math.h>

int num_digits(long long n);
int sum_digits(int n);
bool luhn_pass(long long n);
bool amex_match(long long n);
bool mastercard_match(long long n);
bool visa_match(long long n);
string card_type(long long n);

int main(void)
{
    printf("Number: ");
    long long number = get_long_long();
    if (number > 0 && luhn_pass(number)) {
        printf("%s", card_type(number));
    }
    else {
        printf("INVALID\n");
    }
}

bool luhn_pass(long long n)
{
    int sub = 0;
    int even_dig = 0;
    while (n > 0) {
        if (even_dig == 0) {
            sub += n % 10;
            even_dig = 1;
        }
        else {
            sub += sum_digits((n % 10) * 2);
            even_dig = 0;
        }
        n = n / 10;
    }
    return sub % 10 == 0;
}

string card_type(long long n)
{
    if (amex_match(n)) {
        return ("AMEX\n");
    }
    else if (mastercard_match(n)) {
        return ("MASTERCARD\n");
    }
    else if (visa_match(n)) {
        return ("VISA\n");
    }
    else {
        return ("INVALID\n");
    }
}

int sum_digits(int n)
{
    int sub = 0;
    while (n > 0) {
        sub += n % 10;
        n = n / 10;
    }
    return sub;
}

int num_digits(long long n)
{
    return ceil(log10(n));
}

bool amex_match(long long n)
{
    return (num_digits(n) == 15 && (n / 10000000000000 == 34 || n / 10000000000000 == 37));
}

bool visa_match(long long n)
{
    return ((num_digits(n) == 13 || num_digits(n) == 16) && (n / 1000000000000000 == 4 || n / 1000000000000 == 4));
}

bool mastercard_match(long long n)
{
    return (num_digits(n) == 16 && (n / 100000000000000 == 51 || n / 100000000000000 == 52
                                       || n / 100000000000000 == 53 || n / 100000000000000 == 54 || n / 100000000000000 == 55));
}