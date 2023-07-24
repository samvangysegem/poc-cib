#include "application.hpp"

// No logging available in main.cpp
int main(int argc, char *argv[]) {

    application newApp{};
    newApp.log_messages();

    return 0;
}