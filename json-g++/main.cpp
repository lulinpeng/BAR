#include <fstream>
#include <iostream>
#include <nlohmann/json.hpp>

int main() {
  std::ifstream f("example.json");
  try {
    nlohmann::json data = nlohmann::json::parse(f);
    std::string a = data["a"];

    uint32_t b = data["b"];
    std::string d = data["c"]["d"];
    uint32_t e = data["c"]["e"];
    std::cout << "a: " << a << ", b: " << b << ", d: " << d << ", e: " << e << std::endl;
    std::cout << data.dump(2) << std::endl;
  } catch (const nlohmann::json::parse_error &e) {
    std::cerr << "parse error: " << e.what() << std::endl;
    return 1;
  }
  return 0;
}
