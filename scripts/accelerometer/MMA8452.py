#!/bin/python

import I2C

ACLMTR_ADDR = 0x1d
ACLMTR_X = 0x01
ACLMTR_Y = 0x03
ACLMTR_Z = 0x05


class Accelerometer_MMA8452():
    ''' I2C Wrapper for accelerometer of this particular model '''

    def __init__(self, addr=ACLMTR_ADDR):
        self.aclmeter = I2C.get_i2c_device(addr)

    def get_ux(self):
        return self.aclmeter.readS8(ACLMTR_X)
    def get_uy(self):
        return self.aclmeter.readS8(ACLMTR_Y)
    def get_uz(self):
        return self.aclmeter.readS8(ACLMTR_Z)

acl = Accelerometer_MMA8452()

print("X: {}".format(acl.get_ux()))
print("Y: {}".format(acl.get_uy()))
print("Z: {}".format(acl.get_uz()))
