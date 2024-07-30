// Scrie solutia in acest fisier
#include <iostream>

int main() {
    unsigned int x, y;
    std::cin >> x;
    std::cin >> y;

    int lastDigitSum = (x % 10 + y % 10) % 10;

    std::cout << lastDigitSum << std::endl;

}
