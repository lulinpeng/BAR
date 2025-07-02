#include "ckzg.h"
#include <assert.h>
#include <stdio.h>

void print_hex(const unsigned char *data, size_t len) {
  for (size_t i = 0; i < len; i++) printf("%02x ", data[i]);
  printf("\n");
}

int main(void) {
  /* Load kzg trust_setup */
  FILE *fp;
  fp = fopen("kzg_trust_setup.txt", "r");
  assert(fp != NULL);

  KZGSettings kzg_setup;
  C_KZG_RET ret = load_trusted_setup_file(&kzg_setup, fp, 0);
  assert(ret == C_KZG_OK);
  fclose(fp);

  /* execute kzg commitment on a Blob */
  Blob blob = {0, 1, 2, 3, 4, 6, 7};
  KZGCommitment kzg_commit;
  printf("kzg commitment size: %lu\n", sizeof(KZGCommitment));
  printf("kzg commitment: ");
  print_hex((unsigned char *)&kzg_commit, sizeof(KZGCommitment));
  ret = blob_to_kzg_commitment(&kzg_commit, &blob, &kzg_setup);
  uint32_t print_len = 16;
  printf("(the first %d bytes of) blob: ", print_len);
  print_hex((unsigned char *)&blob, print_len);
  printf("kzg commitment: ");
  print_hex((unsigned char *)&kzg_commit, sizeof(KZGCommitment));
  assert(ret == C_KZG_OK);

  /* free kzg trust_setup */
  free_trusted_setup(&kzg_setup);

  return 0;
}
