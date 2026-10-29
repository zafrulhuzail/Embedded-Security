#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {

    FILE *outfile;
    char byte;

    if (argc == 3) {
        
        // process command line arguments
        outfile = fopen(argv[1], "wb");
        int n_bytes = atoi(argv[2]);
        
        // write random bytes to file
        for (int n = 0; n < n_bytes; n++) {
            if ((n % 2) == 0) {
                byte = 65 + (n*17 % 26);
            }
            else {
                byte = 97 + (n*19 % 26);
            }
            fwrite(&byte, 1, sizeof(byte), outfile);
        }
        
        fclose(outfile);
    }
    else {
        printf("Usage: %s <output-file> <number-of-rng-bytes>\n", argv[0]);
    }
   
    return 0;
}

