'''
        Read Gyro and Accelerometer by Interfacing Raspberry Pi with MPU6050 using Python
	http://www.electronicwings.com
'''
import requests
import smbus			#import SMBus module of I2C
from time import sleep
import time          #import
from os import system, name

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

x_list_1 = []
y_list_1 = []
z_list_1 = []

x_list_2 = []
y_list_2 = []
z_list_2 = []

x_list_3 = []
y_list_3 = []
z_list_3 = []

x_list_4 = []
y_list_4 = []
z_list_4 = []

maxX_1 = -100000
maxY_1 = -100000
maxZ_1 = -100000

maxX_2 = -100000
maxY_2 = -100000
maxZ_2 = -100000

maxX_3 = -100000
maxY_3 = -100000
maxZ_3 = -100000

maxX_4 = -100000
maxY_4 = -100000
maxZ_4 = -100000

minX_1 = 100000
minY_1 = 100000
minZ_1 = 100000

minX_2 = 100000
minY_2 = 100000
minZ_2 = 100000

minX_3 = 100000
minY_3 = 100000
minZ_3 = 100000

minX_4 = 100000
minY_4 = 100000
minZ_4 = 100000

lastX_1 = 0
lastY_1 = 0
lastZ_1 = 0

lastX_2 = 0
lastY_2 = 0
lastZ_2 = 0

lastX_3 = 0
lastY_3 = 0
lastZ_3 = 0

lastX_4 = 0
lastY_4 = 0
lastZ_4 = 0

decisionsArray = []

def postreq(dat):
	url = 'https://swiftlykul1.herokuapp.com/graphql'
	
	timestamp = int(time.time()*1000.0)

	correct_payload = {'query': "mutation { sendCharacter (character:\"" + str(dat) +"\", timestamp: \""+ str(timestamp) + "\") { id } }"}

	# Output => You need to provide Username & password
	r = requests.post(url, json=correct_payload)
	print(r.text)	
	
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
        bus_1.write_byte_data(Device_Address_2, SMPLRT_DIV, 7)
        bus_2.write_byte_data(Device_Address_1, SMPLRT_DIV, 7)
        bus_2.write_byte_data(Device_Address_2, SMPLRT_DIV, 7)
	
	#Write to power management register
	bus_1.write_byte_data(Device_Address_1, PWR_MGMT_1, 1)
        bus_1.write_byte_data(Device_Address_2, PWR_MGMT_1, 1)
        bus_2.write_byte_data(Device_Address_1, PWR_MGMT_1, 1)
        bus_2.write_byte_data(Device_Address_2, PWR_MGMT_1, 1)
	
	#Write to Configuration register
	bus_1.write_byte_data(Device_Address_1, CONFIG, 0)
        bus_1.write_byte_data(Device_Address_2, CONFIG, 0)
        bus_2.write_byte_data(Device_Address_1, CONFIG, 0)
        bus_2.write_byte_data(Device_Address_2, CONFIG, 0)
	
	#Write to Gyro configuration register
	bus_1.write_byte_data(Device_Address_1, GYRO_CONFIG, 24)
        bus_1.write_byte_data(Device_Address_2, GYRO_CONFIG, 24)
        bus_2.write_byte_data(Device_Address_1, GYRO_CONFIG, 24)
        bus_2.write_byte_data(Device_Address_2, GYRO_CONFIG, 24)
	
	#Write to interrupt enable register
	bus_1.write_byte_data(Device_Address_1, INT_ENABLE, 1)
        bus_1.write_byte_data(Device_Address_2, INT_ENABLE, 1)
        bus_2.write_byte_data(Device_Address_1, INT_ENABLE, 1)
        bus_2.write_byte_data(Device_Address_2, INT_ENABLE, 1)

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
bus_2 = smbus.SMBus(5)
Device_Address_1 = 0x68   # MPU6050 device address
Device_Address_2 = 0x69

MPU_Init_Buses()

print (" Reading Data of Gyroscope and Accelerometer")

