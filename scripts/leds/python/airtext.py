#!/usr/bin/python

import time
import Adafruit_BBIO.GPIO as GPIO
from charmap import CHAR_MAP

def bb_led_on(quad):
    for i in range(4):
        GPIO.output("USR%d" % i, quad[i])

def bb_led_off():
    for i in range(4):
        GPIO.output("USR%d" % i, 0)

def reset_led(interval=0.2):
    for i in range(4):
        GPIO.output("USR%d" % i, GPIO.LOW)
    time.sleep(interval)

def bb_led_flash(quad):
    bb_led_on(quad)
    time.sleep(0.1)
    bb_led_off()

def led_display_text(text, interval):

    for i in range(4):
        GPIO.setup("USR%d" % i, GPIO.OUT)
    reset_led()

    text = text.strip()
    num_chars = len(text)
    char_interval = round(interval/float(num_chars), 2)
    # print ("Each char interval: {}s".format(char_interval))
    for next_char in text.upper():
        # Spaces are handled
        bitmap = CHAR_MAP.get(next_char)
        if not bitmap:
            print ("Character: '{}' is not defined".format(next_char))
            continue

        frame_interval = round(char_interval/(len(bitmap) + 1), 2)
        # print ("Each frame interval: {}s".format(frame_interval))
        for column in bitmap:
            bb_led_flash(column)
            time.sleep(frame_interval)
        # Gap between characters
        reset_led(frame_interval)

while True:
    t = 2
    led_display_text("HELLO", t)
    time.sleep(t)
