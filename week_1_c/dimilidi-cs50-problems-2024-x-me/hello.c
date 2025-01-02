#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Prompt the user to enter their name and store it in the variable 'name'
    string name = get_string("What's your name? ");
    // Print a greeting message including the user's name
    // %s is a placeholder for the string 'name'
    printf("Hello, %s\n", name);
}
