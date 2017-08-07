/**
 * Copies a BMP piece by piece, just because.
 */
       
#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: ./resize n infile outfile\n");
        return 1;
    }
    
    // remember resize amount
    int factor = atoi(argv[1]);
    
    if (factor < 1 || factor > 100)
    {
        fprintf(stderr, "n must be between 1 and 100\n");
        return 2;
    }

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];
    
    // open input file 
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 3;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 4;
    }

    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);
    

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);
    

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 || 
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 5;
    }
    
    // Copy fileheader to new variable
    BITMAPFILEHEADER r_bf = bf;

    // Copy infoheader to new variable    
    BITMAPINFOHEADER r_bi = bi;
    
    // New width, height
    r_bi.biWidth = factor * bi.biWidth;
    r_bi.biHeight = factor * bi.biHeight;
    
    
    // Determine padding for scanlines
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;    
    int r_padding = (4 - (r_bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    
    // new imagesize
    r_bi.biSizeImage = ((r_bi.biWidth * sizeof(RGBTRIPLE)) + r_padding) * abs(r_bi.biHeight);
    
    // New filesize
    r_bf.bfSize = sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER) + r_bi.biSizeImage;


    // write outfile's BITMAPFILEHEADER
    fwrite(&r_bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&r_bi, sizeof(BITMAPINFOHEADER), 1, outptr);


    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        // horizontal stretch
        for (int m = 0; m < factor; m++)
        {
            // iterate over pixels in scanline
            for (int j = 0; j < bi.biWidth; j++)
            {
                // temporary storage
                RGBTRIPLE triple;
    
                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
    
                // write RGB triple to outfile
                
                // horizontal stretch
                for (int k = 0; k < factor; k++)
                {
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                }
                
            }

            // Add padding to outputfile
            for (int l = 0; l < r_padding; l++)
            {
                fputc(0x00, outptr);
            }

            fseek(inptr, -((int) sizeof(RGBTRIPLE) * bi.biWidth), SEEK_CUR);
        }
        
        fseek(inptr, bi.biWidth * sizeof(RGBTRIPLE) + padding, SEEK_CUR);    
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
