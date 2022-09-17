#pragma once

// use this to define the lenght of message passed to can_receive
#define MAX_CAN_MESSAGE_SIZE 20

/**
 * @brief simulates opening CAN interface
 * 
 * @param filepath string containing path to the file
 * @return int 0 if ok, -1 if it couldn't open the file (probably wrong path)
 */
int open_can(const char* filepath);

/**
 * @brief simulates receiveing data from CAN interface, it is blocking with a random sleep.
 * 
 * @param message where the data will be setted
 * @return int -1 if there was an error reading CAN, else it returns the number of bytes read
 */
int can_receive(char message[MAX_CAN_MESSAGE_SIZE]);

/**
 * @brief closes the CAN interface
 * 
 */
void close_can();