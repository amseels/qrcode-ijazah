#include <quirc.h>
#include <iostream>
#include <fstream>
#include <quirc++/decoder.h>

using qr::decode;
using namespace std;

int main() {
    ifstream file("./resources/helloworld.dat", ios::binary | ios::in);
    if (!file) {
        cerr << "Could not open file\n";
        return 1;
    }
    const int width = 290;
    const int height = 290;
    uint8_t image[height * width];
    file.read(reinterpret_cast<char*>(image), width * height);

    auto results = decode(image, width, height);
    cout << "Found " << results.size() << " qr code(s) in image" << "\n";
    for (const auto& result: results) {
        cout << "==== Payload ====\n";
        for (auto byte: result.payload) {
            cout << static_cast<char>(byte);
        }
        cout << '\n';
    }

}
