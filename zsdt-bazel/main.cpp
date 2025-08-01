#include <iostream>
#include <vector>
#include <zstd.h> 

void ZsdtCompress(std::vector<uint8_t> & out_bytes, const std::vector<uint8_t> & in_bytes, int compression_level = 1){
    size_t buf_size = ZSTD_compressBound(in_bytes.size());
    std::cout << "buf size: " << buf_size << std::endl;
    out_bytes.resize(buf_size);
    size_t out_size = ZSTD_compress(out_bytes.data(), out_bytes.size(), in_bytes.data(), in_bytes.size(), compression_level);
    std::cout << "out size: " << out_size << std::endl;
    out_bytes.resize(out_size);
    return;
}

int main(int argc, const char** argv)
{
    std::vector<uint8_t> in_bytes(100000);
    std::vector<uint8_t> out_bytes;
    ZsdtCompress(out_bytes, in_bytes);
    return 0;
}
