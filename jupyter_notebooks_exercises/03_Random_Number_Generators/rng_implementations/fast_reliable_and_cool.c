#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

int main(int argc, char *argv[]) {

    FILE *outfile;
    char byte;

    if (argc == 3) {
        
        // process command line arguments
        outfile = fopen(argv[1], "wb");
        int n_bytes = atoi(argv[2]);

        // initialize LFSR variables
        uint16_t init = 0xbeef;
        uint16_t lfsr = init;
        uint16_t bit;

        // write random bytes to file
        for (int n = 0; n < n_bytes; n++) {
            for (int m = 0; m < 8; m++) {
                // polynomial: x^16 + x^14 + x^13 + x^11 + 1
                bit = ((lfsr >> 0) ^ (lfsr >> 2) ^ (lfsr >> 3) ^ (lfsr >> 5));
                lfsr = (lfsr >> 1) | (bit << 15);
            }
            byte = lfsr & 0xff;
            fwrite(&byte, 1, sizeof(byte), outfile);
        }
        
        fclose(outfile);
    }
    else {
        printf("Usage: %s <output-file> <number-of-rng-bytes>\n", argv[0]);
    }
   
    return 0;
}

