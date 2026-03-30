#!/usr/bin/env python3

import time
import smbus
import struct
import math
import numpy as np

# ICM20948: i2c addresses
I2C_ADD_ICM20948 = 0x68  # Accelerometer + Gyro
I2C_ADD_ICM20948_AK09916 = 0x0C  # Magnetometer, by AKM
I2C_ADD_ICM20948_AK09916_READ = 0x80  # Control flag (READ mode)
I2C_ADD_ICM20948_AK09916_WRITE = 0x00  # Control flag (WRITE mode)

# ICM20948: registers (see ICM-20948 Datasheet and Register Map)
#     - user bank 0 register
REG_ADD_WIA = 0x00  # Who I am (handshake)
REG_VAL_WIA = 0xEA  # Who I am (expected response)
REG_ADD_USER_CTRL = 0x03
REG_VAL_BIT_DMP_EN = 0x80
REG_VAL_BIT_FIFO_EN = 0x40
REG_VAL_BIT_I2C_MST_EN = 0x20
REG_VAL_BIT_I2C_IF_DIS = 0x10
REG_VAL_BIT_DMP_RST = 0x08
REG_VAL_BIT_DIAMOND_DMP_RST = 0x04
REG_ADD_PWR_MIGMT_1 = 0x06
REG_VAL_ALL_RGE_RESET = 0x80
REG_VAL_RUN_MODE = 0x01  # Non low-power mode
REG_ADD_LP_CONFIG = 0x05
REG_ADD_PWR_MGMT_1 = 0x06
REG_ADD_PWR_MGMT_2 = 0x07
REG_ADD_ACCEL_XOUT_H = 0x2D
REG_ADD_ACCEL_XOUT_L = 0x2E
REG_ADD_ACCEL_YOUT_H = 0x2F
REG_ADD_ACCEL_YOUT_L = 0x30
REG_ADD_ACCEL_ZOUT_H = 0x31
REG_ADD_ACCEL_ZOUT_L = 0x32
REG_ADD_GYRO_XOUT_H = 0x33
REG_ADD_GYRO_XOUT_L = 0x34
REG_ADD_GYRO_YOUT_H = 0x35
REG_ADD_GYRO_YOUT_L = 0x36
REG_ADD_GYRO_ZOUT_H = 0x37
REG_ADD_GYRO_ZOUT_L = 0x38
REG_ADD_EXT_SENS_DATA_00 = 0x3B
REG_ADD_REG_BANK_SEL = 0x7F  # Important: register bank select
REG_VAL_REG_BANK_0 = 0x00
REG_VAL_REG_BANK_1 = 0x10
REG_VAL_REG_BANK_2 = 0x20
REG_VAL_REG_BANK_3 = 0x30

# ICM20948: registers (cont.)
#     - user bank 1 register
#     - user bank 2 register
REG_ADD_GYRO_SMPLRT_DIV = 0x00
REG_ADD_GYRO_CONFIG_1 = 0x01
REG_VAL_BIT_GYRO_DLPCFG_2 = 0x10  # bit[5:3]
REG_VAL_BIT_GYRO_DLPCFG_4 = 0x20  # bit[5:3]
REG_VAL_BIT_GYRO_DLPCFG_6 = 0x30  # bit[5:3]
REG_VAL_BIT_GYRO_FS_250DPS = 0x00  # bit[2:1]
REG_VAL_BIT_GYRO_FS_500DPS = 0x02  # bit[2:1]
REG_VAL_BIT_GYRO_FS_1000DPS = 0x04  # bit[2:1]
REG_VAL_BIT_GYRO_FS_2000DPS = 0x06  # bit[2:1]
REG_VAL_BIT_GYRO_DLPF = 0x01  # bit[0]
REG_ADD_ACCEL_SMPLRT_DIV_2 = 0x11
REG_ADD_ACCEL_CONFIG = 0x14
REG_VAL_BIT_ACCEL_DLPCFG_2 = 0x10  # bit[5:3]
REG_VAL_BIT_ACCEL_DLPCFG_4 = 0x20  # bit[5:3]
REG_VAL_BIT_ACCEL_DLPCFG_6 = 0x30  # bit[5:3]
REG_VAL_BIT_ACCEL_FS_2g = 0x00  # bit[2:1]
REG_VAL_BIT_ACCEL_FS_4g = 0x02  # bit[2:1]
REG_VAL_BIT_ACCEL_FS_8g = 0x04  # bit[2:1]
REG_VAL_BIT_ACCEL_FS_16g = 0x06  # bit[2:1]
REG_VAL_BIT_ACCEL_DLPF = 0x01  # bit[0]

