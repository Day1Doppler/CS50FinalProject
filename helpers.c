/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */
 
#include <cs50.h>

#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 * Assumes array is sorted
 */
bool search(int value, int values[], int n)
{
    // Binary search algorithm
    if (n <= 0)
    {
        return false;
    }
    if (n == 1)
    {
        return values[0] == value;
    }
    if (values[n/2] == value)
    {
        return true;
    }
    else if (values[n/2] > value)
    {
        return search(value, values, n/2);
    }
    else
    {
        return search(value, values + n/2, (n + 1)/2);
    }
}

/**
 * Sorts array of n values.
 * Using bubblesort
 */
void sort(int values[], int n)
{
    if(n < 2)
    {
        return;
    }
    int swap_count;
    do 
    {
        swap_count = 0;
        for (int i = 0; i < n - 1; i++)
        {
            if (values[i] > values[i + 1])
            {
                int a = values[i];
                int b = values[i + 1];
                values[i] = b;
                values[i + 1] = a;
                swap_count = swap_count + 1;

            }
        }
    }
    while (swap_count != 0);
}
