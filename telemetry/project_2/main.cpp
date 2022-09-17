#include <stdio.h>
#include <iostream>
using namespace std;

extern "C"{
    #include "fake_receiver.h"
}

int main(void){

    cout << "Welcome to Project 2" << endl;

    return 0;
}