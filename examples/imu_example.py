import serial
import time
import numpy as np

imuSerial = serial.Serial(port ="/dev/ttyUSB0", baudrate=115200)
header_pass = 0
index = 0
raw_imu = np.zeros(65)
ka = 1/32768.0*16
kw = 1/32768.0*2000
kt = 1/32768.0*180


def decode(rawimu):
    bytedata = rawimu
    bytedata_shift8 = rawimu*(2**8)
    bytedata_shift16 = rawimu*(2**16)
    bytedata_shift24 = rawimu*(2**24)
    
    ax = np.int16(bytedata_shift8[3]+bytedata[2])*ka
    ay = np.int16(bytedata_shift8[5]+bytedata[4])*ka
    az = np.int16(bytedata_shift8[7]+bytedata[6])*ka
    
    wx = np.int16(bytedata_shift8[14]+bytedata[13])*kw
    wy = np.int16(bytedata_shift8[16]+bytedata[15])*kw
    wz = np.int16(bytedata_shift8[18]+bytedata[17])*kw

    roll  = np.int16(bytedata_shift8[25]*(2**8)+bytedata[24])/32768.0*180
    pitch = np.int16(bytedata_shift8[27]*(2**8)+bytedata[26])/32768.0*180
    yaw   = np.int16(bytedata_shift8[29]*(2**8)+bytedata[28])/32768.0*180

    height   = np.int32(bytedata_shift24[42]+ bytedata_shift16[41]+bytedata_shift8[40]+bytedata[39])/100

    raw_longitude = np.int32(bytedata_shift24[49]+bytedata_shift16[48]+bytedata_shift8[47]+bytedata[46])
    raw_latitude  = np.int32(bytedata_shift24[53]+bytedata_shift16[52]+bytedata_shift8[51]+bytedata[50])

    speeds =np.int32(bytedata_shift24[64]+bytedata_shift16[63]+bytedata_shift8[62]+bytedata[61])/1000*3.6
    
    lon = (raw_longitude/10000000) + (raw_longitude%10000000)/6000000.0
    lat  = (raw_latitude/10000000) + (raw_latitude %10000000)/6000000.0


while True:

        data = imuSerial.read()[0]
        if (data == 85 and header_pass == 0 and index == 0):
            raw_imu[index] = data
            index = 1

        
        elif(data == 81 and header_pass == 0 and index ==1):
            raw_imu[index]=data
            index = 2
            header_pass = 1
    
        
        elif(header_pass == 1 and index < 65):
                raw_imu[index] = data
                index = index+1

        
        elif(header_pass == 1 and index >=65):
                header_pass = 0
                index = 0
                fin = 1
                decode(raw_imu)
        
    
        else :
                    header_pass = 0
                    index = 0
                    fin = 0
            
        