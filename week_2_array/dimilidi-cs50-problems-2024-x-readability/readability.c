#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

// Function prototypes
int count_letters(string text);
int count_words(string text);
int count_sentences(string text);
int calculate_index(int letters, int words, int sentences);
void find_grade_level(int index);

int main(void)
{
    // Prompt the user for some text
    string text = get_string("Text: ");

    // Count letters, words, and sentences
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);

    // Compute the Coleman-Liau index
    int index = calculate_index(letters, words, sentences);

    // Print the grade level
    find_grade_level(index);
}

// Function to count the number of letters
int count_letters(string text)
{
    int count = 0;
    for (int i = 0; text[i] != '\0'; i++)
    {
        // Check if the character is a letter
        if (isalpha(text[i]))
        {
            count++;
        }
    }
    return count;
}

// Function to count the number of words
int count_words(string text)
{
    int count = 0;
    for (int i = 0; text[i] != '\0'; i++)
    {
        // Count spaces as word boundaries
        if (text[i] == ' ' || (i > 0 && text[i] == '\0'))
        {
            count++;
        }
    }
    return count + 1; // Add 1 for the last word
}

// Function to count the number of sentences
int count_sentences(string text)
{
    int count = 0;
    for (int i = 0; text[i] != '\0'; i++)
    {
        count += (text[i] == '.' || text[i] == '!' || text[i] == '?');
    }
    return count;
}

// Function to calculate the Coleman-Liau index
int calculate_index(int letters, int words, int sentences)
{
    // Average number of letters per 100 words
    float L = (letters * 100.0) / words;
    // Average number of sentences per 100 words
    float S = (sentences * 100.0) / words;
    return round(0.0588 * L - 0.296 * S - 15.8);
}

// Function to determine grade level
void find_grade_level(int index)
{
    string result;
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}
