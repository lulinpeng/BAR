#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

#include "blst.h"
#include "blst_aux.h"

std::string Bytes2HexStr(const std::vector<uint8_t> &bytes) {
  std::stringstream ss;
  ss << "0x";
  ss << std::hex << std::setfill('0');
  for (uint32_t i = 0; i < bytes.size(); ++i) ss << std::setw(2) << static_cast<int>(bytes[i]);
  return ss.str();
}

int main(void) {
  std::vector<uint8_t> msg(42);
  std::vector<uint8_t> hash(32);

  /* sha256 */
  blst_sha256(hash.data(), msg.data(), msg.size());
  std::cout << "msg: " << Bytes2HexStr(msg) << std::endl;
  std::cout << "hash: " << Bytes2HexStr(hash) << std::endl;

  /* void blst_keygen(blst_scalar *out_SK, const byte *IKM, size_t IKM_len, const byte *info DEFNULL, size_t info_len DEFNULL); */  
  blst_scalar sk; /* typedef struct { byte b[256/8]; } blst_scalar; */
  std::vector<uint8_t> IKM(32); // input key material
  blst_keygen(&sk, IKM.data(), IKM.size());
  std::vector<uint8_t> sk_bytes((uint8_t*)&sk, (uint8_t*)&sk + 256/8);
  std::cout << "sk: " << Bytes2HexStr(sk_bytes) << std::endl;

  /* void blst_sk_to_pk_in_g1(blst_p1 *out_pk, const blst_scalar *SK); */
  blst_p1 pk; /* typedef struct { blst_fp x, y, z; } blst_p1; typedef struct { limb_t l[384/8/sizeof(limb_t)]; } blst_fp; */
  blst_sk_to_pk_in_g1(&pk, &sk); // pk = g_1^{sk}

  return 0;
}
