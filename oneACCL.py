'''
        Read Gyro and Accelerometer by Interfacing Raspberry Pi with MPU6050 using Python
	http://www.electronicwings.com
'''
import requests
import smbus			#import SMBus module of I2C
from time import sleep
import time          #import
from os import system, name
import csv

#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47
	
def clear():
 
    # for windows
    if name == 'nt':
        _ = system('cls')
 
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

def MPU_Init_Buses():
	#write to sample rate register
	bus_1.write_byte_data(Device_Address_1, SMPLRT_DIV, 7)
	
	#Write to power management register
	bus_1.write_byte_data(Device_Address_1, PWR_MGMT_1, 1)
	
	#Write to Configuration register
	bus_1.write_byte_data(Device_Address_1, CONFIG, 0)
	
	#Write to Gyro configuration register
	bus_1.write_byte_data(Device_Address_1, GYRO_CONFIG, 24)
	
	#Write to interrupt enable register
	bus_1.write_byte_data(Device_Address_1, INT_ENABLE, 1)

def read_raw_data(bus, device, addr):
	#Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(device, addr)
        low = bus.read_byte_data(device, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value

bus_1 = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
Device_Address_1 = 0x68   # MPU6050 device address

MPU_Init_Buses()

print (" Reading Data of Gyroscope and Accelerometer")
import time
start_time = time.time()
with open('oneCSV.csv', 'w') as f:
    thewriter = csv.writer(f)
    thewriter.writerow(['time', 'Ax', 'Ay', 'Az', 'Gx', 'Gy', 'Gz'])

    while True:

	#Read Accelerometer raw value 1
	acc_x_1 = read_raw_data(bus_1, Device_Address_1, ACCEL_XOUT_H)
	acc_y_1 = read_raw_data(bus_1, Device_Address_1, ACCEL_YOUT_H)
	acc_z_1 = read_raw_data(bus_1, Device_Address_1, ACCEL_ZOUT_H)

	#Read Gyroscope raw value
	gyro_x_1 = read_raw_data(bus_1, Device_Address_1, GYRO_XOUT_H)
	gyro_y_1 = read_raw_data(bus_1, Device_Address_1, GYRO_YOUT_H)
	gyro_z_1 = read_raw_data(bus_1, Device_Address_1, GYRO_ZOUT_H)

	#Full scale range +/- 250 degree/C as per sensitivity scale factor
	Ax_1 = acc_x_1/16384.0
	Ay_1 = acc_y_1/16384.0
	Az_1 = acc_z_1/16384.0

	Gx_1 = gyro_x_1/131.0
	Gy_1 = gyro_y_1/131.0
	Gz_1 = gyro_z_1/131.0
	thewriter.writerow([time.time() - start_time, Ax_1, Ay_1, Az_1, Gx_1, Gy_1, Gz_1])
	#clear()
