#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{
    // Ensure the program is executed with exactly one command-line argument
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // Check if the command-line argument is a digit
    for (int i = 0; argv[1][i] != '\0'; i++)
    {
        if (!isdigit(argv[1][i]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }

    // Convert the key to an integer
    int key = atoi(argv[1]);

    // Prompt user for plaintext
    string plaintext = get_string("plaintext:  ");

    // Encrypt the plaintext
    printf("ciphertext: ");
    for (int i = 0; i < strlen(plaintext); i++)
    {
        char c = plaintext[i];

        if (isupper(c))
        {
            // Rotate uppercase letters
            printf("%c", ((c - 'A' + key) % 26) + 'A');
        }
        else if (islower(c))
        {
            // Rotate lowercase letters
            printf("%c", ((c - 'a' + key) % 26) + 'a');
        }
        else
        {
            // Leave non-alphabetical characters unchanged
            printf("%c", c);
        }
    }

    // Print a newline at the end
    printf("\n");

    return 0;
}
