#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Take average of red, green, and blue
            int average_rgb = round((image[i][j].rgbtRed +  image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0);

            // Update pixel values
            image[i][j].rgbtRed = image[i][j].rgbtGreen = image[i][j].rgbtBlue = average_rgb;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    float sepiaRed, sepiaGreen, sepiaBlue;
    // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Compute sepia values
            sepiaRed = 0.393 * image[i][j].rgbtRed + 0.769 * image[i][j].rgbtGreen + 0.189 * image[i][j].rgbtBlue;
            sepiaGreen = 0.349 * image[i][j].rgbtRed  + 0.686 * image[i][j].rgbtGreen  + 0.168 * image[i][j].rgbtBlue;
            sepiaBlue = 0.272 * image[i][j].rgbtRed  + 0.534 * image[i][j].rgbtGreen  + 0.131 * image[i][j].rgbtBlue;

            sepiaRed = sepiaRed > 255 ? 255 : sepiaRed;

            // Update pixel with sepia values
            image[i][j].rgbtRed = sepiaRed > 255 ? 255 : round(sepiaRed);
            image[i][j].rgbtGreen = sepiaGreen > 255 ? 255 : round(sepiaGreen);
            image[i][j].rgbtBlue = sepiaBlue > 255 ? 255 : round(sepiaBlue);
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            // Swap pixels
             RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Create a copy of image
    RGBTRIPLE copy[height][width];

    // Loop through each pixel
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Initialize sums and pixel count
            float r_sum = 0, g_sum = 0, b_sum = 0, total_px = 0;

            // Loop through the 3x3 grid around the pixel
            for (int new_i = i - 1; new_i < i + 2; new_i++)
            {
                for (int new_j = j - 1; new_j < j + 2; new_j++)
                {
                    // Check for valid neighbouring pixel
                    if (new_i >= 0 && new_j >= 0 && new_i < height && new_j < width)
                    {
                        r_sum += image[new_i][new_j].rgbtRed;
                        g_sum += image[new_i][new_j].rgbtGreen;
                        b_sum += image[new_i][new_j].rgbtBlue;
                        total_px++;
                    }
                }
            }
            // Compute blurred value and assign it to the copy
             copy[i][j].rgbtRed = round(r_sum / total_px);
             copy[i][j].rgbtGreen = round(g_sum / total_px);
             copy[i][j].rgbtBlue = round(b_sum / total_px);
        }
    }
    // Copy the blurred values back to the original values
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = copy[i][j];
        }
    }
    return;
}