# ICM20948: registers (cont.)
#     - user bank 3 register
REG_ADD_I2C_SLV0_ADDR = 0x03
REG_ADD_I2C_SLV0_REG = 0x04
REG_ADD_I2C_SLV0_CTRL = 0x05
REG_VAL_BIT_SLV0_EN = 0x80
REG_VAL_BIT_MASK_LEN = 0x07
REG_ADD_I2C_SLV0_DO = 0x06
REG_ADD_I2C_SLV1_ADDR = 0x07
REG_ADD_I2C_SLV1_REG = 0x08
REG_ADD_I2C_SLV1_CTRL = 0x09
REG_ADD_I2C_SLV1_DO = 0x0A

# AK09916 magnetometer (MAG) registers
REG_ADD_MAG_WIA1 = 0x00
REG_VAL_MAG_WIA1 = 0x48
REG_ADD_MAG_WIA2 = 0x01
REG_VAL_MAG_WIA2 = 0x09
REG_ADD_MAG_ST2 = 0x10
REG_ADD_MAG_DATA = 0x11
REG_ADD_MAG_CNTL2 = 0x31
REG_VAL_MAG_MODE_PD = 0x00
REG_VAL_MAG_MODE_SM = 0x01
REG_VAL_MAG_MODE_10HZ = 0x02
REG_VAL_MAG_MODE_20HZ = 0x04
REG_VAL_MAG_MODE_50HZ = 0x05
REG_VAL_MAG_MODE_100HZ = 0x08
REG_VAL_MAG_MODE_ST = 0x10


