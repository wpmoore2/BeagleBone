/** Simple I2C example to read the first address of a device in C
* Written by Derek Molloy for the book "Exploring BeagleBone: Tools and
* Techniques for Building with Embedded Linux" by John Wiley & Sons, 2014
* ISBN 9781118935125. Please see the file README.md in the repository root
* directory for copyright and GNU GPLv3 license information.            */

#include<stdio.h>
#include<fcntl.h>
#include<sys/ioctl.h>
#include<linux/i2c.h>
#include<linux/i2c-dev.h>

// Small macro to display value in hexadecimal with 2 places
#define DEVID       0x00
#define BUFFER_SIZE 7

int main(){
   int file, i;
   signed long int xa, ya, za;

   printf("Starting the test application\n");
   if((file=open("/dev/i2c-1", O_RDWR)) < 0){
      perror("failed to open the bus\n");
      return 1;
   }
   if(ioctl(file, I2C_SLAVE, 0x1d) < 0){
      perror("Failed to connect to the sensor\n");
      return 1;
   }
   char writeCtrlBuffer[2] = {0x2a, 0x09};
   if(write(file, writeCtrlBuffer, 2)!=2){
      perror("Failed to write to CTRL_REG1 register\n");
      return 1;
   }
   char readBuffer[1];
   if(read(file, readBuffer, BUFFER_SIZE)!=BUFFER_SIZE){
      perror("Failed to read in the buffer\n");
      return 1;
   }
   close(file);


   printf("The Device ID is: 0x%02x\n", readBuffer[DEVID]);
   printf ("Dumping all bytes:\n");
   for (i=0; i<BUFFER_SIZE; i++) {
      printf ("%02x ", readBuffer[i]);
   }
   printf ("\n");

   xa = (signed char) readBuffer[1];
   ya = (signed char) readBuffer[3];
   za = (signed char) readBuffer[5];

   printf ("X-acceleration: %d\nY-acceleration: %d\nZ-acceleration: %d\n", xa, ya, za);

   return 0;
}
