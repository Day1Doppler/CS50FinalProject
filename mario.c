#include <cs50.h>
#include <stdio.h>

void pyramid(int n);
void left_pyr(int row, int height);
void right_pyr(int row);

int main(void)
{
    int height;

    do {
        printf("Height: ");
        height = get_int();
    } while (height < 0 || height > 23);

    pyramid(height);
}

void pyramid(int n)
{
    for (int i = 0; i < n; i++) {
        left_pyr(i, n);
        printf("  ");
        right_pyr(i);
        printf("\n");
    }
}

void left_pyr(int row, int height)
{
    for (int i = 0; i < height; i++) {
        if (i + row + 1 < height) {
            printf(" ");
        }
        else {
            printf("#");
        }
    }
}

void right_pyr(int row)
{
    for (int i = 0; i <= row; i++) {
        printf("#");
    }
}