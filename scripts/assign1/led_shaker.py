#!/bin/python

import time
from threading import Thread, Lock
import Adafruit_BBIO.GPIO as GPIO
from charmap import CHAR_MAP
from MMA8452 import Accelerometer_MMA8452

################
# LED API
################
class LEDAPI():

    @staticmethod
    def bb_led_on(quad):
        for i in range(4):
            GPIO.output("USR%d" % i, quad[i])

    @staticmethod
    def bb_led_off():
        for i in range(4):
            GPIO.output("USR%d" % i, GPIO.LOW)

    @staticmethod
    def get_led_list(text):
        led_list = []
        for next_char in text.upper():
            led_list.extend(CHAR_MAP[next_char])
            led_list.append([0,0,0,0])
        return led_list


class AirtextShaker():


    def __init__(self):
        self.START = False
        self.start_lock = Lock()
        self.stop_thread = True

    #
    #   Method for accelerometer thread
    #
    def watch_accelerometer(self):
        acl = Accelerometer_MMA8452()
        xold, yold, zold = acl.get_ucoord()
        while True:

            # Check to stop, and clean
            if self.stop_thread:
                LEDAPI.bb_led_off()
                acl.aclmeter._bus.close()
                print ("\nInterrupt Handled")
                exit(0)


            time.sleep(0.2)
            xnew, ynew, znew = acl.get_ucoord()
            xd = abs(xnew - xold)
            yd = abs(ynew - yold)
            zd = abs(znew - zold)
            xold, yold, zold = xnew, ynew, znew

            if any(val > 100 for val in [xd, yd, zd]):
                print ("X0: {} X1: {} diff: {}\nY0: {} Y1: {} diff: {}\nZ0: {} Z1: {}\n diff: {}\n".format(
                        xold, xnew, xd, yold, ynew, yd, zold, znew, zd))
                self.start_lock.acquire()
                if self.START:
                    self.START = False
                else:
                    self.START = True
                self.start_lock.release()

                print ("Start condition: {}".format(self.START))

    def stop_current_thread(self):
        self.stop_thread = True


    def start_airtext(self, text, interval):

        # Setup LEDs for output
        for i in range(4):
            GPIO.setup("USR%d" % i, GPIO.OUT)

        # Determine how to spread led flashes based on string length and interval
        # Also serialize string in list of LED flashes - led_list
        text = text.strip()
        num_chars = len(text)
        led_list = LEDAPI.get_led_list(text)
        # Add a blank between each character. Divide time up accordingly
        length = len(led_list)
        frame_interval = round(float(interval)/length, 2)
        print ("Frame Interval: {}".format(frame_interval))

        # Start accelerometer thread
        self.stop_thread = False
        acl_thread = Thread(target=self.watch_accelerometer)
        acl_thread.start()

        # Start/Stop LEDs based on accelerometer
        idx = 0
        while True:
            # Wait for START variable to be set
            while not self.START:
                print ("Wait")
                time.sleep(0.5)
            # Flash next frame
            print ("Go: {}".format(idx))
            LEDAPI.bb_led_on(led_list[idx])
            time.sleep(frame_interval)
            idx += 1
            # Start back at beginning, but wait interval
            if idx >= length:
                print ("Wait {}s to restart".format(interval))
                time.sleep(interval)
                idx = 0


############################
# Start of execution
############################

try:
    airs = AirtextShaker()
    airs.start_airtext("hello", 15)
except KeyboardInterrupt:
    airs.stop_current_thread()
