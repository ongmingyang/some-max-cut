# The sources we're building
HEADERS = $(wildcard *.h)

CC := gcc
LDFLAGS = -lrt -lm -lcilkrts
CFLAGS = -std=gnu99 -Wall -O3 -fcilkplus -g

ifeq ($(DEBUG),1)
	CFLAGS += -DNDEBUG
endif

all: qubo

qubo: main.o graph.o matrix.o
	$(CC) $(CFLAGS) -o qubo $^ $(LDFLAGS)

%.o: %.c $(HEADERS)
	$(CC) $(CFLAGS) -o $@ -c $<

clean:
	rm -f *.o

