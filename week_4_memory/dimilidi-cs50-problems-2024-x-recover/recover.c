#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

// Constants
#define BLOCK_SIZE 512

// Function prototypes
bool is_jpg_header(uint8_t buffer[]);

int main(int argc, char *argv[])
{
  // Accept a single command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    // Open the memory card
    FILE *card = fopen(argv[1], "r");

    // Create a buffer for a block of data
    uint8_t buffer[BLOCK_SIZE];

    // Initialize variables
    bool found_jpg = false;
    int counter = 0;
    char filename[9];
    FILE * img = NULL;

    // While there's still data left to read from the memory card
    while (fread(buffer, 1, BLOCK_SIZE, card) == BLOCK_SIZE)
    {
        // Check if the block indicats the start of a new jpg
        if (is_jpg_header(buffer))
        {
            // Close previoud jpg file if any
            if (img != NULL)
            {
                fclose(img);
            }

            // Create new jpg file
            // "&03i.jpeg" - format string; print integer with 3 digits
            sprintf(filename, "%03i.jpg", counter);
            img = fopen(filename, "w");
            counter++;
        }

        // Write the block to the current jpg file, if open
        if (img != NULL)
        {
            fwrite(buffer, sizeof(uint8_t), BLOCK_SIZE, img);
        }
    }

    // Close files
    fclose(img);
    fclose(card);
    return 0;
}

// Function to check if the block contains the start of a jpg
bool is_jpg_header(uint8_t buffer[])
{
    // look at the first 4 bits of thid 8 bits byte and set the remaining bits ot 0
    return buffer[0] == 0xff && buffer[1] == 0xd8  && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0;
}
