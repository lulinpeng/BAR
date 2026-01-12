#define _GNU_SOURCE
#include <dlfcn.h> // dynamic link function
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

static time_t (*original_time)(time_t *t) = NULL;
static int (*original_rand)(void) = NULL;
static int (*original_srand)(unsigned int seed) = NULL;

// function called when library is loaded
__attribute__((constructor)) static void init() {
  printf("libintercept.so is loaded\n");
  original_time = dlsym(RTLD_NEXT, "time"); // get address of symbol
  printf("original time function address: time=%p,\n", original_time);
}

time_t time(time_t *t) {
  char *config = getenv("INTERCEPT");
  if (config) return 1672531200;
  return original_time(t);
}

int rand(void) { return 42; }

void srand(unsigned int seed) {
  printf("srand functon is called with parameter: seed = %u\n", seed);
  return;
}