while True:
	
	#Read Accelerometer raw value 1
	acc_x_1 = read_raw_data(bus_1, Device_Address_1, ACCEL_XOUT_H)
	acc_y_1 = read_raw_data(bus_1, Device_Address_1, ACCEL_YOUT_H)
	acc_z_1 = read_raw_data(bus_1, Device_Address_1, ACCEL_ZOUT_H)
	
        #Read Accelerometer raw value 2
        acc_x_2 = read_raw_data(bus_1, Device_Address_2, ACCEL_XOUT_H)
        acc_y_2 = read_raw_data(bus_1, Device_Address_2, ACCEL_YOUT_H)
        acc_z_2 = read_raw_data(bus_1, Device_Address_2, ACCEL_ZOUT_H)

        #Read Accelerometer raw value
        acc_x_3 = read_raw_data(bus_2, Device_Address_1, ACCEL_XOUT_H)
        acc_y_3 = read_raw_data(bus_2, Device_Address_1, ACCEL_YOUT_H)
        acc_z_3 = read_raw_data(bus_2, Device_Address_1, ACCEL_ZOUT_H)

        #Read Accelerometer raw value
        acc_x_4 = read_raw_data(bus_2, Device_Address_2, ACCEL_XOUT_H)
        acc_y_4 = read_raw_data(bus_2, Device_Address_2, ACCEL_YOUT_H)
        acc_z_4 = read_raw_data(bus_2, Device_Address_2, ACCEL_ZOUT_H)

	#Read Gyroscope raw value
	gyro_x_1 = read_raw_data(bus_1, Device_Address_1, GYRO_XOUT_H)
	gyro_y_1 = read_raw_data(bus_1, Device_Address_1, GYRO_YOUT_H)
	gyro_z_1 = read_raw_data(bus_1, Device_Address_1, GYRO_ZOUT_H)

        gyro_x_2 = read_raw_data(bus_1, Device_Address_2, GYRO_XOUT_H)
        gyro_y_2 = read_raw_data(bus_1, Device_Address_2, GYRO_YOUT_H)
        gyro_z_2 = read_raw_data(bus_1, Device_Address_2, GYRO_ZOUT_H)

        gyro_x_3 = read_raw_data(bus_2, Device_Address_1, GYRO_XOUT_H)
        gyro_y_3 = read_raw_data(bus_2, Device_Address_1, GYRO_YOUT_H)
        gyro_z_3 = read_raw_data(bus_2, Device_Address_1, GYRO_ZOUT_H)

        gyro_x_4 = read_raw_data(bus_2, Device_Address_2, GYRO_XOUT_H)
        gyro_y_4 = read_raw_data(bus_2, Device_Address_2, GYRO_YOUT_H)
        gyro_z_4 = read_raw_data(bus_2, Device_Address_2, GYRO_ZOUT_H)

	#Full scale range +/- 250 degree/C as per sensitivity scale factor
	Ax_1 = acc_x_1/16384.0
	Ay_1 = acc_y_1/16384.0
	Az_1 = acc_z_1/16384.0

        Ax_2 = acc_x_2/16384.0
        Ay_2 = acc_y_2/16384.0
        Az_2 = acc_z_2/16384.0

        Ax_3 = acc_x_3/16384.0
        Ay_3 = acc_y_3/16384.0
        Az_3 = acc_z_3/16384.0

        Ax_4 = acc_x_4/16384.0
        Ay_4 = acc_y_4/16384.0
        Az_4 = acc_z_4/16384.0
	
	Gx_1 = gyro_x_1/131.0
	Gy_1 = gyro_y_1/131.0
	Gz_1 = gyro_z_1/131.0

        Gx_2 = gyro_x_2/131.0
        Gy_2 = gyro_y_2/131.0
        Gz_2 = gyro_z_2/131.0

        Gx_3 = gyro_x_3/131.0
        Gy_3 = gyro_y_3/131.0
        Gz_3 = gyro_z_3/131.0

        Gx_4 = gyro_x_4/131.0
        Gy_4 = gyro_y_4/131.0
        Gz_4 = gyro_z_4/131.0

	
	x_list_1.append(Gx_1)
	y_list_1.append(Gy_1)
	z_list_1.append(Gz_1)

        x_list_2.append(Gx_2)
        y_list_2.append(Gy_2)
        z_list_2.append(Gz_2)

        x_list_3.append(Gx_3)
        y_list_3.append(Gy_3)
        z_list_3.append(Gz_3)

        x_list_4.append(Gx_4)
        y_list_4.append(Gy_4)
        z_list_4.append(Gz_4)

	for elem in x_list_1:
		if(maxX_1 < elem):
			maxX_1 = elem
	for elem in y_list_1:
		if(maxY_1 < elem):
			maxY_1 = elem
	for elem in z_list_1:
		if(maxZ_1 < elem):
			maxZ_1 = elem

	for elem in x_list_1:
		if(minX_1 > elem):
			minX_1 = elem
	for elem in y_list_1:
		if(minY_1 > elem):
			minY_1 = elem
	for elem in z_list_1:
		if(minZ_1 > elem):
			minZ_1 = elem

        for elem in x_list_2:
                if(maxX_2 < elem):
                        maxX_2 = elem
        for elem in y_list_2:
                if(maxY_2 < elem):
                        maxY_2 = elem
        for elem in z_list_2:
                if(maxZ_2 < elem):
                        maxZ_2 = elem

        for elem in x_list_2:
                if(minX_2 > elem):
                        minX_2 = elem
        for elem in y_list_2:
                if(minY_2 > elem):
                        minY_2 = elem
        for elem in z_list_2:
                if(minZ_2 > elem):
                        minZ_2 = elem

        for elem in x_list_3:
                if(maxX_3 < elem):
                        maxX_3 = elem
        for elem in y_list_3:
                if(maxY_3 < elem):
                        maxY_3 = elem
        for elem in z_list_3:
                if(maxZ_3 < elem):
                        maxZ_3 = elem

        for elem in x_list_3:
                if(minX_3 > elem):
                        minX_3 = elem
        for elem in y_list_3:
                if(minY_3 > elem):
                        minY_3 = elem
        for elem in z_list_3:
                if(minZ_3 > elem):
                        minZ_3 = elem

        for elem in x_list_4:
                if(maxX_4 < elem):
                        maxX_4 = elem
        for elem in y_list_4:
                if(maxY_4 < elem):
                        maxY_4 = elem
        for elem in z_list_4:
                if(maxZ_4 < elem):
                        maxZ_4 = elem

        for elem in x_list_4:
                if(minX_4 > elem):
                        minX_4 = elem
        for elem in y_list_4:
                if(minY_4 > elem):
                        minY_4 = elem
        for elem in z_list_4:
                if(minZ_4 > elem):
                        minZ_4 = elem

	if(len(x_list_1) > 200):
		x_list_1.pop()

	if(len(y_list_1) > 200):
		y_list_1.pop()

	if(len(z_list_1) > 200):
		z_list_1.pop()

        if(len(x_list_2) > 200):
                x_list_2.pop()

        if(len(y_list_2) > 200):
                y_list_2.pop()

        if(len(z_list_2) > 200):
                z_list_2.pop()

        if(len(x_list_3) > 200):
                x_list_3.pop()

        if(len(y_list_3) > 200):
                y_list_3.pop()

        if(len(z_list_3) > 200):
                z_list_3.pop()

        if(len(x_list_4) > 200):
                x_list_4.pop()

        if(len(y_list_4) > 200):
                y_list_4.pop()

        if(len(z_list_4) > 200):
                z_list_4.pop()

	#print ("Gx=%.2f" %Gx, u'\u00b0'+ "/s", "\tGy=%.2f" %Gy, u'\u00b0'+ "/s", "\tGz=%.2f" %Gz, u'\u00b0'+ "/s", "\tAx=%.2f g" %Ax, "\tAy=%.2f g" %Ay, "\tAz=%.2f g" %Az) 	

	#print (lastX_1 - (maxX_1 - minX_1))
	#print (lastY_1 - (maxY_1 - minY_1))
	#print (lastZ_1 - (maxZ_1 - minZ_1))

        #print (lastX_2 - (maxX_2 - minX_2))
        #print (lastY_2 - (maxY_2 - minY_2))
        #print (lastZ_2 - (maxZ_2 - minZ_2))

        #print (lastX_3 - (maxX_3 - minX_3))
        #print (lastY_3 - (maxY_3 - minY_3))
        #print (lastZ_3 - (maxZ_3 - minZ_3))

        #print (lastX_4 - (maxX_4 - minX_4))
        #print (lastY_4 - (maxY_4 - minY_4))
        #print (lastZ_4 - (maxZ_4 - minZ_4))

	#print(len(z_list))

	test = []

	if ((maxX_1 - minX_1) != lastX_1 or (maxY_1 - minY_1) != lastY_1 or (maxZ_1 - minZ_1) != lastZ_1):
		test.append(abs(lastX_1 - (maxX_1 - minX_1)) + abs(lastY_1 - (maxY_1 - minY_1)) + abs(lastZ_1 - (maxZ_1 - minZ_1)))
	else:
		test.append(0)
		#print ("noMotion 1")

        if ((maxX_2 - minX_2) != lastX_2 or (maxY_2 - minY_2) != lastY_2 or (maxZ_2 - minZ_2) != lastZ_2):
                test.append(abs(lastX_2 - (maxX_2 - minX_2)) + abs(lastY_2 - (maxY_2 - minY_2)) + abs(lastZ_2 - (maxZ_2 - minZ_2)))
        else:
		test.append(0)
                #print ("noMotion 2")

        if ((maxX_3 - minX_3) != lastX_3 or (maxY_3 - minY_3) != lastY_3 or (maxZ_3 - minZ_3) != lastZ_3):
                test.append(abs(lastX_3 - (maxX_3 - minX_3)) + abs(lastY_3 - (maxY_3 - minY_3)) + abs(lastZ_3 - (maxZ_3 - minZ_3)))
        else:
		test.append(0)
                #print ("noMotion 3")

        if ((maxX_4 - minX_4) != lastX_4 or (maxY_4 - minY_4) != lastY_4 or (maxZ_4 - minZ_4) != lastZ_4):
                test.append(abs(lastX_4 - (maxX_4 - minX_4)) + abs(lastY_4 - (maxY_4 - minY_4)) + abs(lastZ_4 - (maxZ_4 - minZ_4)))
        else:
		test.append(0)
                #print ("noMotion 4")

	#print(test)

	num = 0

	char = 'N'

	if(test[0] > num):
		char = 'A'
		num = test[0]

        if(test[1] > num):
                char = 'B'
                num = test[1]

        if(test[2] > num):
                char = 'C'
                num = test[2]

        if(test[3] > num):
                char = 'D'

	decisionsArray.append(char)

	lastX_1 = (maxX_1 - minX_1)
	lastY_1 = (maxY_1 - minY_1)
	lastZ_1 = (maxZ_1 - minZ_1)

        lastX_2 = (maxX_2 - minX_2)
        lastY_2 = (maxY_2 - minY_2)
        lastZ_2 = (maxZ_2 - minZ_2)

        lastX_3 = (maxX_3 - minX_3)
        lastY_3 = (maxY_3 - minY_3)
        lastZ_3 = (maxZ_3 - minZ_3)

        lastX_4 = (maxX_4 - minX_4)
        lastY_4 = (maxY_4 - minY_4)
        lastZ_4 = (maxZ_4 - minZ_4)

	maxX_1 = -100000
	maxY_1 = -100000
	maxZ_1 = -100000

	minZ_1 = 100000
	minY_1 = 100000
	minX_1 = 100000

        maxX_2 = -100000
        maxY_2 = -100000
        maxZ_2 = -100000

        minZ_2 = 100000
        minY_2 = 100000
        minX_2 = 100000

        maxX_3 = -100000
        maxY_3 = -100000
        maxZ_3 = -100000

        minZ_3 = 100000
        minY_3 = 100000
        minX_3 = 100000

        maxX_4 = -100000
        maxY_4 = -100000
        maxZ_4 = -100000

        minZ_4 = 100000
        minY_4 = 100000
        minX_4 = 100000

	test = []

	decisionCounts = [0, 0, 0, 0]

	if(len(decisionsArray) > 20):
		for elem in decisionsArray:
			if(elem == 'A'):
				decisionCounts[0] = decisionCounts[0] + 1
                        if(elem == 'B'):
				decisionCounts[1] = decisionCounts[1] + 1
                        if(elem == 'C'):
				decisionCounts[2] = decisionCounts[2] + 1
                        if(elem == 'D'):
				decisionCounts[3] = decisionCounts[3] + 1

		decision = 'N'
		#max = 0
		if(decisionCounts[0] >= 5):
			decision = 'A'
		elif(decisionCounts[1] >= 5):
			decision = 'B'
		elif(decisionCounts[2] >= 5):
			decision = 'C'
		elif(decisionCounts[3] >= 5):
			decision = 'D'
		if(decision != 'N'):
			print(decision)
			postreq(decision)
		decisionsArray = []

	sleep(0.01)
	#clear()
