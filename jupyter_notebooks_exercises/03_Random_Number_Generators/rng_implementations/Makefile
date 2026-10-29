CC=gcc

SRC_FRAC=fast_reliable_and_cool.c
EXEC_FRAC=fast_reliable_and_cool

SRC_RSAU=rock_solid_as_usual.c
EXEC_RSAU=rock_solid_as_usual

SRC_YCCOM=you_can_count_on_me.c
EXEC_YCCOM=you_can_count_on_me

SRC_BRBE=best_random_base_ever.c
EXEC_BRBE=best_random_base_ever

all: frac rsau yccom brbe

frac: $(SRC_FRAC)
	$(CC) -o $(EXEC_FRAC) $(SRC_FRAC)

rsau: $(SRC_RSAU)
	$(CC) -o $(EXEC_RSAU) $(SRC_RSAU)

yccom: $(SRC_YCCOM)
	$(CC) -o $(EXEC_YCCOM) $(SRC_YCCOM)

brbe: $(SRC_BRBE)
	$(CC) -o $(EXEC_BRBE) $(SRC_BRBE)

clean:
	rm $(EXEC_FRAC) $(EXEC_RSAU) $(EXEC_YCCOM) $(EXEC_BRBE)

