#include <iostream>
#include <windows.h>

int main() {
    HWND window = FindWindow(NULL, "Old School Runescape");
    if(!window) {
        std::cout << "window not found\n";
    }
    RECT rect;
    if(GetWindowRect(window, &rect)) {
        std::cout   << rect.right - rect.left << "," 
                    << rect.bottom - rect.top << "," 
                    << rect.left << "," 
                    << rect.top << "," 
                    << rect.right << "," 
                    << rect.bottom << "\n";
    }
    else {
        std::cout << "failed to retrieve window size" << "\n";
    }
    return 0;
}