#include <iostream>
using namespace std;

#define LOG_INFO(msg) \
    std::cout << __TIME__ << " [INFO] " << __FILE__ << ":" << __LINE__ << " - " << msg << std::endl

int main()
{
    cout << "__FILE__ " << __FILE__ << endl;
    cout << "__FUNCTION__ " << __FUNCTION__ << endl;
    cout << "__PRETTY_FUNCTION__ " << __PRETTY_FUNCTION__ << endl;
    cout << "__LINE__ " << __LINE__ << endl;
    cout << "__DATE__ " << __DATE__ << endl;
    cout << "__TIME__ " << __TIME__ << endl;
    cout << "__TIMESTAMP__ " << __TIMESTAMP__ << endl;
    LOG_INFO("successfully");

    return 0;
}