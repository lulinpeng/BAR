
#include <fstream>
#include <string>
using namespace std;
namespace Utils {
class Config {
public:
  bool secure;
  string address;
  string port;

public:
  Config(bool secure, string address, string port) {
    this->secure = secure;
    this->address = address;
    this->port = port;
  }
  void parse_args(int argc, char **argv) {
    for (int i = 1; i < argc; i++) {
      string arg = argv[i];
      if (arg == "-s" || arg == "--secure") {
        this->secure = true;
      } else if (arg == "-a" && i + 1 < argc) {
        this->address = argv[++i];
      } else if (arg == "-p" && i + 1 < argc) {
        this->port = argv[++i];
      }
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
}; // namespace Utils
