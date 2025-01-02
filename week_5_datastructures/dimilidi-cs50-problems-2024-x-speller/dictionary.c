// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Variable to keep track of words_count
int words_count = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Hash word to obtain a hash value
    int hash_value = hash(word);

    // Access the linked list at that index of the hash table
    node *cursor = table[hash_value];

    // Traverse linked list, looking for the word
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    return toupper(word[0]) - 'A';
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open dictionary file
    FILE *file = fopen(dictionary, "r");
    // If no file found print message and exit
    if (file == NULL)
    {
        printf("Something went wrong by opening the file.\n");
        return false;
    }

    // Declare buffer with size equal to the length og the longest word in the dictionary to store
    // scanned strings from file
    char buffer[LENGTH];

    // Read strings from the file one at a time
    while (fscanf(file, "%s", buffer) != EOF)
    {
        // Create new node for each word
        node *new_word = malloc(sizeof(node));

        // Hash word to obtain a hash value
        int hash_value = hash(buffer);

        // Insert node into hash table
        strcpy(new_word->word, buffer);
        new_word->next = table[hash_value];
        table[hash_value] = new_word;

        words_count++;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return words_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // Iterate through the hash table (array of linked list)
    for (int i = 0; i < N; i++)
    {
        // Pointer to the current word
        node *temp = table[i];
        // Pointer to the next word
        node *cursor = table[i];

        // Iterate through linked list
        while (cursor != NULL)
        {
            cursor = cursor->next;
            free(temp);
            temp = cursor;
        }
    }
    return true;
}
