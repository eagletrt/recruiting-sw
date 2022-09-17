#include "fake_receiver.h"

#include <time.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

static int current_line_count = 0;
static int next_start_stop = 50;
static int start_or_stop = 0;
static int line_count = 0;
static int opened = 0;
static FILE* can = NULL;

int open_can(const char* filepath){
    if(opened == 1)
        return -1;

    can = fopen(filepath, "r");

    if(can == NULL)
        return -1;
    srand(time(NULL));
    opened = 1;

    char c;
    while((c = fgetc(can)) != EOF){
        if(c == '\n'){
            line_count ++;
        }
    }
    fseek(can, 0, SEEK_SET);

    return 0;
}

int can_receive(char message[MAX_CAN_MESSAGE_SIZE]){
    if(opened == 0)
        return -1;
    
    char c;
    int bytes_received = 0;
    memset(message, 0, strlen(message));

    if((current_line_count+1) % next_start_stop == 0){
        printf("\n\n%d, %d\n\n", next_start_stop, start_or_stop);
        if(start_or_stop == 0){      // start
            if(rand()%2 == 0){
                strcpy(message, "0A0#6601");
            }else{
                strcpy(message, "0A0#FF01");
            }
            start_or_stop = 1;
            next_start_stop = 400;
        }else{                      // stop
            strcpy(message, "0A0#66FF");
            start_or_stop = 0;
            next_start_stop = 100;
        }
        bytes_received = strlen(message);
        current_line_count ++;
        return bytes_received;
    }

    while((c = fgetc(can)) != EOF){
        if(c == '\n')
            break;
        message[bytes_received] = c;
        bytes_received ++;
    }

    if(bytes_received == 0)
        return -1;

    current_line_count ++;
    if(current_line_count == line_count)
        fseek(can, 0, SEEK_SET);
    
    usleep((rand()%50 + 1)*1000);

    return bytes_received;
}

void close_can(){
    if(opened == 0)
        return;

    if(can == NULL)
        return;
    
    fclose(can);
}