# Represents a (connection to an) ICM20948
class ICM20948(object):

    # Initialize a connection to the ICM20948
    def __init__(self, address=I2C_ADD_ICM20948):
        self._address = address
        self._bus = smbus.SMBus(1)

        # Check connection to primary ICM20948 peripheral.
        #
        # - Initialization of the device multiple times after
        #   power on will result in a return error
        # - We can skip this detection by delaying it by 500
        #   milliseconds
        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_0)
        assert REG_VAL_WIA == self._read_byte(REG_ADD_WIA), "Cannot detect ICM20948 peripheral, is it plugged in?"

        time.sleep(0.5)

        # Setup device
        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_0)
        self._write_byte(REG_ADD_PWR_MIGMT_1, REG_VAL_ALL_RGE_RESET)
        time.sleep(0.1)
        self._write_byte(REG_ADD_PWR_MIGMT_1, REG_VAL_RUN_MODE)

        # Setup gyroscope
        #
        # - REG_ADD_GYRO_SMPLRT_DIV: Set the sample rate divider to 7, so that the
        #   gyro samples at 8x lower rate (around 138 hz = 1100/(1 + SMPLRT_DIV)).
        # - REG_VAL_BIT_GYRO_FS_1000DPS: Set sensitivity to 1000 degrees per second.
        # - REG_VAL_BIT_GYRO_DLPF: enable digital low-pass filter
        # - REG_VAL_BIT_GYRO_DLPCFG_6: Make low-pass filter to around 5-10hz, removing vibrations
        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_2)
        self._write_byte(REG_ADD_GYRO_SMPLRT_DIV, 0x07)
        self._write_byte(
            REG_ADD_GYRO_CONFIG_1,
            REG_VAL_BIT_GYRO_DLPCFG_6 | REG_VAL_BIT_GYRO_FS_1000DPS | REG_VAL_BIT_GYRO_DLPF
        )

        # Setup accelerometer
        #
        # - REG_ADD_ACCEL_SMPLRT_DIV_2: Set sample rate divider to 7, so that
        #   the accelerometer samples at 8x lower rate (around 141 hz = 1125/(1 + SMPLRT_DIV_2)).
        #   similar to gyroscope rate.
        # - REG_VAL_BIT_ACCEL_FS_2g: make sensor sensitivity +- 2g (i.e. 2x earth's gravity)
        # - REG_VAL_BIT_ACCEL_DLPF: enable digital low-pass filter
        # - REG_VAL_BIT_ACCEL_DLPCFG_6: Make low-pass filter to around 5-10hz, removing vibrations
        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_2)
        self._write_byte(REG_ADD_ACCEL_SMPLRT_DIV_2, 0x07)
        self._write_byte(
            REG_ADD_ACCEL_CONFIG,
            REG_VAL_BIT_ACCEL_DLPCFG_6 | REG_VAL_BIT_ACCEL_FS_2g | REG_VAL_BIT_ACCEL_DLPF
        )

        # Setup magnetometer
        #
        # - Perform Who I Am (WIA1) check
        # - Set frequency to 20HZ
        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_0)
        time.sleep(0.1)
        pu8data = self.read_from_AK09916(
            I2C_ADD_ICM20948_AK09916 | I2C_ADD_ICM20948_AK09916_READ,
            REG_ADD_MAG_WIA1,
            2
        )
        assert pu8data == [REG_VAL_MAG_WIA1, REG_VAL_MAG_WIA2], "Cannot detect AK09916 magnetometer (but could detect the ICM20948), connection/SenseHAT might be faulty!"
        self.write_to_AK09916(
            I2C_ADD_ICM20948_AK09916 | I2C_ADD_ICM20948_AK09916_WRITE,
            REG_ADD_MAG_CNTL2,
            REG_VAL_MAG_MODE_20HZ
        )

    # Reads the gyroscope and accelerometer and returns both of them in
    # a tuple as 3-element numpy arrays. The gyroscope's units are radians.
    # The accelerometer's units are m/s^2.
    def read_gyro_and_accel(self, num_readings=1):
        # Set bank for reading
        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_0)

        # Accumulate
        gyro = np.array([0.0, 0.0, 0.0])
        accel = np.array([0.0, 0.0, 0.0])
        for i in range(num_readings):
            data = self._read_block(REG_ADD_ACCEL_XOUT_H, 12)

            unpacked = struct.unpack(">6h", bytes(data))
            for j in range(3):
                accel[j] += unpacked[j]
                gyro[j] += unpacked[j + 3]

        # Reset bank to default state
        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_2)

        # Calculate means
        gyro /= num_readings
        accel /= num_readings

        # Convert raw gyro values into usable ones:
        #
        # - Divide by 32.8 to convert 16-bit integer range (-32768 to +32767) into
        #   the 1000 deg/sec range (-1000 to +1000). The units are then in degrees.
        # - Multiply by 0.0175 to convert degrees into radians, which is how most
        #   algorithms handle angles.
        gyro *= 0.01745329 / 32.8

        # Convert raw acceleration values into usable ones:
        #
        # - Divide it by 16384.0 to convert the 16-bit integer range (-32768 to +32767)
        #   into the g range (-2g to +2g). Dictated by `REG_VAL_BIT_ACCEL_FS_2g`.
        # - Multiply g value by 9.80665 to convert it into m/s^2 (SI units).
        accel *= 9.80665 / 16384.0

        return gyro, accel

    # Reads the magnetometer and returns the reading as 3-element numpy
    # array in microteslas (uT).
    def read_mag(self, num_readings=8):

        # Set magnetometer for reading
        counter = 20
        while counter > 0:
            time.sleep(0.01)
            pu8data = self.read_from_AK09916(
                I2C_ADD_ICM20948_AK09916 | I2C_ADD_ICM20948_AK09916_READ,
                REG_ADD_MAG_ST2,
                1)
            if (pu8data[0] & 0x01) != 0:
                break
            counter -= 1

        if counter == 0:
            raise RuntimeError("Error turning the magnetometer on: could be faulty?")

        # Accumulate readings
        mag = np.array([0.0, 0.0, 0.0])
        for i in range(num_readings):
            pu8data = self.read_from_AK09916(
                I2C_ADD_ICM20948_AK09916 | I2C_ADD_ICM20948_AK09916_READ,
                REG_ADD_MAG_DATA,
                6)
            unpacked = struct.unpack("<3h", bytes(pu8data))
            mag[0] += unpacked[0]
            mag[1] -= unpacked[1]
            mag[2] -= unpacked[2]

        # Calculate mean
        mag /= num_readings

        # Convert the raw signal into microteslas (uT), dictated by the
        # magnetometer's specification (see AK09916 datasheet).
        mag *= 0.15

        return mag

    def read_from_AK09916(self, u8I2CAddr, u8RegAddr, u8Len):
        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_3)  # Switch to bank3
        self._write_byte(REG_ADD_I2C_SLV0_ADDR, u8I2CAddr)
        self._write_byte(REG_ADD_I2C_SLV0_REG, u8RegAddr)
        self._write_byte(REG_ADD_I2C_SLV0_CTRL, REG_VAL_BIT_SLV0_EN | u8Len)

        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_0)  # Switch to bank0

        u8Temp = self._read_byte(REG_ADD_USER_CTRL)
        u8Temp |= REG_VAL_BIT_I2C_MST_EN
        self._write_byte(REG_ADD_USER_CTRL, u8Temp)
        time.sleep(0.01)
        u8Temp &= ~REG_VAL_BIT_I2C_MST_EN
        self._write_byte(REG_ADD_USER_CTRL, u8Temp)

        pu8data = [self._read_byte(REG_ADD_EXT_SENS_DATA_00 + i) for i in range(u8Len)]

        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_3)  # Switch to bank3

        u8Temp = self._read_byte(REG_ADD_I2C_SLV0_CTRL)
        u8Temp &= ~((REG_VAL_BIT_I2C_MST_EN) & (REG_VAL_BIT_MASK_LEN))
        self._write_byte(REG_ADD_I2C_SLV0_CTRL, u8Temp)

        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_0)  # Switch to bank0

        return pu8data

    def write_to_AK09916(self, u8I2CAddr, u8RegAddr, u8data):
        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_3)  # Switch to bank3
        self._write_byte(REG_ADD_I2C_SLV1_ADDR, u8I2CAddr)
        self._write_byte(REG_ADD_I2C_SLV1_REG, u8RegAddr)
        self._write_byte(REG_ADD_I2C_SLV1_DO, u8data)
        self._write_byte(REG_ADD_I2C_SLV1_CTRL, REG_VAL_BIT_SLV0_EN | 1)

        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_0)  # Switch to bank0

        u8Temp = self._read_byte(REG_ADD_USER_CTRL)
        u8Temp |= REG_VAL_BIT_I2C_MST_EN
        self._write_byte(REG_ADD_USER_CTRL, u8Temp)
        time.sleep(0.01)
        u8Temp &= ~REG_VAL_BIT_I2C_MST_EN
        self._write_byte(REG_ADD_USER_CTRL, u8Temp)

        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_3)  # Switch to bank3

        u8Temp = self._read_byte(REG_ADD_I2C_SLV0_CTRL)
        u8Temp &= ~((REG_VAL_BIT_I2C_MST_EN) & (REG_VAL_BIT_MASK_LEN))
        self._write_byte(REG_ADD_I2C_SLV0_CTRL, u8Temp)

        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_0)  # Switch to bank0

    def _read_byte(self, cmd):
        return self._bus.read_byte_data(self._address, cmd)

    def _read_block(self, reg, length=1):
        return self._bus.read_i2c_block_data(self._address, reg, length)

    def _write_byte(self, cmd, val):
        self._bus.write_byte_data(self._address, cmd, val)
        time.sleep(0.0001)


