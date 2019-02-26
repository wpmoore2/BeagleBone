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
    def setup():
        for i in range(4):
            GPIO.setup("USR%d" % i, GPIO.OUT)

    @staticmethod
    def bb_led_flash(quad):
        LEDAPI.bb_led_on(quad)
        time.sleep(0.1)
        LEDAPI.bb_led_off()

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




DEFAULT_SHAKE_TIMEOUT = 3
ACCELEROMETER_READ_INTERVAL = 0.2
DEFAULT_SHAKE_THRESHOLD = 5

class AirtextShaker():

    def __init__(self):
        self.START = False
        self.start_lock = Lock()
        self.stop_thread = True
        self.finterval = 0

    #
    #   Method for accelerometer thread
    #
    def watch_accelerometer(self):
        acl = Accelerometer_MMA8452()
        xold, yold, zold = acl.get_ucoord()
        num_shakes = 0
        shake_timeout = DEFAULT_SHAKE_TIMEOUT
        while True:

            # Check to stop, and clean
            if self.stop_thread:
                LEDAPI.bb_led_off()
                acl.aclmeter._bus.close()
                print ("\nInterrupt Handled")
                exit(0)


            time.sleep(ACCELEROMETER_READ_INTERVAL)
            xnew, ynew, znew = acl.get_ucoord()
            xd = xnew - xold
            yd = ynew - yold
            zd = znew - zold
            xold, yold, zold = xnew, ynew, znew

            if xnew > 0:
                if xd > xnew:
                    # xold must of been negative
                    change_neg_2_pos_x = True
                elif xd > 0:
                    # xold positive but small than xnew
                    speedup_pos_x = True
                else:
                    # air text should always move, not speed up is slowdown
                    speedup_pos_x = False
            else:
                if xd < xnew:
                    # xold must of been positive
                    change_pos_2_neg_x = True
                if xd < 0:
                    # xold is negative and smaller than xnew
                    speedup_pos_x = True
                else:
                    speedup_pos_x = False

            absxd = abs(xd)
            factor = 0
            if absxd > 5:
                factor = 0.1
            elif absxd > 10:
                factor = 0.15
            elif absxd > 20:
                factor = 0.2
            elif absxd > 40:
                factor = 0.3


            if speedup_pos_x:
                # decrease interval, speedup flashes
                self.finterval = self.finterval*(1.0 - (factor*0.5))
            else:
                # increase interval
                self.finterval = self.finterval*(1.0 + factor)

            print (self.finterval)
            # print (xd)
            # print (xnew)
            # print ("\n\n")


            # Keep track of multiple rigorous shakes to start/stop
            shake_timeout -= ACCELEROMETER_READ_INTERVAL
            if shake_timeout <= 0:
                num_shakes = 0
            # Check for start/stop from 3 shakes
            if any(abs(val) > 150 for val in [xd, yd, zd]):
                # print ("X0: {} X1: {} diff: {}\nY0: {} Y1: {} diff: {}\nZ0: {} Z1: {}\n diff: {}\n".format(
                #         xold, xnew, xd, yold, ynew, yd, zold, znew, zd))
                shake_timeout = DEFAULT_SHAKE_TIMEOUT
                if num_shakes > DEFAULT_SHAKE_THRESHOLD:
                    num_shakes = 0
                    self.start_lock.acquire()
                    if self.START:
                        self.START = False
                    else:
                        self.START = True
                        print ("Go")
                    self.start_lock.release()
                else:
                    print ("shake: " + str(num_shakes))
                    num_shakes += 1

    def stop_current_thread(self):
        self.stop_thread = True

    def start_airtext(self, text, interval):

        # Setup LEDs for output
        LEDAPI.setup()

        # Determine how to spread led flashes based on string length and interval
        # Also serialize string in list of LED flashes - led_list
        text = text.strip()
        num_chars = len(text)
        led_list = LEDAPI.get_led_list(text)
        # Add a blank between each character. Divide time up accordingly
        length = len(led_list)
        init_frame_interval = round(float(interval)/length, 2)
        self.finterval = init_frame_interval
        print ("Initial frame Interval: {}".format(init_frame_interval))

        # Start accelerometer thread
        self.stop_thread = False
        acl_thread = Thread(target=self.watch_accelerometer)
        acl_thread.start()
        # self.START = True

        # Start/Stop LEDs based on accelerometer
        idx = 0
        while True:
            # Wait for START variable to be set
            while not self.START:
                print ("Wait")
                time.sleep(0.5)
            # Flash next frame
            LEDAPI.bb_led_flash(led_list[idx])
            time.sleep(self.finterval)
            idx += 1
            # Start back at beginning, but wait interval
            if idx >= length:
                print ("Wait {}s to restart".format(interval))
                time.sleep(interval)
                idx = 0


############################
# Start of execution
############################

import sys

string = "HELLO"
time_interval = 3
if len(sys.argv) > 2:
    string = sys.argv[1]
    time_interval = sys.argv[2]

try:
    airs = AirtextShaker()
    airs.start_airtext(string, time_interval)
except (KeyboardInterrupt, Exception):
    airs.stop_current_thread()
