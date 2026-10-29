#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

int main(int argc, char *argv[]) {

    FILE *outfile;
    FILE *urandom;
    char byte;

    if (argc == 3) {

        // open /dev/urandom for reading
        urandom = fopen("/dev/urandom", "rb");
        
        // process command line arguments
        outfile = fopen(argv[1], "wb");
        int n_bytes = atoi(argv[2]);
        
        // write random bytes to file
        for (int n = 0; n < n_bytes; n++) {
            fread(&byte, 1, sizeof(byte), urandom);
            fwrite(&byte, 1, sizeof(byte), outfile);
        }
        
        fclose(urandom);
        fclose(outfile);
    }
    else {
        printf("Usage: %s <output-file> <number-of-rng-bytes>\n", argv[0]);
    }
   
    return 0;
}

