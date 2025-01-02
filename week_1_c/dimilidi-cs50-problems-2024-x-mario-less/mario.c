#include <cs50.h>
#include <stdio.h>

void print_row(int spaces, int bricks);

int main(void)
{
    // Prompt the user for the pyramid's height
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (n < 1);

    // Print a pyramid of that height
    for (int i = n; i > 0; i--)
    {
        int spaces = i - 1;
        int bricks = n - spaces;
        print_row(spaces, bricks);
    }
}

// Function to print a row with the given number of spaces and bricks
void print_row(int spaces, int bricks)
{
    // Print spaces
    for (int j = 0; j < spaces; j++)
    {
        printf(" ");
    }

    // Print bricks
    for (int k = 0; k < bricks; k++)
    {
        printf("#");
    }

    // Move to the next line
    printf("\n");
}
