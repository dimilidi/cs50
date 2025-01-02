#include <cs50.h>
#include <stdio.h>

int calc_coins(int cents, int coin);

typedef struct
{
    char name[20];
    int value;
} Coin;

int main(void)
{
    // Initialize an array of coins
    Coin coins[] = {{"quarter", 25}, {"dime", 10}, {"nickel", 5}, {"penny", 1}};

    // Size of the coins array
    int num_coins = sizeof(coins) / sizeof(coins[0]);

    // Prompt the user for change owed, in cents
    int cents;
    do
    {
        cents = get_int("Change owed: ");
    }
    while (cents < 0);

    int totalCoins = 0;

    // Calculate the number of coins for each denomination
    for (int i = 0; i < num_coins; i++)
    {
        // Calculate how many coins you should give customer
        int coinCount = calc_coins(cents, coins[i].value);
        // Subtract the value of those coins from remaining cents
        cents -= coinCount * coins[i].value;
        // Sum the number of quarters, dimes, nickels, and pennies used
        totalCoins += coinCount;
    }

    // Print that sum
    printf("%i\n", totalCoins);
}

int calc_coins(int cents, int coin)
{
    return cents / coin;
}
