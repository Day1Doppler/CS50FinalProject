#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>

#define BLOCK_LEN 512
#define FILE_SUFFIX 5
#define FILE_PREFIX 3

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }
    
    // remember image
    char *image = argv[1];
    
    // open image file
    FILE *inptr = fopen(image, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", image);
        return 2;
    }
    
    // temporary storage - allocate memory for 512 bytes
    unsigned char *buffer = malloc(BLOCK_LEN);
    
    // filename: prefix XXX, suffix jpg./0
    char *filename = malloc(FILE_PREFIX + FILE_SUFFIX);
    
    // counter for naming convention, flag for when to start copying
    int h = 0;
    bool found_first_jpg = false;

    // try to open output file
    FILE *outptr;
    
    // read file by 512 byte blocks until EOF (technically till can't read in block of 512)
    while (fread(buffer, BLOCK_LEN, 1, inptr) == 1)
    {
        // test if jpg header
        if (*(buffer) == 0xff && *(buffer + 1) == 0xd8 && *(buffer + 2) == 0xff && (*(buffer + 3) & 0xfe) == 0xe0)
        {
            // flip found jpg to true. Better style to only do this once but keep checking variable value?
            found_first_jpg = true;
            
            // send new file name to filename
            sprintf(filename, "%03d.jpg", h);
            
            // increment num jpgs counter
            h++;

            // change and try to open output file
            outptr = fopen(filename, "w");
            if (outptr == NULL)
            {
                fclose(inptr);
                fprintf(stderr, "Could not create %s.\n", filename);
                return 4;
            }
        }
        
        // write if after first jpg designation
        if(found_first_jpg)
        {
            fwrite(buffer, BLOCK_LEN, 1, outptr);
        }    
    }
    
    //close i/o files
    fclose(inptr);
    fclose(outptr);
    
    // free memory
    free(buffer);

    // success
    return 0;
}