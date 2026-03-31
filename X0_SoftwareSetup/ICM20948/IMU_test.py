import sys                   # Used to `insert` things into `sys.path`
sys.path.insert(0, '/opt/')  # Look in `/opt` when `import`ing stuff
import ICM20948              # Finds `ICM20948.py` in `/opt`
import time                  # Provides `time.sleep`
import math                  # Provides `math.asin`, etc.
import numpy as np           # Provides `np.rad2deg`

print("\nSense HAT Test Program ...\n")

# Initialize connection to the sensor(s).
icm20948 = ICM20948.ICM20948()

# Initialize Mahony filter for tracking sensor attitude.
mahony_filter = ICM20948.MahonyFilter()

# Take baseline gyro reading
baseline_gyro, baseline_accel = icm20948.read_gyro_and_accel(num_readings=32)

# Keep looping infinitely until the script is interrupted
while True:
    try:
        time.sleep(0.1)  # Sleep between measurements (if desired)

        gyro, accel = icm20948.read_gyro_and_accel()  # Read from gyro + accelerometer
        mag = icm20948.read_mag(num_readings=8)       # Read from the magnetometer (noisy)

        # Subtract baseline (noise) from the gyro to figure out how much it rotated.
        gyro -= baseline_gyro

        # Update Mahony filter with latest sensor readings, yielding a new
        # sensor orientation (AHRS) estimate.
        q0, q1, q2, q3 = mahony_filter.update(gyro, accel, mag)

        # Convert quaternion orientation representation to Euler angles in degrees (easier to read).
        pitch = math.asin(-2 * q1 * q3 + 2 * q0* q2) * 57.3
        roll  = math.atan2(2 * q2 * q3 + 2 * q0 * q1, -2 * q1 * q1 - 2 * q2* q2 + 1) * 57.3
        yaw   = math.atan2(-2 * q1 * q2 - 2 * q0 * q3, 2 * q2 * q2 + 2 * q3 * q3 - 1) * 57.3

        gyro_deg = np.rad2deg(gyro)  # Show gyroscope in deg/sec (easier to read).

        # Print the values
        print("-------------------------------------------------------------")
        print(f"Eulers (deg):         Roll = {roll:10.2f}, Pitch = {pitch:10.2f}, Yaw = {yaw:10.2f}")
        print(f"Acceleration (m/s^2):    X = {accel[0]:10.2f},     Y = {accel[1]:10.2f},   Z = {accel[2]:10.2f}")
        print(f"Gyroscope (rad/s):       X = {gyro_deg[0]:10.2f},     Y = {gyro_deg[1]:10.2f},   Z = {gyro_deg[2]:10.2f}")
        print(f"Magnetometer (uT):       X = {mag[0]:10.2f},     Y = {mag[1]:10.2f},   Z = {mag[2]:10.2f}")

    # Ensure the infinite loop can be interrupted (e.g. with `Ctrl+C` in a terminal)
    except(KeyboardInterrupt):
        print("\n === INTERRUPTED ===")
        break
