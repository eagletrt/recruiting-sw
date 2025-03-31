#include <stdio.h>
#include <iostream>

extern "C"{
    #include "fake_receiver.h"
}

int main(void){

    std::cout << "Welcome to Project 2" << std::endl;

    return 0;
}