# Represents the state of a Mahony filter, which tracks the Attitude
# and Heading Reference System (AHRS) of the sensor by taking noisy
# readings (from the gyroscope, accelerometer, and magnetometer) and
# updating an internal quaternion over time with new readings.
class MahonyFilter:

    # Initializes a `MahonyFilter` that can be updated with the
    # sensor readings to provide an error-corrected AHRS.
    def __init__(self, initial_quaternion=np.array([1.0, 0.0, 0.0, 0.0])):
        self.quaternion = initial_quaternion

    # Updates this `MahonyFilter` with the latest readings from the
    # three sensors and returns the latest computed AHRS as a quaternion.
    def update(self, gyro, accel, mag):
        norm = 0.0
        gx, gy, gz = gyro
        ax, ay, az = accel
        mx, my, mz = mag
        hx = hy = hz = bx = bz = 0.0
        vx = vy = vz = wx = wy = wz = 0.0
        exInt = eyInt = ezInt = 0.0
        ex = ey = ez = 0.0
        halfT = 0.024
        q0, q1, q2, q3 = self.quaternion
        q0q0 = q0 * q0
        q0q1 = q0 * q1
        q0q2 = q0 * q2
        q0q3 = q0 * q3
        q1q1 = q1 * q1
        q1q2 = q1 * q2
        q1q3 = q1 * q3
        q2q2 = q2 * q2
        q2q3 = q2 * q3
        q3q3 = q3 * q3

        norm = float(1 / math.sqrt(ax * ax + ay * ay + az * az))
        ax = ax * norm
        ay = ay * norm
        az = az * norm

        norm = float(1 / math.sqrt(mx * mx + my * my + mz * mz))
        mx = mx * norm
        my = my * norm
        mz = mz * norm

        # compute reference direction of flux
        hx = 2 * mx * (0.5 - q2q2 - q3q3) + 2 * my * (q1q2 - q0q3) + 2 * mz * (q1q3 + q0q2)
        hy = 2 * mx * (q1q2 + q0q3) + 2 * my * (0.5 - q1q1 - q3q3) + 2 * mz * (q2q3 - q0q1)
        hz = 2 * mx * (q1q3 - q0q2) + 2 * my * (q2q3 + q0q1) + 2 * mz * (0.5 - q1q1 - q2q2)
        bx = math.sqrt((hx * hx) + (hy * hy))
        bz = hz

        # estimated direction of gravity and flux (v and w)
        vx = 2 * (q1q3 - q0q2)
        vy = 2 * (q0q1 + q2q3)
        vz = q0q0 - q1q1 - q2q2 + q3q3
        wx = 2 * bx * (0.5 - q2q2 - q3q3) + 2 * bz * (q1q3 - q0q2)
        wy = 2 * bx * (q1q2 - q0q3) + 2 * bz * (q0q1 + q2q3)
        wz = 2 * bx * (q0q2 + q1q3) + 2 * bz * (0.5 - q1q1 - q2q2)

        # error is sum of cross product between reference direction of fields and direction measured by sensors
        ex = (ay * vz - az * vy) + (my * wz - mz * wy)
        ey = (az * vx - ax * vz) + (mz * wx - mx * wz)
        ez = (ax * vy - ay * vx) + (mx * wy - my * wx)

        Ki = 1.0
        Kp = 4.50
        if (ex != 0.0 and ey != 0.0 and ez != 0.0):
            exInt = exInt + ex * Ki * halfT
            eyInt = eyInt + ey * Ki * halfT
            ezInt = ezInt + ez * Ki * halfT

            gx = gx + Kp * ex + exInt
            gy = gy + Kp * ey + eyInt
            gz = gz + Kp * ez + ezInt

        q0 = q0 + (-q1 * gx - q2 * gy - q3 * gz) * halfT
        q1 = q1 + (q0 * gx + q2 * gz - q3 * gy) * halfT
        q2 = q2 + (q0 * gy - q1 * gz + q3 * gx) * halfT
        q3 = q3 + (q0 * gz + q1 * gy - q2 * gx) * halfT

        norm = float(1 / math.sqrt(q0 * q0 + q1 * q1 + q2 * q2 + q3 * q3))
        q0 = q0 * norm
        q1 = q1 * norm
        q2 = q2 * norm
        q3 = q3 * norm

        self.quaternion = np.array([q0, q1, q2, q3])
        return self.quaternion.copy()
