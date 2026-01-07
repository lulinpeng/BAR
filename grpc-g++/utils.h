#include <fstream>
#include <iostream>
#include <string>
using namespace std;
namespace Utils {
class Config {
 public:
  bool secure;
  bool mutual_tls;
  bool enable_compression;
  string address;
  string port;

 public:
  Config(bool secure=false, bool mutual_tls=false, bool enable_compression=false, string address="0.0.0.0", string port="5000") {
    this->secure = secure;
    this->mutual_tls = mutual_tls;
    this->enable_compression = enable_compression;
    this->address = address;
    this->port = port;
  }

  void Print() { cout << "CONFIG: secure:" << secure << ", mutual_tls: " << mutual_tls << ", enable_compression: " << enable_compression << ", address: " << address << ", port: " << port << endl; }

  void parse_args(int argc, char **argv) {
    for (int i = 1; i < argc; i++) {
      string arg = argv[i];
      if (arg == "-s" || arg == "--secure")
        this->secure = true;
      else if (arg == "-d")
        this->mutual_tls = true;
      else if (arg == "-c")
        this->enable_compression = true;
      else if (arg == "-h" && i + 1 < argc)
        this->address = argv[++i];
      else if (arg == "-p" && i + 1 < argc)
        this->port = argv[++i];
    }
    return;
  }
};

std::string read_file(const std::string &filename) {
  std::ifstream file(filename);
  if (!file.is_open()) {
    throw std::runtime_error("can not open file: " + filename);
  }
  return std::string((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
}
};  // namespace Utils
