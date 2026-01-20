#include <iostream>
#include <vector>
#include <zstd.h> 

void ZsdtCompress(std::vector<uint8_t> & out_bytes, const std::vector<uint8_t> & in_bytes, int compression_level = 1){
    auto start_time = std::chrono::high_resolution_clock::now();
    size_t buf_size = ZSTD_compressBound(in_bytes.size());
    std::cout << "buf size: " << buf_size << std::endl;
    out_bytes.resize(buf_size);
    size_t out_size = ZSTD_compress(out_bytes.data(), out_bytes.size(), in_bytes.data(), in_bytes.size(), compression_level);
    std::cout << "out size: " << out_size << std::endl;
    out_bytes.resize(out_size);
    auto interval = std::chrono::duration_cast<std::chrono::microseconds>(std::chrono::high_resolution_clock::now() - start_time).count();
    std::cout <<"Time elapsed: " << interval << " us" << std::endl;
    return;
}

void ZsdtDeompress(std::vector<uint8_t> & out_bytes, const std::vector<uint8_t> & in_bytes){
    auto start_time = std::chrono::high_resolution_clock::now();
    size_t buf_size = ZSTD_getDecompressedSize(in_bytes.data(), in_bytes.size());
    if (buf_size == 0) {
        std::cout << "zstd error: ZSTD_getDecompressedSize" << std::endl;
        return;
    }
    std::cout << "buf size: " << buf_size << std::endl;
    out_bytes.resize(buf_size);
    size_t out_size = ZSTD_decompress(out_bytes.data(), out_bytes.size(), in_bytes.data(), in_bytes.size());
    std::cout << "out size: " << out_size << std::endl;
    out_bytes.resize(out_size);
    auto interval = std::chrono::duration_cast<std::chrono::microseconds>(std::chrono::high_resolution_clock::now() - start_time).count();
    std::cout <<"Time elapsed: " << interval << " us" << std::endl;
    return;
}

int main(int argc, const char** argv)
{
    std::vector<uint8_t> a(100000);
    std::vector<uint8_t> b;
    ZsdtCompress(b, a);

    a.clear();
    ZsdtDeompress(a, b);

    return 0;
}
